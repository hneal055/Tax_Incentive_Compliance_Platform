"""
Jurisdictions API
- Robust list endpoint with filtering, ordering, pagination
- Tight payload by default (no relations, no timestamps)
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Literal

from src.utils.database import prisma


router = APIRouter(prefix="/jurisdictions", tags=["Jurisdictions"])


# ----------------------------
# Response Models (tight by default)
# ----------------------------

class JurisdictionTight(BaseModel):
    id: str
    code: str
    name: str
    country: str
    type: str
    active: bool
    description: Optional[str] = None
    website: Optional[str] = None


class JurisdictionMeta(JurisdictionTight):
    contactInfo: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class JurisdictionsListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    q: Optional[str] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    order: Dict[str, str] = Field(default_factory=dict)
    jurisdictions: List[Dict[str, Any]]


# ----------------------------
# Helpers
# ----------------------------

ALLOWED_ORDER_FIELDS = {
    "code",
    "name",
    "country",
    "type",
    "active",
    "createdAt",
    "updatedAt",
}

def _tighten_row(row: Any, include_meta: bool) -> Dict[str, Any]:
    """
    Prisma returns model objects; convert to dict using model_dump() if present.
    Then shrink payload to allowed keys.
    """
    if hasattr(row, "model_dump"):
        data = row.model_dump()
    elif isinstance(row, dict):
        data = row
    else:
        # best-effort fallback
        data = dict(row)

    base = {
        "id": data.get("id"),
        "code": data.get("code"),
        "name": data.get("name"),
        "country": data.get("country"),
        "type": data.get("type"),
        "active": data.get("active"),
        "description": data.get("description"),
        "website": data.get("website"),
    }

    if include_meta:
        base.update(
            {
                "contactInfo": data.get("contactInfo"),
                "createdAt": str(data.get("createdAt")) if data.get("createdAt") is not None else None,
                "updatedAt": str(data.get("updatedAt")) if data.get("updatedAt") is not None else None,
            }
        )

    # Remove None values to keep payload tight
    return {k: v for k, v in base.items() if v is not None}


def _build_where(
    q: Optional[str],
    country: Optional[str],
    j_type: Optional[str],
    active: Optional[bool],
) -> Optional[Dict[str, Any]]:
    clauses: List[Dict[str, Any]] = []

    if country:
        clauses.append({"country": {"equals": country}})

    if j_type:
        clauses.append({"type": {"equals": j_type}})

    if active is not None:
        clauses.append({"active": {"equals": active}})

    if q:
        # Prisma Client Python supports string filters incl. mode=insensitive on PostgreSQL :contentReference[oaicite:1]{index=1}
        q_clause = {
            "OR": [
                {"name": {"contains": q, "mode": "insensitive"}},
                {"code": {"contains": q, "mode": "insensitive"}},
                {"country": {"contains": q, "mode": "insensitive"}},
                {"description": {"contains": q, "mode": "insensitive"}},
            ]
        }
        clauses.append(q_clause)

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"AND": clauses}


# ----------------------------
# Routes
# ----------------------------

@router.get("/", response_model=JurisdictionsListResponse)
async def list_jurisdictions(
    limit: int = Query(50, ge=1, le=2000),
    offset: int = Query(0, ge=0),
    q: Optional[str] = Query(None, min_length=1, max_length=200),
    country: Optional[str] = Query(None, max_length=60),
    type: Optional[str] = Query(None, max_length=30, alias="type"),
    active: Optional[bool] = Query(None),
    order_by: str = Query("code"),
    order_dir: Literal["asc", "desc"] = Query("asc"),
    include_meta: bool = Query(False, description="Include timestamps/contactInfo"),
    include_relations: bool = Query(False, description="Include related objects (can expand payload)"),
) -> JurisdictionsListResponse:
    """
    List jurisdictions with filtering, ordering, pagination.

    IMPORTANT: Prisma Client Python uses `order=` (not `order_by=`) and `take/skip`. :contentReference[oaicite:2]{index=2}
    """
    if order_by not in ALLOWED_ORDER_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order_by '{order_by}'. Allowed: {sorted(ALLOWED_ORDER_FIELDS)}",
        )

    where = _build_where(q=q, country=country, j_type=type, active=active)

    # Prisma Client Python: take/skip/order/include :contentReference[oaicite:3]{index=3}
    find_kwargs: Dict[str, Any] = {
        "take": limit,
        "skip": offset,
        "order": {order_by: order_dir},
    }
    if where is not None:
        find_kwargs["where"] = where

    # Only include relations if explicitly asked (keeps default payload tight)
    if include_relations:
        # Adjust relation names if your schema differs
        find_kwargs["include"] = {
            "incentiveRules": True,
            "productions": True,
        }

    try:
        total = await prisma.jurisdiction.count(where=where) if where is not None else await prisma.jurisdiction.count()
        rows = await prisma.jurisdiction.find_many(**find_kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jurisdictions: {e}")

    # Tighten each row for response payload
    jurisdictions_out: List[Dict[str, Any]] = []
    for r in rows:
        jurisdictions_out.append(_tighten_row(r, include_meta=include_meta))

    return JurisdictionsListResponse(
        total=int(total),
        limit=limit,
        offset=offset,
        q=q,
        filters={"country": country, "type": type, "active": active},
        order={"by": order_by, "dir": order_dir},
        jurisdictions=jurisdictions_out,
    )


@router.get("/{code}")
async def get_jurisdiction_by_code(
    code: str,
    include_meta: bool = Query(False),
    include_relations: bool = Query(False),
) -> Dict[str, Any]:
    """
    Fetch a single jurisdiction by code (case-insensitive).
    """
    code_norm = code.strip().upper()

    find_kwargs: Dict[str, Any] = {
        "where": {"code": {"equals": code_norm}},
    }
    if include_relations:
        find_kwargs["include"] = {
            "incentiveRules": True,
            "productions": True,
        }

    try:
        j = await prisma.jurisdiction.find_unique(**find_kwargs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jurisdiction: {e}")

    if not j:
        raise HTTPException(status_code=404, detail=f"Jurisdiction '{code_norm}' not found")

    return _tighten_row(j, include_meta=include_meta)
