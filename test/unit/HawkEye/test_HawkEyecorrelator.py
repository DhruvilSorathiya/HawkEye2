# test_hawkeyecorrelator.py
import unittest

from hawkeye import HawkEyeCorrelator, HawkEyeDb


class TestHawkEyeCorrelator(unittest.TestCase):
    """
    Test HawkEyeCorrelator
    """

    def test_init_argument_dbh_invalid_type_should_raise_TypeError(self):
        invalid_types = [None, str(), list(), dict(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    HawkEyeCorrelator(invalid_type, {})

    def test_init_argument_ruleset_invalid_type_should_raise_TypeError(self):
        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    HawkEyeCorrelator(None, invalid_type)

    def test_init_argument_ruleset_invalid_rule_should_raise_SyntaxError(self):
        hedb = HawkEyeDb(self.default_options, False)

        ruleset = {"sample rule": "invalid yaml"}
        with self.assertRaises(SyntaxError):
            HawkEyeCorrelator(hedb, ruleset)

    def test_run_correlations_invalid_scan_instance_should_raise_ValueError(self):
        hedb = HawkEyeDb(self.default_options, False)

        correlator = HawkEyeCorrelator(hedb, {}, 'example scan id')
        with self.assertRaises(ValueError):
            correlator.run_correlations()

    def test_build_db_criteria_argument_matchrule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.build_db_criteria(invalid_type)

    def test_enrich_event_sources_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.enrich_event_sources(invalid_type)

    def test_enrich_event_children_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.enrich_event_children(invalid_type)

    def test_enrich_event_entities_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.enrich_event_entities(invalid_type)

    def test_process_rule_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.process_rule(invalid_type)

    def test_build_correlation_title_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.build_correlation_title(invalid_type, [])

    def test_build_correlation_title_argument_data_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), dict(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.build_correlation_title({}, invalid_type)

    def test_create_correlation_argument_rule_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.create_correlation(invalid_type, [], readonly=True)

    def test_create_correlation_argument_data_invalid_type_should_raise_TypeError(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), dict(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                with self.assertRaises(TypeError):
                    correlator.create_correlation({}, invalid_type, readonly=True)

    def test_check_ruleset_validity_should_return_bool(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        ruleset = [{"sample": "sample"}]
        self.assertIsInstance(correlator.check_ruleset_validity(ruleset), bool)

        invalid_types = [None, str(), list(), dict(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                self.assertIsInstance(correlator.check_ruleset_validity(invalid_type), bool)

    def test_check_rule_validity_invalid_rule_should_return_false(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        invalid_types = [None, str(), list(), dict(), int()]
        for invalid_type in invalid_types:
            with self.subTest(invalid_type=invalid_type):
                self.assertFalse(correlator.check_rule_validity(invalid_type))

    def test_check_rule_validity_rule_missing_mandatory_field_should_return_false(self):
        hedb = HawkEyeDb(self.default_options, False)
        correlator = HawkEyeCorrelator(hedb, {})

        rule = {
            "id": "sample",
            "collections": [],
            "headline": "sample"
        }
        self.assertFalse(correlator.check_rule_validity(rule))

        rule = {
            "id": "sample",
            "meta": "sample",
            "headline": "sample"
        }
        self.assertFalse(correlator.check_rule_validity(rule))

        rule = {
            "id": "sample",
            "meta": "sample",
            "collections": []
        }
        self.assertFalse(correlator.check_rule_validity(rule))
