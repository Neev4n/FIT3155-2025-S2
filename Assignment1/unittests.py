import unittest
import sys
import os

# Import your functions - adjust based on your module name
from q3 import a1q3test


class TestWildcardPatternMatching(unittest.TestCase):
    """Comprehensive test suite for wildcard pattern matching using Z-algorithm."""

    def setUp(self):
        """Set up common test data."""
        self.default_wildcard = '#'

    # ============================================================================

    # BASIC FUNCTIONALITY TESTS
    # ============================================================================

    def test_exact_match_no_wildcards(self):
        self.assertEqual(a1q3test.run_test("abc", "abcdefabc"), [0, 6])
        self.assertEqual(a1q3test.run_test("test", "testing test"), [0, 8])
        self.assertEqual(a1q3test.run_test("a", "aaaa"), [0, 1, 2, 3])

    def test_no_matches(self):
        self.assertEqual(a1q3test.run_test("xyz", "abcdef"), [])
        self.assertEqual(a1q3test.run_test("abc", "def"), [])
        self.assertEqual(a1q3test.run_test("long", "short"), [])

    def test_single_character_patterns(self):
        self.assertEqual(a1q3test.run_test("a", "banana"), [1, 3, 5])
        self.assertEqual(a1q3test.run_test("z", "banana"), [])
        self.assertEqual(a1q3test.run_test("#", "abc"), [0, 1, 2])

    # ============================================================================

    # EDGE CASES
    # ============================================================================

    def test_empty_strings(self):
        self.assertEqual(a1q3test.run_test("", "abc"), [])
        self.assertEqual(a1q3test.run_test("abc", ""), [])
        self.assertEqual(a1q3test.run_test("", ""), [])

    def test_pattern_longer_than_text(self):
        self.assertEqual(a1q3test.run_test("abcdef", "abc"), [])
        self.assertEqual(a1q3test.run_test("test", "te"), [])

    def test_pattern_equals_text(self):
        self.assertEqual(a1q3test.run_test("abc", "abc"), [0])
        self.assertEqual(a1q3test.run_test("test", "test"), [0])

    def test_single_character_text(self):
        self.assertEqual(a1q3test.run_test("a", "a"), [0])
        self.assertEqual(a1q3test.run_test("a", "b"), [])
        self.assertEqual(a1q3test.run_test("#", "x"), [0])

    # ============================================================================

    # WILDCARD-SPECIFIC TESTS
    # ============================================================================

    def test_original_problem_case(self):
        txt = "bbebabababebebababab"
        pat = "be##ba#"
        self.assertEqual(a1q3test.run_test(pat, txt), [1, 9, 11])

    def test_all_wildcards(self):
        self.assertEqual(a1q3test.run_test("###", "abcdef"), [0, 1, 2, 3])
        self.assertEqual(a1q3test.run_test("#", "xyz"), [0, 1, 2])

    def test_wildcards_at_different_positions(self):
        self.assertEqual(a1q3test.run_test("#bc", "abcxbc"), [0, 3])
        self.assertEqual(a1q3test.run_test("ab#", "abcabx"), [0, 3])
        self.assertEqual(a1q3test.run_test("a#c", "abcaxc"), [0, 3])

    def test_multiple_wildcards(self):
        self.assertEqual(a1q3test.run_test("a##d", "abcdaxyd"), [0, 4])
        self.assertEqual(a1q3test.run_test("#a#a#", "babababab"), [0, 2, 4])

    def test_consecutive_wildcards(self):
        self.assertEqual(a1q3test.run_test("a##b", "axxbayybazzb"), [0, 4, 8])
        self.assertEqual(a1q3test.run_test("###", "abcdef"), [0, 1, 2, 3])

    # ============================================================================

    # ALGORITHM PATH COVERAGE TESTS
    # ============================================================================

    def test_case_1_outside_z_box(self):
        result = a1q3test.run_test("a#a", "axabxaxya")
        self.assertEqual(result, [0])

    def test_case_2a_inside_z_box_short(self):
        result = a1q3test.run_test("#bc#bc", "abcxbcabcxbc")
        self.assertEqual(result, [0, 3, 6])

    def test_case_2b_inside_z_box_extend(self):
        txt = "abcabcabcabc"
        pat = "#bc#bc"
        result = a1q3test.run_test(pat, txt)
        self.assertEqual(result, [0, 3, 6])

    # ============================================================================

    # OVERLAPPING MATCHES
    # ============================================================================

    def test_overlapping_matches_with_wildcards(self):
        self.assertEqual(a1q3test.run_test("a#a", "aaaa"), [0, 1])
        self.assertEqual(a1q3test.run_test("#a#", "ababa"), [1])

    def test_complex_overlapping_pattern(self):
        txt = "ababababab"
        pat = "#b#b"
        result = a1q3test.run_test(pat, txt)
        self.assertEqual(result, [0, 2, 4, 6])

    # ============================================================================

    # STRESS TESTS AND PERFORMANCE EDGE CASES
    # ============================================================================

    def test_repeated_pattern_with_wildcards(self):
        txt = "abcabcabcabc" * 5
        pat = "#bc"
        expected = list(range(0, len(txt), 3))
        result = a1q3test.run_test(pat, txt)
        self.assertEqual(result, expected)

    def test_long_pattern_no_match(self):
        txt = "a" * 100
        pat = "a" * 50 + "b"
        self.assertEqual(a1q3test.run_test(pat, txt), [])

    def test_worst_case_scenario(self):
        txt = "a" * 100
        pat = "a" * 10
        expected = list(range(91))
        result = a1q3test.run_test(pat, txt)
        self.assertEqual(result, expected)

    # ============================================================================

    # DIFFERENT WILDCARD CHARACTERS
    # ============================================================================

    # ============================================================================

    # BOUNDARY CONDITIONS
    # ============================================================================

    def test_pattern_at_text_boundaries(self):
        self.assertEqual(a1q3test.run_test("#bc", "abc"), [0])
        self.assertEqual(a1q3test.run_test("c#e", "abcde"), [2])
        txt = "abcdefabc"
        pat = "#bc"
        self.assertEqual(a1q3test.run_test(pat, txt), [0, 6])

    def test_off_by_one_scenarios(self):
        self.assertEqual(a1q3test.run_test("a#c", "abc"), [0])
        self.assertEqual(a1q3test.run_test("a#", "abc"), [0])
        self.assertEqual(a1q3test.run_test("a#c", "ab"), [])

    # ============================================================================

    # SPECIAL PATTERNS
    # ============================================================================

    def test_palindromic_patterns(self):
        self.assertEqual(a1q3test.run_test("a#a", "abaacadae"), [0, 3, 5])
        self.assertEqual(a1q3test.run_test("#b#", "abacaba"), [0, 4])

    def test_repetitive_patterns(self):
        txt = "aabaabaabaab"
        pat = "##b"
        result = a1q3test.run_test(pat, txt)
        self.assertEqual(result, [0, 3, 6, 9])

    # ============================================================================

    # CORRECTNESS VERIFICATION
    # ============================================================================

    def test_match_verification(self):
        test_cases = [
            ("be##ba#", "bbebabababebebababab", [1, 9, 11]),
            ("a#c", "abcaxcaycazc", [0, 3, 6, 9]),
            ("#a#a#", "babababab", [0, 2, 4]),
        ]

        for pat, txt, expected in test_cases:
            result = a1q3test.run_test(pat, txt)
            self.assertEqual(result, expected)

            for pos in result:
                for i in range(len(pat)):
                    if pat[i] != '#':
                        self.assertEqual(pat[i], txt[pos + i],
                                         f"Mismatch at pattern pos {i}, text pos {pos + i}")


if __name__ == '__main__':
    unittest.main(verbosity=2)