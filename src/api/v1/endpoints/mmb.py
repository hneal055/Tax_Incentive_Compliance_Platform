"""
MMB (Movie Magic Budgeting) Integration API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Dict, Any
import tempfile
from pathlib import Path

from src.mmb_parser.parser import MMBParser


router = APIRouter(prefix="/mmb", tags=["MMB Integration"])


@router.post("/upload")
async def upload_mmb_file(
    file: UploadFile = File(...),
    jurisdiction: str = Query("georgia", description="Jurisdiction code for incentive calculation")
) -> Dict[str, Any]:
    """
    Upload and parse an MMB (Movie Magic Budgeting) file.
    
    Supports .mmbx (XML) and .csv file formats.
    Returns parsed budget data with eligible expenses calculated based on jurisdiction rules.
    """
    
    # Validate file type
    if not file.filename.endswith(('.mmbx', '.csv', '.xlsx')):
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Supported formats: .mmbx, .csv, .xlsx"
        )
    
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Parse
        parser = MMBParser(temp_path)
        data = parser.parse()
        
        # Get eligible expenses
        eligible_df = parser.get_eligible_expenses(jurisdiction)
        eligible_total = eligible_df["amount"].sum() if not eligible_df.empty else 0
        
        # Calculate estimated credit (simplified for demo)
        credit_rate = 0.30  # 30% base for Georgia
        if jurisdiction == "georgia":
            # Check for music uplift
            music_df = eligible_df[eligible_df["description"].str.contains("Scoring", na=False)]
            if not music_df.empty:
                credit_rate = 0.40  # 30% + 10% uplift
        
        estimated_credit = eligible_total * credit_rate
        
        # Build optimization opportunities
        optimization_opportunities = []
        if jurisdiction == "georgia":
            music_items = eligible_df[eligible_df["description"].str.contains("Music", na=False)]
            if not music_items.empty:
                current_music = music_items["amount"].sum()
                potential_music = current_music * 1.1  # 10% uplift potential
                optimization_opportunities.append({
                    "category": "Music Scoring",
                    "current": float(current_music),
                    "potential": float(potential_music),
                    "recommendation": "Move scoring to Atlanta for 10% uplift"
                })
        
        return {
            "filename": file.filename,
            "production": data.get("production", {}),
            "summary": {
                "total_budget": data["summary"]["total"],
                "eligible_expenses": round(eligible_total, 2),
                "estimated_credit": round(estimated_credit, 2),
                "credit_rate": f"{credit_rate*100:.0f}%",
                "line_items_parsed": len(data["line_items"])
            },
            "optimization_opportunities": optimization_opportunities
        }
    
    finally:
        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)


@router.get("/", summary="MMB Integration Info")
async def mmb_info() -> Dict[str, Any]:
    """
    Get information about the MMB integration endpoint.
    """
    return {
        "name": "Movie Magic Budgeting Integration",
        "description": "Upload and parse MMB files to analyze tax incentive eligibility",
        "supported_formats": [".mmbx", ".csv", ".xlsx"],
        "endpoints": {
            "upload": "/api/v1/mmb/upload"
        }
    }
