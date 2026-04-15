# create_maximizer.ps1
# PowerShell script to create all Maximizer engine files for SceneIQ

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SceneIQ Maximizer File Creator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set your project path - UPDATE THIS TO YOUR ACTUAL PATH
$ProjectPath = "C:\Dev\tax-incentive-compliance-platform"

# Verify path exists
if (-not (Test-Path $ProjectPath)) {
    Write-Host "ERROR: Project path not found: $ProjectPath" -ForegroundColor Red
    Write-Host "Please update `$ProjectPath variable in this script." -ForegroundColor Yellow
    exit 1
}
$ProjectPath = "C:\Dev\tax-incentive-compliance-platform"
Write-Host "Creating Maximizer files in: $ProjectPath" -ForegroundColor Green
Write-Host ""

# Function to create file with content
function Create-File {
    param(
        [string]$RelativePath,
        [string]$Content
    )
    
    $FullPath = Join-Path $ProjectPath $RelativePath
    $Directory = Split-Path $FullPath -Parent
    
    # Create directory if it doesn't exist
    if (-not (Test-Path $Directory)) {
        New-Item -ItemType Directory -Path $Directory -Force | Out-Null
        Write-Host "  Created directory: $Directory" -ForegroundColor Gray
    }
    
    # Write file
    Set-Content -Path $FullPath -Value $Content -Encoding UTF8
    Write-Host "  Created file: $RelativePath" -ForegroundColor Green
}

# -------------------------------------------------------------------
# File 1: maximizer.py (Core Engine)
# -------------------------------------------------------------------
$MaximizerPy = @'
"""
SceneIQ Maximizer Engine
Optimizes tax incentives across multiple jurisdiction layers (state, county, city, town, village)
Handles additive stacking, override selection, and conflict resolution.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ConflictResolution(Enum):
    HIGHEST_VALUE = "highest_value"
    LOWEST_VALUE = "lowest_value"
    MOST_RESTRICTIVE = "most_restrictive"
    LEAST_RESTRICTIVE = "least_restrictive"
    JURISDICTION_PRIORITY = "jurisdiction_priority"

@dataclass
class ApplicableRule:
    """A rule that applies to a specific project"""
    jurisdiction_id: str
    jurisdiction_name: str
    jurisdiction_type: str
    rule_key: str
    rule_type: str
    value: Optional[float]
    value_unit: str
    inheritance_mode: str
    conflict_priority: int
    source_citation: str
    effective_date: datetime

@dataclass
class MaximizedResult:
    """Final maximized incentive package"""
    total_value: float
    total_value_unit: str
    breakdown: Dict[str, float]
    applied_rules: List[ApplicableRule]
    overridden_rules: List[ApplicableRule]
    conflicts_resolved: List[str]
    warnings: List[str]
    recommendations: List[str]

class SceneIQMaximizer:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL not set")
    
    def get_connection(self):
        return psycopg2.connect(self.db_url)
    
    def resolve_jurisdiction_layers(self, lat: float, lng: float) -> List[Dict]:
        """Resolve all jurisdiction layers containing a point"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                SELECT id, name, type, level, parent_jurisdiction_id
                FROM jurisdictions
                WHERE ST_Contains(geometry, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ORDER BY level ASC
            """, (lng, lat))
            results = cur.fetchall()
            if results:
                cur.close()
                conn.close()
                return results
        except Exception as e:
            logger.debug(f"Spatial query failed: {e}")
        
        cur.execute("""
            SELECT id, name, type, level, parent_jurisdiction_id
            FROM jurisdictions
            WHERE active = true
            ORDER BY level ASC
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    
    def fetch_applicable_rules(self, jurisdiction_ids: List[str], project_type: str) -> List[ApplicableRule]:
        """Fetch all active rules for given jurisdictions"""
        if not jurisdiction_ids:
            return []
        
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        placeholders = ','.join(['%s'] * len(jurisdiction_ids))
        cur.execute(f"""
            SELECT 
                lr.jurisdiction_id,
                j.name as jurisdiction_name,
                j.type as jurisdiction_type,
                lr.rule_key,
                lr.rule_type,
                lr.value,
                lr.value_unit,
                COALESCE(ip.inheritance_mode, 'additive') as inheritance_mode,
                COALESCE(ip.conflict_priority, 10) as conflict_priority,
                lr.source_citation,
                lr.effective_date
            FROM local_rules lr
            JOIN jurisdictions j ON lr.jurisdiction_id = j.id
            LEFT JOIN inheritance_policies ip 
                ON ip.jurisdiction_id = lr.jurisdiction_id 
                AND ip.rule_category = (
                    CASE lr.rule_type
                        WHEN 'tax_abatement' THEN 'incentives'
                        WHEN 'green_bonus' THEN 'incentives'
                        WHEN 'permit_fee' THEN 'fees'
                        WHEN 'setback' THEN 'zoning'
                        WHEN 'zoning_restriction' THEN 'zoning'
                        ELSE 'other'
                    END
                )
            WHERE lr.jurisdiction_id IN ({placeholders})
                AND (lr.expiry_date IS NULL OR lr.expiry_date > NOW())
                AND (lr.effective_date <= NOW())
                AND (lr.applies_to::jsonb ? %s OR lr.applies_to::jsonb ? 'all')
            ORDER BY j.level ASC, ip.conflict_priority ASC
        """, jurisdiction_ids + [project_type])
        
        rules = cur.fetchall()
        cur.close()
        conn.close()
        
        return [
            ApplicableRule(
                jurisdiction_id=r['jurisdiction_id'],
                jurisdiction_name=r['jurisdiction_name'],
                jurisdiction_type=r['jurisdiction_type'],
                rule_key=r['rule_key'],
                rule_type=r['rule_type'],
                value=r['value'],
                value_unit=r['value_unit'] or 'USD',
                inheritance_mode=r['inheritance_mode'],
                conflict_priority=r['conflict_priority'],
                source_citation=r['source_citation'],
                effective_date=r['effective_date']
            )
            for r in rules
        ]
    
    def apply_inheritance_logic(self, rules: List[ApplicableRule]) -> Tuple[List[ApplicableRule], List[ApplicableRule]]:
        """Apply strict/override/additive inheritance rules"""
        applied = []
        overridden = []
        
        rules_by_key: Dict[str, List[ApplicableRule]] = {}
        for rule in rules:
            if rule.rule_key not in rules_by_key:
                rules_by_key[rule.rule_key] = []
            rules_by_key[rule.rule_key].append(rule)
        
        for rule_key, rule_group in rules_by_key.items():
            rule_group.sort(key=lambda x: (
                0 if x.jurisdiction_type == 'state' else
                1 if x.jurisdiction_type == 'county' else
                2 if x.jurisdiction_type in ['city', 'town'] else 3,
                x.conflict_priority
            ))
            
            current_rule = None
            for rule in rule_group:
                if current_rule is None:
                    current_rule = rule
                    continue
                
                if rule.inheritance_mode == 'strict':
                    overridden.append(rule)
                elif rule.inheritance_mode == 'override':
                    overridden.append(current_rule)
                    current_rule = rule
                elif rule.inheritance_mode == 'additive':
                    if current_rule.value is not None and rule.value is not None:
                        if current_rule.value_unit == rule.value_unit:
                            current_rule.value += rule.value
                            applied.append(rule)
                        else:
                            applied.append(current_rule)
                            applied.append(rule)
                            current_rule = None
                    else:
                        applied.append(rule)
                else:
                    applied.append(rule)
            
            if current_rule:
                applied.append(current_rule)
        
        return applied, overridden
    
    def calculate_net_value(self, applied_rules: List[ApplicableRule]) -> Dict[str, float]:
        """Calculate net total value by category"""
        breakdown = {
            'tax_abatement': 0.0,
            'green_bonus': 0.0,
            'permit_fee': 0.0,
            'setback': 0.0,
            'zoning_restriction': 0.0,
            'other': 0.0
        }
        
        for rule in applied_rules:
            category = rule.rule_type
            value = rule.value or 0.0
            if category == 'permit_fee':
                value = -abs(value)
            if category in breakdown:
                breakdown[category] += value
            else:
                breakdown['other'] += value
        
        return breakdown
    
    def generate_recommendations(self, applied_rules: List[ApplicableRule], 
                                  overridden_rules: List[ApplicableRule],
                                  breakdown: Dict[str, float]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if overridden_rules:
            top_override = overridden_rules[0]
            recommendations.append(
                f"Local {top_override.jurisdiction_name} overrides state rules for '{top_override.rule_key}'"
            )
        
        if breakdown.get('permit_fee', 0) < -1000:
            recommendations.append("High permit fees detected. Consider alternative jurisdiction.")
        
        additive_count = len([r for r in applied_rules if r.inheritance_mode == 'additive'])
        if additive_count >= 2:
            recommendations.append(f"Multiple additive incentives ({additive_count}) available. Stack for maximum benefit.")
        
        return recommendations
    
    def maximize(self, lat: float, lng: float, project_type: str = 'all') -> MaximizedResult:
        """Main entry point: maximize incentives for a project location"""
        jurisdictions = self.resolve_jurisdiction_layers(lat, lng)
        jurisdiction_ids = [j['id'] for j in jurisdictions]
        
        if not jurisdiction_ids:
            return MaximizedResult(
                total_value=0.0, total_value_unit='USD', breakdown={},
                applied_rules=[], overridden_rules=[], conflicts_resolved=[],
                warnings=['No jurisdictions found'], recommendations=[]
            )
        
        all_rules = self.fetch_applicable_rules(jurisdiction_ids, project_type)
        
        if not all_rules:
            return MaximizedResult(
                total_value=0.0, total_value_unit='USD', breakdown={},
                applied_rules=[], overridden_rules=[],
                conflicts_resolved=['No active rules found'],
                warnings=['Run monitor.py to populate local_rules'],
                recommendations=['Ensure monitor has been executed']
            )
        
        applied_rules, overridden_rules = self.apply_inheritance_logic(all_rules)
        breakdown = self.calculate_net_value(applied_rules)
        total_value = sum(v for v in breakdown.values())
        recommendations = self.generate_recommendations(applied_rules, overridden_rules, breakdown)
        
        conflicts_resolved = [f"{r.jurisdiction_name} {r.rule_key} overridden" for r in overridden_rules]
        warnings = []
        if breakdown.get('permit_fee', 0) < 0:
            warnings.append(f"Net fees of ${-breakdown['permit_fee']:.2f} reduce incentive value")
        
        return MaximizedResult(
            total_value=total_value, total_value_unit='USD', breakdown=breakdown,
            applied_rules=applied_rules, overridden_rules=overridden_rules,
            conflicts_resolved=conflicts_resolved, warnings=warnings, recommendations=recommendations
        )


def main():
    import sys
    import json
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 3:
        print("Usage: python maximizer.py <lat> <lng> [project_type]")
        print("Example: python maximizer.py 40.7128 -74.0060 solar")
        sys.exit(1)
    
    lat = float(sys.argv[1])
    lng = float(sys.argv[2])
    project_type = sys.argv[3] if len(sys.argv) > 3 else 'all'
    
    maximizer = SceneIQMaximizer()
    result = maximizer.maximize(lat, lng, project_type)
    
    print(json.dumps({
        'total_value': result.total_value,
        'total_value_unit': result.total_value_unit,
        'breakdown': result.breakdown,
        'warnings': result.warnings,
        'recommendations': result.recommendations,
        'applied_rules_count': len(result.applied_rules),
        'overridden_rules_count': len(result.overridden_rules)
    }, indent=2))

if __name__ == "__main__":
    main()
'@

# -------------------------------------------------------------------
# File 2: api_maximizer.py (FastAPI endpoint)
# -------------------------------------------------------------------
$ApiMaximizerPy = @'
# api_maximizer.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from maximizer import SceneIQMaximizer

app = FastAPI(title="SceneIQ Maximizer API")
maximizer = SceneIQMaximizer()

class MaximizeResponse(BaseModel):
    total_value: float
    total_value_unit: str
    breakdown: dict
    warnings: List[str]
    recommendations: List[str]
    applied_rules_count: int
    overridden_rules_count: int

@app.get("/maximize", response_model=MaximizeResponse)
def maximize(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    project_type: str = Query("all", description="Project type")
):
    result = maximizer.maximize(lat, lng, project_type)
    return MaximizeResponse(
        total_value=result.total_value,
        total_value_unit=result.total_value_unit,
        breakdown=result.breakdown,
        warnings=result.warnings,
        recommendations=result.recommendations,
        applied_rules_count=len(result.applied_rules),
        overridden_rules_count=len(result.overridden_rules)
    )

@app.get("/health")
def health():
    return {"status": "ok"}
'@

# -------------------------------------------------------------------
# File 3: test_maximizer.py (Test script)
# -------------------------------------------------------------------
$TestMaximizerPy = @'
# test_maximizer.py
from maximizer import SceneIQMaximizer

def test_maximizer():
    maximizer = SceneIQMaximizer()
    
    result = maximizer.maximize(42.8864, -78.8784, "solar")
    
    print("\n" + "="*60)
    print("PILOTFORGE MAXIMIZER RESULT")
    print("="*60)
    print(f"Total Value: ${result.total_value:.2f} {result.total_value_unit}")
    print(f"\nBreakdown:")
    for category, value in result.breakdown.items():
        if value != 0:
            print(f"  {category}: ${value:.2f}")
    
    if result.warnings:
        print(f"\nWarnings:")
        for w in result.warnings:
            print(f"  ⚠ {w}")
    
    if result.recommendations:
        print(f"\nRecommendations:")
        for r in result.recommendations:
            print(f"  → {r}")
    
    print(f"\nApplied Rules: {len(result.applied_rules)}")
    print(f"Overridden Rules: {len(result.overridden_rules)}")

if __name__ == "__main__":
    test_maximizer()
'@

# -------------------------------------------------------------------
# File 4: seed_test_data.sql (Sample test data)
# -------------------------------------------------------------------
$SeedTestDataSql = @'
-- seed_test_data.sql
-- Sample test data for SceneIQ Maximizer

-- Insert New York State (if not exists)
INSERT INTO jurisdictions (id, name, type, level, active)
VALUES ('11111111-1111-1111-1111-111111111111', 'New York', 'state', 0, true)
ON CONFLICT (id) DO NOTHING;

-- Insert Erie County
INSERT INTO jurisdictions (id, name, type, parent_jurisdiction_id, level, active)
VALUES ('22222222-2222-2222-2222-222222222222', 'Erie County', 'county', 
        '11111111-1111-1111-1111-111111111111', 1, true)
ON CONFLICT (id) DO NOTHING;

-- Insert City of Buffalo
INSERT INTO jurisdictions (id, name, type, parent_jurisdiction_id, level, active)
VALUES ('33333333-3333-3333-3333-333333333333', 'Buffalo', 'city',
        '22222222-2222-2222-2222-222222222222', 2, true)
ON CONFLICT (id) DO NOTHING;

-- Sample State Rule: 25% solar tax credit
INSERT INTO local_rules (id, jurisdiction_id, rule_type, rule_key, value, value_unit, applies_to, source_citation, effective_date)
VALUES ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111',
        'tax_abatement', 'solar_tax_credit', 25.0, 'percent', '["solar"]', 'NY State Tax Law §606', '2024-01-01')
ON CONFLICT (id) DO NOTHING;

-- Sample County Rule: Additional 10% (additive)
INSERT INTO local_rules (id, jurisdiction_id, rule_type, rule_key, value, value_unit, applies_to, source_citation, effective_date)
VALUES ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-2222-2222-2222-222222222222',
        'tax_abatement', 'solar_tax_credit', 10.0, 'percent', '["solar"]', 'Erie County Code §123', '2024-01-01')
ON CONFLICT (id) DO NOTHING;

-- Sample City Rule: $500 permit fee (negative)
INSERT INTO local_rules (id, jurisdiction_id, rule_type, rule_key, value, value_unit, applies_to, source_citation, effective_date)
VALUES ('cccccccc-cccc-cccc-cccc-cccccccccccc', '33333333-3333-3333-3333-333333333333',
        'permit_fee', 'solar_permit_fee', 500.0, 'USD', '["solar"]', 'Buffalo Code §456', '2024-01-01')
ON CONFLICT (id) DO NOTHING;

-- Inheritance policy: County adds to State
INSERT INTO inheritance_policies (jurisdiction_id, rule_category, inheritance_mode, valid_from)
VALUES ('22222222-2222-2222-2222-222222222222', 'incentives', 'additive', '2024-01-01')
ON CONFLICT (jurisdiction_id, rule_category) DO UPDATE 
SET inheritance_mode = EXCLUDED.inheritance_mode;

-- Inheritance policy: City fees override (stricter)
INSERT INTO inheritance_policies (jurisdiction_id, rule_category, inheritance_mode, valid_from)
VALUES ('33333333-3333-3333-3333-333333333333', 'fees', 'override', '2024-01-01')
ON CONFLICT (jurisdiction_id, rule_category) DO UPDATE 
SET inheritance_mode = EXCLUDED.inheritance_mode;

SELECT 'Test data seeded successfully!' as status;
'@

# -------------------------------------------------------------------
# Create all files
# -------------------------------------------------------------------
Write-Host "Creating Maximizer files..." -ForegroundColor Yellow
Write-Host ""

Create-File -RelativePath "maximizer.py" -Content $MaximizerPy
Create-File -RelativePath "api_maximizer.py" -Content $ApiMaximizerPy
Create-File -RelativePath "test_maximizer.py" -Content $TestMaximizerPy
Create-File -RelativePath "migrations/seed_test_data.sql" -Content $SeedTestDataSql

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All Maximizer files created successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update `$ProjectPath in this script if needed (currently: $ProjectPath)" -ForegroundColor White
Write-Host "2. Run the seed data: psql -d your_db -f migrations/seed_test_data.sql" -ForegroundColor White
Write-Host "3. Test the maximizer: python test_maximizer.py" -ForegroundColor White
Write-Host "4. Run the API: uvicorn api_maximizer:app --reload" -ForegroundColor White
Write-Host ""