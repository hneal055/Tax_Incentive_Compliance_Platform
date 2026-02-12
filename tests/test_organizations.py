"""
Test organization admin endpoints
"""
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from jose import jwt
from src.utils.config import settings


class MockUser:
    """Mock user object for testing"""
    def __init__(self, id="test-user-id", email="test@example.com", name="Test User"):
        self.id = id
        self.email = email
        self.name = name


class MockOrg:
    """Mock organization object for testing"""
    def __init__(self, id="test-org-id", name="Test Organization", slug="test-org"):
        self.id = id
        self.name = name
        self.slug = slug
        self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)


class MockMembership:
    """Mock membership object for testing"""
    def __init__(self, id="test-membership-id", user_id="test-user-id", org_id="test-org-id", role="ADMIN", user=None, organization=None):
        self.id = id
        self.userId = user_id
        self.organizationId = org_id
        self.role = role
        self.user = user or MockUser(id=user_id)
        self.organization = organization or MockOrg(id=org_id)
        self.createdAt = datetime.now(timezone.utc)
        self.updatedAt = datetime.now(timezone.utc)


def create_test_jwt(test_user):
    """Create a test JWT token for a user"""
    payload = {
        "sub": test_user.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


@pytest.fixture
def test_user():
    """Test user fixture"""
    return MockUser()


@pytest.fixture
def test_org():
    """Test organization fixture"""
    return MockOrg()


@pytest.fixture
def test_admin_membership(test_user, test_org):
    """Test admin membership fixture"""
    return MockMembership(user_id=test_user.id, org_id=test_org.id, role="ADMIN", user=test_user, organization=test_org)


@pytest.fixture
async def client():
    """HTTP client for testing"""
    from src.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_organization_success(client, test_org, test_user, test_admin_membership):
    """Test getting organization details as admin"""
    from src.main import app
    
    # Mock database calls
    with patch('src.utils.database.prisma') as mock_prisma:
        # Mock the user lookup in auth
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        
        # Mock membership lookup for auth
        mock_prisma.membership.find_first = AsyncMock(return_value=test_admin_membership)
        
        # Mock organization lookup
        mock_prisma.organization.find_unique = AsyncMock(return_value=test_org)
        
        # Create JWT token
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        # Make request
        response = await client.get(f"/api/v1/organizations/{test_org.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_org.id
        assert data["name"] == test_org.name
        assert data["slug"] == test_org.slug


@pytest.mark.asyncio
async def test_get_organization_forbidden_different_org(client, test_user):
    """Test that users cannot access other organizations"""
    from src.main import app
    
    test_org = MockOrg(id="org-1")
    other_org_id = "org-2"
    test_membership = MockMembership(user_id=test_user.id, org_id=test_org.id, role="ADMIN", user=test_user, organization=test_org)
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(return_value=test_membership)
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get(f"/api/v1/organizations/{other_org_id}", headers=headers)
        
        assert response.status_code == 403
        assert "Cannot access other organizations" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_organization_not_admin(client, test_user, test_org):
    """Test that non-admin users cannot access organization endpoints"""
    from src.main import app
    
    # Create a MEMBER (not ADMIN) membership
    test_membership = MockMembership(user_id=test_user.id, org_id=test_org.id, role="MEMBER", user=test_user, organization=test_org)
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(return_value=test_membership)
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get(f"/api/v1/organizations/{test_org.id}", headers=headers)
        
        assert response.status_code == 403
        assert "Admin role required" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_organization_success(client, test_org, test_user, test_admin_membership):
    """Test updating organization details as admin"""
    from src.main import app
    
    updated_org = MockOrg(id=test_org.id, name="Updated Organization", slug="updated-org")
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(return_value=test_admin_membership)
        mock_prisma.organization.find_first = AsyncMock(return_value=None)  # No slug conflict
        mock_prisma.organization.update = AsyncMock(return_value=updated_org)
        
        # Mock audit log service
        with patch('src.services.audit_log_service.audit_log_service.log_action', new_callable=AsyncMock):
            token = create_test_jwt(test_user)
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.put(
                f"/api/v1/organizations/{test_org.id}",
                headers=headers,
                json={"name": "Updated Organization", "slug": "updated-org"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Updated Organization"
            assert data["slug"] == "updated-org"


@pytest.mark.asyncio
async def test_update_organization_slug_conflict(client, test_org, test_user, test_admin_membership):
    """Test updating organization with slug that already exists"""
    from src.main import app
    
    conflicting_org = MockOrg(id="other-org-id", slug="existing-slug")
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(return_value=test_admin_membership)
        mock_prisma.organization.find_first = AsyncMock(return_value=conflicting_org)
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.put(
            f"/api/v1/organizations/{test_org.id}",
            headers=headers,
            json={"slug": "existing-slug"}
        )
        
        assert response.status_code == 409
        assert "slug already in use" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_organization_members(client, test_org, test_user, test_admin_membership):
    """Test listing organization members"""
    from src.main import app
    
    member_user = MockUser(id="member-user-id", email="member@example.com", name="Member User")
    member_membership = MockMembership(
        id="member-membership-id",
        user_id=member_user.id,
        org_id=test_org.id,
        role="MEMBER",
        user=member_user,
        organization=test_org
    )
    
    memberships = [test_admin_membership, member_membership]
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(return_value=test_admin_membership)
        mock_prisma.membership.find_many = AsyncMock(return_value=memberships)
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get(f"/api/v1/organizations/{test_org.id}/members", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["role"] in ["ADMIN", "MEMBER"]
        assert data[1]["role"] in ["ADMIN", "MEMBER"]


@pytest.mark.asyncio
async def test_add_organization_member(client, test_org, test_user, test_admin_membership):
    """Test adding a new member to organization"""
    from src.main import app
    
    new_user = MockUser(id="new-user-id", email="newuser@example.com", name="New User")
    new_membership = MockMembership(
        id="new-membership-id",
        user_id=new_user.id,
        org_id=test_org.id,
        role="MEMBER",
        user=new_user,
        organization=test_org
    )
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(side_effect=[test_user, new_user])
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, None])  # Admin check, then no existing membership
        mock_prisma.membership.create = AsyncMock(return_value=new_membership)
        
        with patch('src.services.audit_log_service.audit_log_service.log_action', new_callable=AsyncMock):
            token = create_test_jwt(test_user)
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.post(
                f"/api/v1/organizations/{test_org.id}/members",
                headers=headers,
                json={"userId": new_user.id, "role": "MEMBER"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["userId"] == new_user.id
            assert data["role"] == "MEMBER"


@pytest.mark.asyncio
async def test_add_organization_member_already_exists(client, test_org, test_user, test_admin_membership):
    """Test adding a member that already exists"""
    from src.main import app
    
    existing_user = MockUser(id="existing-user-id", email="existing@example.com")
    existing_membership = MockMembership(user_id=existing_user.id, org_id=test_org.id, role="MEMBER")
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(side_effect=[test_user, existing_user])
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, existing_membership])
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.post(
            f"/api/v1/organizations/{test_org.id}/members",
            headers=headers,
            json={"userId": existing_user.id, "role": "MEMBER"}
        )
        
        assert response.status_code == 409
        assert "already a member" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_member_role(client, test_org, test_user, test_admin_membership):
    """Test updating a member's role"""
    from src.main import app
    
    member_user = MockUser(id="member-user-id", email="member@example.com")
    member_membership = MockMembership(user_id=member_user.id, org_id=test_org.id, role="MEMBER", user=member_user)
    updated_membership = MockMembership(user_id=member_user.id, org_id=test_org.id, role="ADMIN", user=member_user)
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, member_membership])
        mock_prisma.membership.update = AsyncMock(return_value=updated_membership)
        
        with patch('src.services.audit_log_service.audit_log_service.log_action', new_callable=AsyncMock):
            token = create_test_jwt(test_user)
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.put(
                f"/api/v1/organizations/{test_org.id}/members/{member_user.id}",
                headers=headers,
                json={"role": "ADMIN"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["role"] == "ADMIN"


@pytest.mark.asyncio
async def test_update_member_role_prevent_self_demotion(client, test_org, test_user, test_admin_membership):
    """Test that last admin cannot demote themselves"""
    from src.main import app
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, test_admin_membership])
        mock_prisma.membership.count = AsyncMock(return_value=1)  # Only 1 admin
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.put(
            f"/api/v1/organizations/{test_org.id}/members/{test_user.id}",
            headers=headers,
            json={"role": "MEMBER"}
        )
        
        assert response.status_code == 400
        assert "at least one admin" in response.json()["detail"]


@pytest.mark.asyncio
async def test_remove_organization_member(client, test_org, test_user, test_admin_membership):
    """Test removing a member from organization"""
    from src.main import app
    
    member_user = MockUser(id="member-user-id", email="member@example.com")
    member_membership = MockMembership(user_id=member_user.id, org_id=test_org.id, role="MEMBER", user=member_user)
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, member_membership])
        mock_prisma.membership.delete = AsyncMock(return_value=None)
        
        with patch('src.services.audit_log_service.audit_log_service.log_action', new_callable=AsyncMock):
            token = create_test_jwt(test_user)
            headers = {"Authorization": f"Bearer {token}"}
            
            response = await client.delete(
                f"/api/v1/organizations/{test_org.id}/members/{member_user.id}",
                headers=headers
            )
            
            assert response.status_code == 204


@pytest.mark.asyncio
async def test_remove_member_prevent_self_removal_last_admin(client, test_org, test_user, test_admin_membership):
    """Test that last admin cannot remove themselves"""
    from src.main import app
    
    with patch('src.utils.database.prisma') as mock_prisma:
        mock_prisma.user.find_unique = AsyncMock(return_value=test_user)
        mock_prisma.membership.find_first = AsyncMock(side_effect=[test_admin_membership, test_admin_membership])
        mock_prisma.membership.count = AsyncMock(return_value=1)  # Only 1 admin
        
        token = create_test_jwt(test_user)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.delete(
            f"/api/v1/organizations/{test_org.id}/members/{test_user.id}",
            headers=headers
        )
        
        assert response.status_code == 400
        assert "at least one admin" in response.json()["detail"]
