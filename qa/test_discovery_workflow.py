from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalize_text(text: str) -> str:
    without_markdown = re.sub(r"[`*_]", "", text.casefold())
    punctuation_normalized = without_markdown.replace("—", "-").replace("–", "-")
    return " ".join(punctuation_normalized.split())


def missing_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    normalized = normalize_text(text)
    return [marker for marker in markers if normalize_text(marker) not in normalized]


def unsafe_approval_claims(text: str) -> list[str]:
    forbidden = (
        "product owner acceptance authorizes architecture",
        "product owner acceptance authorizes build",
        "product owner acceptance approves implementation",
        "product owner acceptance authorizes release",
        "product owner sign-off authorizes release",
        "product owner approval opens architecture",
        "accepted for delivery",
    )
    normalized = " ".join(text.casefold().split())
    return [claim for claim in forbidden if claim in normalized]


DISCOVERY_TEMPLATES = {
    "templates/discovery-script.md": (
        "participants received the required notice and consented",
        "approved ai boundary",
        "approved storage/access",
        "retention, and disposal rules",
        "source timestamps or note-section locators",
        "does not authorize architecture, build, production change, or release",
    ),
    "templates/discovery-to-user-story-prompt.md": (
        "using only the supplied approved discovery sources",
        "cite every client-specific statement",
        "open questions",
        "assumptions",
        "the draft does not claim ready",
        "not authorization for architecture, build, production change, or release",
    ),
    "templates/user-story-specification.md": (
        "source register",
        "provider/participants",
        "open questions",
        "assumptions",
        "product owner acceptance",
        "not project-go, readiness, architecture, estimate, build, production-change, or release authorization",
        "all tier 1 questions are closed before a ready disposition",
    ),
    "templates/solution-intake.md": (
        "discovery package handoff",
        "facts, assumptions, and unknowns",
        "source register",
        "complexity tier",
        "risk class",
        "tier 1 questions closed",
        "architecture approval: not granted by this brief",
        "release authorization: not granted by this brief",
    ),
}

GOVERNED_SURFACES = {
    "standards/common-delivery-lifecycle.md": (
        "product owner acceptance confirms",
        "does not authorize architecture, build, production change, or release",
        "participant notice/consent",
        "sources are attributed",
        "all tier 1 intake questions closed",
        "named approvers authorize release",
    ),
    "standards/intake-and-triage.md": (
        "confirmed fact",
        "implied requirement",
        "assumption",
        "unknown",
        "author or participants",
        "participant notice/consent",
        "complexity tier",
        "risk class",
        "record product owner acceptance separately from the readiness decision",
    ),
    "skills/solution-intake/SKILL.md": (
        "confirmed fact",
        "implied requirement",
        "assumption",
        "unknown",
        "provider or participants",
        "participant notice/consent",
        "approved ai boundary",
        "ready requires both assigned risk/complexity and closure of every tier 1 question",
    ),
    "agents/delivery-orchestrator.md": (
        "product owner",
        "governed triage",
        "accountable readiness approval",
        "confirmed facts, implied requirements, assumptions, and unknowns",
        "source",
        "named human release approval",
    ),
    ".github/agents/mgp-delivery.agent.md": (
        "product owner",
        "governed triage",
        "accountable readiness approval",
        "confirmed facts, implied requirements, assumptions, and unknowns",
        "source attribution",
        "named human release approval",
    ),
    ".github/copilot-instructions.md": (
        "product owner",
        "governed triage",
        "accountable readiness approver approves the baseline",
        "confirmed facts, implied requirements, assumptions, and unknowns",
        "attribute discovery statements to their sources",
        "named human approval for release",
    ),
    "governance/power-desk-delivery-charter.md": (
        "product owner specification-accuracy validation",
        "accountable readiness approval",
        "confirmed facts, implied requirements, assumptions, and unknowns",
        "sources are attributed",
        "recording, transcription, and ai boundaries are approved",
        "release approved",
    ),
}

TRAINING_SURFACES = {
    "docs/csm-handoff-intake-flow.md": (
        "attributed transcript",
        "product owner",
        "ready, discovery, or re-scope",
        "approved ai",
        "retention",
        "not authorization to build, release, publish, change access, or make a production change",
    ),
    "docs/training-materials-plan.md": (
        "qualification → discovery interview → attributed transcript",
        "product owner specification acceptance",
        "developer triage/readiness",
        "approved ai processing boundary",
        "does not authorize build or release",
    ),
    "docs/training-video-roadmap.md": (
        "qualification, discovery interview, attributed transcript",
        "product owner specification acceptance",
        "developer triage/readiness",
        "approved ai boundary",
        "is not build or release approval",
    ),
    "docs/training/index.html": (
        "trace transcript to specification",
        "product owner acceptance",
        "ready, discovery, or re-scope",
        "approved ai processing boundary",
        "readiness and architecture remain separate gates",
    ),
    "blog/article-02-delivery-lifecycle.md": (
        "discovery interview",
        "attributed transcript",
        "product owner acceptance",
        "developer triage",
        "approved ai processing boundary",
        "does not authorize build or release",
    ),
    "skills/solution-intake/examples/worked-example-inspection-workflow.md": (
        "confirmed facts",
        "implied requirements",
        "assumptions",
        "unknowns",
        "src-01",
        "us-001-ac-01",
        "disposition",
    ),
}


class DiscoveryWorkflowTests(unittest.TestCase):
    def assert_markers(self, relative: str, markers: tuple[str, ...]) -> None:
        missing = missing_markers(read(relative), markers)
        self.assertEqual([], missing, f"{relative} missing controls: {missing}")

    def test_each_required_discovery_template_exists(self) -> None:
        for relative in DISCOVERY_TEMPLATES:
            with self.subTest(file=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_each_discovery_template_has_its_required_controls(self) -> None:
        for relative, markers in DISCOVERY_TEMPLATES.items():
            with self.subTest(file=relative):
                self.assert_markers(relative, markers)

    def test_each_governed_surface_has_its_required_controls(self) -> None:
        for relative, markers in GOVERNED_SURFACES.items():
            with self.subTest(file=relative):
                self.assert_markers(relative, markers)

    def test_each_training_surface_teaches_its_required_controls(self) -> None:
        for relative, markers in TRAINING_SURFACES.items():
            with self.subTest(file=relative):
                self.assert_markers(relative, markers)

    def test_readme_links_every_discovery_template(self) -> None:
        readme = read("README.md")
        for relative in DISCOVERY_TEMPLATES:
            if relative == "templates/solution-intake.md":
                continue
            with self.subTest(file=relative):
                self.assertIn(f"({relative})", readme)

    def test_training_page_links_every_discovery_template(self) -> None:
        training = read("docs/training/index.html")
        for template in (
            "discovery-script.md",
            "discovery-to-user-story-prompt.md",
            "user-story-specification.md",
        ):
            with self.subTest(template=template):
                encoded = f"templates%2F{template}"
                self.assertIn(encoded, training)

    def test_no_governed_surface_contains_unsafe_approval_claims(self) -> None:
        for relative in (*GOVERNED_SURFACES, *TRAINING_SURFACES, *DISCOVERY_TEMPLATES):
            with self.subTest(file=relative):
                self.assertEqual([], unsafe_approval_claims(read(relative)))

    def test_requirements_and_completed_plan_are_synchronized(self) -> None:
        requirements = read("requirements.md")
        plan = read("plan.md")
        self.assertIn("REQ-015", requirements)
        self.assertIn("Plan 2.3 - Integrate governed discovery (REQ-015)", plan)
        for completed in (
            "[x] Publish repository-native discovery script",
            "[x] Refresh `skills/solution-intake/SKILL.md`",
            "[x] Update onboarding, training materials",
            "[x] Add examples showing how a discovery transcript",
            "[x] T018A",
            "[x] T018B",
        ):
            with self.subTest(plan_item=completed):
                self.assertIn(completed, plan)

    def test_negative_missing_control_detection_checks_every_profile(self) -> None:
        profiles = {**DISCOVERY_TEMPLATES, **GOVERNED_SURFACES, **TRAINING_SURFACES}
        for relative, markers in profiles.items():
            original = normalize_text(read(relative))
            for marker in markers:
                with self.subTest(file=relative, removed=marker):
                    mutated = original.replace(normalize_text(marker), "")
                    self.assertIn(marker, missing_markers(mutated, markers))

    def test_negative_unsafe_approval_claims_are_rejected(self) -> None:
        unsafe_examples = (
            "Product Owner acceptance authorizes architecture.",
            "Product Owner acceptance approves implementation.",
            "Product Owner sign-off authorizes release.",
            "The document is accepted for delivery.",
        )
        for example in unsafe_examples:
            with self.subTest(example=example):
                self.assertTrue(unsafe_approval_claims(example))

    def test_safe_approval_distinction_is_not_rejected(self) -> None:
        safe = (
            "Product Owner acceptance confirms specification accuracy only; "
            "it does not authorize architecture, build, production change, or release."
        )
        self.assertEqual([], unsafe_approval_claims(safe))

    def test_source_attribution_requires_participant_and_locator_fields(self) -> None:
        specification = read("templates/user-story-specification.md")
        for required in ("Provider/participants:", "Locator method:", "Source ID:", "Source:"):
            with self.subTest(field=required):
                self.assertIn(required, specification)

    def test_discovery_capture_requires_all_boundary_controls(self) -> None:
        script = read("templates/discovery-script.md")
        for required in (
            "notice and consented",
            "Data classification",
            "approved AI boundary",
            "storage/access",
            "retention",
            "disposal",
        ):
            with self.subTest(control=required):
                self.assertIn(required, script)

    def test_repo_self_validation_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_repo.py")],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(
            0,
            result.returncode,
            f"Repository validation failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
