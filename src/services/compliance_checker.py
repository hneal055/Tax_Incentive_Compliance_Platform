from typing import Optional, Dict, Any, List, Tuple
from src.models.calculator import RequirementCheck
from src.utils.database import parse_json_field


class ComplianceChecker:
    def __init__(
        self,
        rule,
        production_budget: Optional[float] = None,
        qualifying_budget: Optional[float] = None,
        shoot_days: Optional[int] = None,
        local_hire_percentage: Optional[float] = None,
        has_promo_logo: Optional[bool] = None,
        has_cultural_test: Optional[bool] = None,
        is_relocating: Optional[bool] = None,
        jurisdiction_name: Optional[str] = None,
    ):
        self.rule = rule
        self.production_budget = production_budget
        self.qualifying_budget = qualifying_budget or production_budget
        self.shoot_days = shoot_days
        self.local_hire_percentage = local_hire_percentage
        self.has_promo_logo = has_promo_logo
        self.has_cultural_test = has_cultural_test
        self.is_relocating = is_relocating
        self.jurisdiction_name = jurisdiction_name
        self.requirements_data = parse_json_field(rule.requirements)

    def check_min_spend(self) -> Optional[RequirementCheck]:
        min_spend = self.rule.minSpend
        if not min_spend:
            return None
        if self.production_budget is None:
            return RequirementCheck(
                requirement="minimum_spend",
                description=f"Minimum spend of ${min_spend:,.0f}",
                status="unknown",
                required=True,
                requiredValue=min_spend,
                notes="Budget not provided",
            )
        meets = self.production_budget >= min_spend
        return RequirementCheck(
            requirement="minimum_spend",
            description=f"Minimum spend of ${min_spend:,.0f}",
            status="met" if meets else "not_met",
            required=True,
            userValue=self.production_budget,
            requiredValue=min_spend,
            notes=f"Budget of ${self.production_budget:,.0f} {'exceeds' if meets else 'is below'} minimum",
        )

    def check_shoot_days(self) -> Optional[RequirementCheck]:
        min_days = self.requirements_data.get("minShootDays")
        if not min_days:
            return None
        if self.shoot_days is None:
            return RequirementCheck(
                requirement="minimum_shoot_days",
                description=f"Minimum {min_days} shoot days required",
                status="unknown",
                required=True,
                requiredValue=min_days,
                notes="Shoot days not provided",
            )
        meets = self.shoot_days >= min_days
        return RequirementCheck(
            requirement="minimum_shoot_days",
            description=f"Minimum {min_days} shoot days required",
            status="met" if meets else "not_met",
            required=True,
            userValue=self.shoot_days,
            requiredValue=min_days,
            notes=f"{self.shoot_days} days scheduled",
        )

    def check_local_hiring(self) -> Optional[RequirementCheck]:
        local_keys = [
            "californiaResidents",
            "georgiaResident",
            "localHirePercentage",
            "nySpend",
            "bcResident",
            "ontarioResident",
        ]
        required_pct = None
        for key in local_keys:
            if key in self.requirements_data:
                required_pct = self.requirements_data[key]
                break
        if not required_pct:
            return None
        if self.local_hire_percentage is None:
            return RequirementCheck(
                requirement="local_hiring",
                description=f"Minimum {required_pct}% local hiring required",
                status="unknown",
                required=True,
                requiredValue=required_pct,
                notes="Local hiring percentage not provided",
            )
        meets = self.local_hire_percentage >= required_pct
        return RequirementCheck(
            requirement="local_hiring",
            description=f"Minimum {required_pct}% local hiring required",
            status="met" if meets else "not_met",
            required=True,
            userValue=self.local_hire_percentage,
            requiredValue=required_pct,
            notes=f"{self.local_hire_percentage}% local hiring planned",
        )

    def check_promo_logo(self) -> Optional[RequirementCheck]:
        if (
            "georgiaPromo" not in self.requirements_data
            and "logoInCredits" not in self.requirements_data
        ):
            return None
        if self.has_promo_logo is None:
            return RequirementCheck(
                requirement="promotional_logo",
                description="Include jurisdiction logo in credits",
                status="unknown",
                required=True,
                notes="Logo placement not confirmed",
            )
        return RequirementCheck(
            requirement="promotional_logo",
            description="Include jurisdiction logo in credits",
            status="met" if self.has_promo_logo else "not_met",
            required=True,
            userValue=self.has_promo_logo,
            notes=(
                "Logo placement confirmed"
                if self.has_promo_logo
                else "Logo not planned for credits"
            ),
        )

    def check_cultural_test(self) -> Optional[RequirementCheck]:
        if "culturalTest" not in self.requirements_data:
            return None
        if self.has_cultural_test is None:
            return RequirementCheck(
                requirement="cultural_test",
                description="Pass cultural test for content",
                status="unknown",
                required=True,
                notes="Cultural test status unknown",
            )
        return RequirementCheck(
            requirement="cultural_test",
            description="Pass cultural test for content",
            status="met" if self.has_cultural_test else "not_met",
            required=True,
            userValue=self.has_cultural_test,
            notes=(
                "Cultural test passed"
                if self.has_cultural_test
                else "Cultural test not passed"
            ),
        )

    def check_relocating(self) -> Optional[RequirementCheck]:
        relocating_req = self.requirements_data.get("relocatingProject")
        if relocating_req is None:
            return None
        if self.is_relocating is None:
            return RequirementCheck(
                requirement="relocating_production",
                description="Relocating production from another jurisdiction",
                status="unknown",
                required=True,
                requiredValue=relocating_req,
                notes="Relocation status not specified",
            )
        meets = self.is_relocating == relocating_req
        return RequirementCheck(
            requirement="relocating_production",
            description="Relocating production from another jurisdiction",
            status="met" if meets else "not_met",
            required=True,
            userValue=self.is_relocating,
            requiredValue=relocating_req,
            notes=(
                "Relocation status matches requirement"
                if meets
                else "This program requires relocating production"
            ),
        )

    def run_all_checks(self) -> Tuple[List[RequirementCheck], List[str], List[str]]:
        checks = []
        action_items = []
        warnings = []

        # Run each check
        min_spend_check = self.check_min_spend()
        if min_spend_check:
            checks.append(min_spend_check)
            if min_spend_check.status == "not_met":
                action_items.append(
                    f"❌ Increase budget to at least ${self.rule.minSpend:,.0f}"
                )
            elif min_spend_check.status == "unknown":
                action_items.append("⚠️ Provide production budget for verification")

        shoot_check = self.check_shoot_days()
        if shoot_check:
            checks.append(shoot_check)
            if shoot_check.status == "not_met":
                action_items.append(
                    f"❌ Extend shoot schedule to at least {self.requirements_data.get('minShootDays')} days"
                )
            elif shoot_check.status == "unknown":
                action_items.append("⚠️ Provide shoot schedule for verification")

        local_check = self.check_local_hiring()
        if local_check:
            checks.append(local_check)
            if local_check.status == "not_met":
                action_items.append(
                    f"❌ Increase local hiring to {local_check.requiredValue}%"
                )
            elif local_check.status == "unknown":
                action_items.append(
                    f"⚠️ Confirm {local_check.requiredValue}% local hiring commitment"
                )

        logo_check = self.check_promo_logo()
        if logo_check:
            checks.append(logo_check)
            if logo_check.status == "not_met":
                action_items.append(
                    f"❌ Add {self.jurisdiction_name} logo to end credits"
                )
            elif logo_check.status == "unknown":
                action_items.append(
                    f"⚠️ Confirm {self.jurisdiction_name} logo placement in credits"
                )

        cultural_check = self.check_cultural_test()
        if cultural_check:
            checks.append(cultural_check)
            if cultural_check.status == "not_met":
                warnings.append("⚠️ Cultural test failure may disqualify production")
            elif cultural_check.status == "unknown":
                action_items.append("⚠️ Submit cultural test application")

        relocating_check = self.check_relocating()
        if relocating_check:
            checks.append(relocating_check)
            if relocating_check.status == "not_met":
                warnings.append("❌ This program is only for relocating productions")
            elif relocating_check.status == "unknown":
                # No action item, just unknown
                pass

        # Add close‑call warning
        if self.production_budget and self.rule.minSpend:
            if self.production_budget < (self.rule.minSpend * 1.1):
                warnings.append(
                    f"⚠️ Budget is close to minimum threshold (${self.rule.minSpend:,.0f})"
                )

        return checks, action_items, warnings
