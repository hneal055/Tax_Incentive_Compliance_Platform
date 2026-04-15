def maximize_incentives(project_address, project_type, project_size):
    # 1. Resolve all applicable jurisdictions (state → county → city/town)
    jurisdictions = resolve_jurisdiction_layers(project_address)

    # 2. Fetch all active local_rules for those jurisdictions
    rules = fetch_applicable_rules(jurisdictions, project_type, project_size)

    # 3. Apply inheritance policy logic (additive, override, etc.)
    net_incentives = apply_inheritance_policies(rules)

    # 4. Return maximized value + recommendation
    return {
        "max_net_credit": net_incentives["total"],
        "best_jurisdiction_layer": net_incentives["primary_contributor"],
        "warnings": net_incentives["conflicts"],
        "alternative_adjacent_jurisdictions": suggest_nearby_alternatives(
            project_address
        ),
    }
