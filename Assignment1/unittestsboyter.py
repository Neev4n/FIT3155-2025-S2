import unittest
import random
import string

from assignment.a1q2 import boyer_moore_algorithm


def naive_search(text, pattern):
    """Naive search for validation."""
    n, m = len(text), len(pattern)
    matches = []
    for i in range(n - m + 1):
        if text[i: i + m] == pattern:
            matches.append(i)
    return matches


class TestBoyerMoore(unittest.TestCase):
    def setUp(self):
        self.test_cases = []
        self.test_cases.extend([
            # --- Pattern immediately after a partial match ---
            ("ababc", "abc", [2]),

            # --- Pattern occurs multiple times but non-contiguous ---
            ("abxxabxxab", "ab", [0, 4, 8]),

            # --- Very long text, short repeating pattern ---
            ("a" * 10000, "aa", list(range(0, 9999))),

            # --- Pattern is entire text minus last char ---
            ("abcdef", "abcde", [0]),

            # --- Pattern overlaps with internal repetition ---
            ("abababa", "aba", [0, 2, 4]),

            # --- Pattern is multiple repetitions of itself in text ---
            ("abc" * 1000, "abc" * 2, list(range(0, 2997, 3))),

            # --- Pattern near the end of text, non-overlapping ---
            ("abcdeabcdf", "abcd", [0, 5]),

            # --- Single character pattern in middle of long text ---
            ("x" * 500 + "y" + "x" * 500, "y", [500]),

            # --- Pattern length 1 less than text, occurs in middle ---
            ("abcdefg", "bcdef", [1]),

            # --- Pattern occurs at every other character in long text ---
            ("ababababab", "ab", [0, 2, 4, 6, 8]),

            # --- Overlapping pattern at start and end ---
            ("aaabaa", "aa", [0, 1, 4]),

            # --- Random stress: pattern is last character of repeated text ---
            ("z" * 10000, "z", list(range(10000))),

            # --- Pattern longer than text (non-match) ---
            ("abc", "abcd", []),

            # --- Pattern same as text (single full match) ---
            ("pattern", "pattern", [0]),
        ])

        # Edge cases: leftward scanning, patterns starting at the beginning
        self.test_cases.extend([
            ("aaabaaa", "aa", [0, 1, 4, 5]),  # overlapping at start
            ("aaaaaaa", "a", [0, 1, 2, 3, 4, 5, 6]),
            ("aaaaaa", "aaa", [0, 1, 2, 3]),  # repeated pattern, overlaps fully
            ("aabc", "aa", [0]),  # pattern exactly at start
            ("abcabc", "ab", [0, 3]),  # pattern appears at start and later
            ("aaaaab", "aaaa", [0, 1]),  # pattern fully at start, overlapping
            ("abcd", "abc", [0]),  # simple start match
            ("xyzxyz", "xy", [0, 3]),  # repeated pattern starting at index 0
            ("ttttt", "tt", [0, 1, 2, 3]),  # all same characters, starting matches
            ("ababab", "ab", [0, 2, 4]),  # alternating pattern, first occurrence at start
            ("aaaabaaa", "aaa", [0, 1, 5]),  # overlapping pattern at start and later
        ])

        # --- 30 deterministic edge/crafted cases ---
        self.test_cases.extend([
            ("hello", "he", [0]),  # 1 match at start
            ("hello", "lo", [3]),  # 2 match at end
            ("aaaaaa", "aa", [0, 1, 2, 3, 4]),  # 3 overlapping matches
            ("abababab", "abab", [0, 2, 4]),  # 4 overlaps
            ("abcdefg", "xyz", []),  # 5 no match
            ("abc", "abcd", []),  # 6 pattern longer
            ("mississippi", "s", [2, 3, 5, 6]),  # 7 single char
            ("a", "a", [0]),  # 8 single char match
            ("a", "b", []),  # 9 single char no match
            ("abc", "", []),  # 10 empty pattern
            ("", "abc", []),  # 11 empty text
            ("", "", []),  # 12 both empty
            ("abcabcabc", "abc", [0, 3, 6]),  # 13 repeated pattern
            ("xxhelloxx", "hello", [2]),  # 14 match in middle
            ("zzzzzzzz", "zzz", list(range(0, 6))),  # 15 repeated chars
            ("pattern", "pattern", [0]),  # 16 pattern == text
            ("abcde", "abcdx", []),  # 17 almost match
            ("a" * 1000, "b", []),  # 18 long no match
            ("a" * 999 + "b", "ab", [998]),  # 19 match at end
            ("abc" * 100, "abc", list(range(0, 300, 3))),  # 20 many spaced matches
            ("overlapoverlap", "lap", [4, 11]),  # 21 overlaps
            ("banana", "ana", [1, 3]),  # 22 overlapping "ana"
            ("toot", "to", [0]),  # 23 corrected
            ("levellevel", "level", [0, 5]),  # 24 repeated palindrome
            ("abcabcab", "cab", [2, 5]),  # 25 multiple
            ("xyzxyz", "zxy", [2]),  # 26 wrap-like
            ("abcdefgh", "h", [7]),  # 27 last char
            ("abcdefgh", "a", [0]),  # 28 first char
            ("abcdefgh", "gh", [6]),  # 29 last two chars
            ("abcdefgh", "efg", [4]),  # 30 middle
        ])

        # --- 20 long/repeated crafted cases ---
        self.test_cases.extend([
            ("a" * 50, "a" * 5, list(range(0, 46))),  # 31 long repeated
            ("abababababab", "aba", [0, 2, 4, 6, 8]),  # 32 overlaps
            ("abc" * 50, "bc", list(range(1, 150, 3))),  # 33 repeated bc
            ("xyz" * 30, "z", list(range(2, 90, 3))),  # 34 last char of repeat
            ("mnop" * 25, "op", list(range(2, 100, 4))),  # 35
            ("qwerty" * 20, "ty", list(range(4, 120, 6))),  # 36
            ("z" * 100, "zzzz", list(range(0, 97))),  # 37 corrected
            ("z" * 100, "zzz", list(range(0, 98))),  # 38 corrected
            ("abcde" * 20, "cde", list(range(2, 100, 5))),  # 39
            ("abcde" * 20, "abcde", list(range(0, 100, 5))),  # 40
            ("abababababababab", "baba", [1, 3, 5, 7, 9, 11]),  # 41
            ("xyxyxyxyxy", "xyx", [0, 2, 4, 6]),  # 42
            ("xyxyxyxyxy", "yxy", [1, 3, 5, 7]),  # 43
            ("palindromemordnilap", "mordnilap", [10]),  # 44
            ("palindromemordnilap", "palindrome", [0]),  # 45
            ("abcabcabcabc", "cab", [2, 5, 8]),  # 46
            ("abcabcabcabc", "bca", [1, 4, 7]),  # 47
            ("abcabcabcabc", "abcabc", [0, 3, 6]),  # 48
            ("abcdefghij" * 10, "def", [3, 13, 23, 33, 43, 53, 63, 73, 83, 93]),  # 49
            ("abcdefghij" * 10, "ghij", [6, 16, 26, 36, 46, 56, 66, 76, 86, 96]),  # 50
        ])

        # --- 50 randomized lowercase stress tests ---
        random.seed()
        # random.seed(42)
        for _ in range(1110):
            text_len = random.randint(20, 50)
            pat_len = random.randint(1, min(3, text_len))
            text = "".join(random.choice(string.ascii_lowercase) for _ in range(text_len))
            start = random.randint(0, text_len - pat_len)
            pattern = text[start: start + pat_len]  # guaranteed match
            expected = naive_search(text, pattern)
            self.test_cases.append((text, pattern, expected))

    def test_cases(self):
        passed = 0
        total = len(self.test_cases)

        for idx, (text, pattern, expected) in enumerate(self.test_cases, 1):
            result = boyer_moore_algorithm(pattern, text)
            result.sort()
            try:
                self.assertEqual(result, [num + 1 for num in expected])
                print(f"Test {idx}: PASS")
                passed += 1
            except AssertionError:
                print(f"Test {idx}: FAIL")
                print(f"  Pattern: '{pattern}'")
                print(f"  Expected: {expected}")
                print(f"  Got:      {result}")

                # Show the actual substring(s) from the text at expected positions
                for pos in expected:
                    snippet = text[pos:pos + len(pattern)]
                    print(f"  At {pos}: '{snippet}'")

                print(f"  Full text: '{text}'")

                # 🔥 Re-run with debug enabled
                # print("\n[DEBUG TRACE START]")
                # boyer_moore_leftward_galil(text, pattern)
                # print("[DEBUG TRACE END]\n")

        print(f"\nSummary: {passed}/{total} tests passed")
        self.assertEqual(passed, total, f"{passed}/{total} tests passed")


if __name__ == "__main__":
    unittest.main(verbosity=0)