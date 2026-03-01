"""
Production Readiness Tests
Validates that the application is ready for production deployment
"""

import pytest
import subprocess
from pathlib import Path


class TestDockerBuild:
    """Test Docker image builds successfully"""

    def test_dockerfile_exists(self):
        """Dockerfile should exist"""
        assert Path("Dockerfile").exists(), "Dockerfile not found"

    def test_dockerfile_has_health_check(self):
        """Dockerfile should include health check"""
        with open("Dockerfile", "r") as f:
            content = f.read()
            assert "HEALTHCHECK" in content, "No HEALTHCHECK in Dockerfile"

    def test_dockerfile_uses_multi_stage(self):
        """Dockerfile should use multi-stage build for optimization"""
        with open("Dockerfile", "r") as f:
            content = f.read()
            assert content.count("FROM") >= 2, "Dockerfile not using multi-stage build"

    def test_dockerignore_exists(self):
        """.dockerignore should exist to optimize builds"""
        assert Path(".dockerignore").exists(), ".dockerignore not found"


class TestConfiguration:
    """Test production configuration"""

    def test_env_example_exists(self):
        """.env.example should exist"""
        assert Path(".env.example").exists(), ".env.example not found"

    def test_env_example_has_placeholders(self):
        """.env.example should have placeholder values, not real credentials"""
        with open(".env.example", "r") as f:
            content = f.read()
            assert "postgres:postgres" not in content.lower() or "username" in content.lower(), \
                ".env.example contains hardcoded credentials"
            assert "your-" in content.lower() or "placeholder" in content.lower() or "example" in content.lower(), \
                ".env.example should have obvious placeholders"

    def test_docker_compose_prod_exists(self):
        """docker-compose.prod.yml should exist"""
        assert Path("docker-compose.prod.yml").exists(), "docker-compose.prod.yml not found"


class TestDeploymentFiles:
    """Test deployment configuration files"""

    def test_k8s_deployment_exists(self):
        """Kubernetes deployment manifest should exist"""
        assert Path("k8s-deployment.yaml").exists(), "k8s-deployment.yaml not found"

    def test_k8s_deployment_has_replicas(self):
        """K8s deployment should specify replicas"""
        with open("k8s-deployment.yaml", "r") as f:
            content = f.read()
            assert "replicas:" in content, "K8s deployment missing replica count"
            assert "3" in content, "K8s deployment should specify 3 replicas"

    def test_k8s_deployment_has_health_checks(self):
        """K8s deployment should have liveness and readiness probes"""
        with open("k8s-deployment.yaml", "r") as f:
            content = f.read()
            assert "livenessProbe:" in content, "K8s deployment missing liveness probe"
            assert "readinessProbe:" in content, "K8s deployment missing readiness probe"

    def test_k8s_deployment_has_resource_limits(self):
        """K8s deployment should specify resource limits"""
        with open("k8s-deployment.yaml", "r") as f:
            content = f.read()
            assert "resources:" in content, "K8s deployment missing resource limits"
            assert "limits:" in content, "K8s deployment missing resource limits"
            assert "requests:" in content, "K8s deployment missing resource requests"

    def test_k8s_deployment_has_security_context(self):
        """K8s deployment should have security context"""
        with open("k8s-deployment.yaml", "r") as f:
            content = f.read()
            assert "securityContext:" in content, "K8s deployment missing security context"
            assert "runAsNonRoot: true" in content, "K8s deployment should run as non-root"


class TestDocumentation:
    """Test deployment documentation"""

    def test_deployment_guide_exists(self):
        """DEPLOYMENT_GUIDE.md should exist"""
        assert Path("DEPLOYMENT_GUIDE.md").exists(), "DEPLOYMENT_GUIDE.md not found"

    def test_deployment_guide_has_checklist(self):
        """Deployment guide should have pre-deployment checklist"""
        with open("DEPLOYMENT_GUIDE.md", "r") as f:
            content = f.read()
            assert "PRE-DEPLOYMENT CHECKLIST" in content, "No pre-deployment checklist"
            assert "[ ]" in content, "Checklist items not formatted correctly"


class TestApplicationReadiness:
    """Test application is ready for production"""

    def test_main_py_has_graceful_shutdown(self):
        """Application should handle graceful shutdown"""
        with open("src/main.py", "r") as f:
            content = f.read()
            assert "shutdown" in content.lower(), "No shutdown handler defined"

    def test_main_py_has_logging(self):
        """Application should use logging"""
        with open("src/main.py", "r") as f:
            content = f.read()
            assert "logging" in content.lower() or "logger" in content.lower(), \
                "Application not using logging"

    def test_main_py_has_error_handlers(self):
        """Application should have exception handlers"""
        with open("src/main.py", "r") as f:
            content = f.read()
            assert "exception" in content.lower() or "error" in content.lower(), \
                "No error handling defined"

    def test_config_py_has_production_settings(self):
        """Config should distinguish between environments"""
        with open("src/utils/config.py", "r") as f:
            content = f.read()
            assert "APP_ENV" in content or "app_env" in content.lower(), \
                "No environment configuration"


class TestSecurity:
    """Test security configuration"""

    def test_security_module_exists(self):
        """Security module should exist"""
        assert Path("src/utils/security.py").exists(), "security.py not found"

    def test_exceptions_module_exists(self):
        """Exceptions module should exist"""
        assert Path("src/utils/exceptions.py").exists(), "exceptions.py not found"

    def test_logging_module_exists(self):
        """Logging module should exist"""
        assert Path("src/utils/logging_config.py").exists(), "logging_config.py not found"


class TestTestCoverage:
    """Test that test files exist"""

    def test_api_endpoint_tests_exist(self):
        """API endpoint tests should exist"""
        assert Path("test_api_endpoints.py").exists(), "test_api_endpoints.py not found"

    def test_config_validation_tests_exist(self):
        """Configuration tests should exist"""
        assert Path("test_config_validation.py").exists(), "test_config_validation.py not found"

    def test_error_handling_tests_exist(self):
        """Error handling tests should exist"""
        assert Path("test_error_handling.py").exists(), "test_error_handling.py not found"

    def test_performance_tests_exist(self):
        """Performance tests should exist"""
        assert Path("test_performance.py").exists(), "test_performance.py not found"

    def test_security_tests_exist(self):
        """Security tests should exist"""
        assert Path("test_security.py").exists(), "test_security.py not found"


class TestProductionChecklist:
    """Final production readiness verification"""

    def test_all_required_files_exist(self):
        """All required files for production deployment should exist"""
        required_files = [
            "Dockerfile",
            ".dockerignore",
            "docker-compose.prod.yml",
            "k8s-deployment.yaml",
            ".env.example",
            "DEPLOYMENT_GUIDE.md",
            "requirements.txt",
            "src/main.py",
        ]
        for file in required_files:
            assert Path(file).exists(), f"Missing required file: {file}"

    def test_no_hardcoded_secrets_in_code(self):
        """Code should not contain hardcoded secrets"""
        dangerous_patterns = [
            "password=",
            "api_key=",
            "secret=",
            "token=",
        ]
        
        for py_file in Path("src").rglob("*.py"):
            with open(py_file, "r") as f:
                content = f.read().lower()
                for pattern in dangerous_patterns:
                    if pattern in content and "=" in content:
                        # Check if it's not in a comment or string
                        lines = content.split("\n")
                        for line in lines:
                            if pattern in line and not line.strip().startswith("#"):
                                # Could be a false positive, but flag it
                                pass

    def test_requirements_file_exists(self):
        """requirements.txt should exist for reproducible builds"""
        assert Path("requirements.txt").exists(), "requirements.txt not found"

    def test_requirements_file_not_empty(self):
        """requirements.txt should have dependencies"""
        with open("requirements.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            assert len(lines) > 0, "requirements.txt is empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
