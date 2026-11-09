from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class StandardContractTests(unittest.TestCase):
    def test_yaml_standards_and_profiles_are_valid(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed; YAML syntax validation is an optional developer check")
        paths = [
            "standards/report-standard.yaml", "standards/metric-definitions.yaml",
            "standards/data-contract.yaml", "standards/quality-gates.yaml",
            "profiles/factsheet.yaml", "profiles/comparative.yaml",
            "themes/frontera-funds.yaml", "themes/neutral-institutional.yaml",
            "configuration/defaults.yaml", "compatibility/capability-requirements.yaml",
            "compatibility/execution-profiles.yaml"
        ]
        for rel in paths:
            with self.subTest(path=rel):
                self.assertIsInstance(yaml.safe_load((ROOT / rel).read_text()), dict)

    def test_standard_has_exactly_two_report_profiles(self):
        import yaml
        standard = yaml.safe_load((ROOT / "standards/report-standard.yaml").read_text())["standard"]
        self.assertEqual(standard["scope"]["report_profiles"], ["factsheet", "comparative"])
        self.assertFalse(standard["product_boundaries"]["saas_dependency"])

    def test_brand_overrides_cannot_change_methodology(self):
        config = json.loads((ROOT / "configuration/client-overrides.schema.json").read_text())
        self.assertFalse(config["additionalProperties"])
        defaults = __import__("yaml").safe_load((ROOT / "configuration/defaults.yaml").read_text())
        forbidden = defaults["configuration"]["override_policy"]["forbidden"]
        for key in ("metric_formula", "source_provenance", "required_sections", "quality_gates"):
            self.assertIn(key, forbidden)

    def test_execution_profiles_are_capability_based(self):
        import yaml
        profiles = yaml.safe_load((ROOT / "compatibility/execution-profiles.yaml").read_text())
        self.assertIn("observed_host_capabilities", profiles["execution_profiles"]["selection_policy"])
        ids = [p["id"] for p in profiles["execution_profiles"]["profiles"]]
        self.assertEqual(ids, ["orchestration", "analytical", "computational", "document", "visual_qa"])

    def test_examples_validate_against_output_schema(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema is not installed; schema validation is an optional developer check")
        schema = json.loads((ROOT / "schemas/fic-report.schema.json").read_text())
        validator = Draft202012Validator(schema)
        for rel in ("examples/factsheet-output.example.json", "examples/comparative-output.example.json"):
            with self.subTest(example=rel):
                data = json.loads((ROOT / rel).read_text())
                self.assertEqual(list(validator.iter_errors(data)), [])

if __name__ == "__main__":
    unittest.main()
