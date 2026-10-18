from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_foundry_boundary import INFRA_DIR, validate_boundary


class FoundryBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configuration = json.loads(
            (INFRA_DIR / "boundary.json").read_text(encoding="utf-8")
        )
        cls.sources = {
            path.name: path.read_text(encoding="utf-8")
            for path in INFRA_DIR.glob("*.bicep")
        }

    def test_approved_scope_and_resource_group_bicep_are_accepted(self) -> None:
        self.assertEqual(validate_boundary(self.configuration, self.sources), [])

    def test_rejects_subscription_resource_group_location_and_environment_mismatch(self) -> None:
        for key, value in (
            ("subscription_id", "00000000-0000-0000-0000-000000000000"),
            ("resource_group", "rg-production"),
            ("location", "westus"),
            ("github_environment", "production"),
        ):
            with self.subTest(key=key):
                configuration = copy.deepcopy(self.configuration)
                configuration[key] = value
                self.assertTrue(validate_boundary(configuration, self.sources))

    def test_rejects_non_resource_group_deployment_scope(self) -> None:
        configuration = copy.deepcopy(self.configuration)
        configuration["deployment_scope"] = "subscription"
        self.assertTrue(validate_boundary(configuration, self.sources))

    def test_rejects_credentials_and_role_assignments(self) -> None:
        for key, value in (
            ("credentials", ["client-secret"]),
            ("role_assignments", [{"role": "Contributor"}]),
        ):
            with self.subTest(key=key):
                configuration = copy.deepcopy(self.configuration)
                configuration[key] = value
                self.assertTrue(validate_boundary(configuration, self.sources))

    def test_rejects_unapproved_bicep_scope_and_sensitive_configuration(self) -> None:
        sources = copy.deepcopy(self.sources)
        sources["main.bicep"] += "\nresource bad 'Microsoft.Authorization/roleAssignments@2022-04-01' = {}\n"
        errors = validate_boundary(self.configuration, sources)
        self.assertTrue(any("RBAC configuration" in error for error in errors))

        sources = copy.deepcopy(self.sources)
        sources["main.bicep"] = sources["main.bicep"].replace(
            "targetScope = 'resourceGroup'", "targetScope = 'subscription'"
        )
        errors = validate_boundary(self.configuration, sources)
        self.assertTrue(any("targetScope" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
