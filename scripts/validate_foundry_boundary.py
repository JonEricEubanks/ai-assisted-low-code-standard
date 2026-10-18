from __future__ import annotations

import json
import pathlib
import re
import sys
from collections.abc import Mapping


ROOT = pathlib.Path(__file__).resolve().parents[1]
INFRA_DIR = ROOT / "infra" / "foundry-qa"
EXPECTED = {
    "subscription_id": "b8f90e47-b8ee-45f1-9442-d3b4f8fd0695",
    "resource_group": "rg-mgp-foundry-qa-dev",
    "location": "eastus2",
    "github_environment": "foundry-dev",
    "deployment_scope": "resourceGroup",
    "authentication": "OIDC",
}
EXPECTED_KEYS = {
    *EXPECTED,
    "credentials",
    "role_assignments",
    "diagnostics_workspace_name",
}
FORBIDDEN_SOURCE_PATTERNS = (
    (r"\bsubscription\s*\(", "subscription-scoped configuration"),
    (r"\bmanagementGroup\s*\(", "management-group-scoped configuration"),
    (r"\btenant\s*\(", "tenant-scoped configuration"),
    (
        r"\b(?:subscription|managementGroup|tenant)ResourceId\s*\(",
        "out-of-scope resource ID",
    ),
    (r"/(?:subscriptions|resourceGroups)/", "hard-coded Azure scope"),
    (
        r"Microsoft\.Authorization/(?:roleAssignments|roleDefinitions)",
        "RBAC configuration",
    ),
    (
        r"Microsoft\.Resources/(?:resourceGroups|deployments)",
        "out-of-scope deployment configuration",
    ),
    (
        r"\b(?:clientId|clientSecret|tenantId|password|accessKey|apiKey|secret|"
        r"servicePrincipal|credential|connectionString|accessToken)\b",
        "credential configuration",
    ),
)


def validate_boundary(
    configuration: Mapping[str, object], bicep_sources: Mapping[str, str]
) -> list[str]:
    errors: list[str] = []
    unknown_keys = set(configuration) - EXPECTED_KEYS
    missing_keys = EXPECTED_KEYS - set(configuration)
    if unknown_keys:
        errors.append(
            f"Unsupported boundary settings: {', '.join(sorted(unknown_keys))}"
        )
    if missing_keys:
        errors.append(f"Missing boundary settings: {', '.join(sorted(missing_keys))}")

    for key, expected_value in EXPECTED.items():
        actual_value = configuration.get(key)
        if actual_value != expected_value:
            errors.append(f"{key} must be {expected_value!r}, got {actual_value!r}")

    for key in ("credentials", "role_assignments"):
        if configuration.get(key) != []:
            errors.append(f"{key} must be empty")

    workspace_name = configuration.get("diagnostics_workspace_name")
    if not isinstance(workspace_name, str):
        errors.append("diagnostics_workspace_name must be a string")
    elif workspace_name and not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9-]{2,62}", workspace_name
    ):
        errors.append(
            "diagnostics_workspace_name must be a simple same-resource-group name"
        )

    main_source = bicep_sources.get("main.bicep")
    if main_source is None:
        errors.append("Missing Bicep source: main.bicep")
    else:
        target_scopes = re.findall(
            r"(?m)^\s*targetScope\s*=\s*['\"]([^'\"]+)['\"]",
            main_source,
        )
        if target_scopes != ["resourceGroup"]:
            errors.append("main.bicep must declare targetScope = 'resourceGroup'")
        location_defaults = re.findall(
            r"(?m)^\s*param\s+location\s+string\s*=\s*['\"]([^'\"]+)['\"]",
            main_source,
        )
        if location_defaults != [EXPECTED["location"]]:
            errors.append("main.bicep location default must match the approved region")

    for filename, source in bicep_sources.items():
        for pattern, description in FORBIDDEN_SOURCE_PATTERNS:
            if re.search(pattern, source, re.IGNORECASE):
                errors.append(f"{filename} contains {description}")
        location_defaults = re.findall(
            r"(?m)^\s*param location\s+string\s*=\s*['\"]([^'\"]+)['\"]",
            source,
        )
        if any(value != EXPECTED["location"] for value in location_defaults):
            errors.append(f"{filename} declares an unapproved location default")
        if re.search(r"(?m)^\s*location\s*:", source) and not re.search(
            r"(?m)^\s*location\s*:\s*location\s*$", source
        ):
            errors.append(
                f"{filename} resources must use the validated location parameter"
            )
        for scope in re.findall(r"(?m)^\s*scope\s*:\s*([^\n]+)", source):
            if scope.strip() != "foundryAccount":
                errors.append(f"{filename} contains an unapproved deployment scope")
        declared_scopes = re.findall(
            r"(?m)^\s*targetScope\s*=\s*['\"]([^'\"]+)['\"]", source
        )
        if filename != "main.bicep" and declared_scopes:
            errors.append(f"{filename} must not declare a separate deployment scope")

    return errors


def main() -> int:
    try:
        configuration = json.loads(
            (INFRA_DIR / "boundary.json").read_text(encoding="utf-8")
        )
        if not isinstance(configuration, dict):
            raise ValueError("boundary.json must contain a JSON object")
        sources = {
            path.relative_to(INFRA_DIR).as_posix(): path.read_text(
                encoding="utf-8"
            )
            for path in sorted(INFRA_DIR.rglob("*.bicep"))
        }
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"BOUNDARY VALIDATION FAILED: {error}")
        return 1

    errors = validate_boundary(configuration, sources)
    if errors:
        print("BOUNDARY VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("BOUNDARY VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
