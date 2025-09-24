ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"
def z_algorithm(input_text: str):
    """
        Function description: Creates Z array to help with matched suffix and good prefix tables

        Input:
            input_text : input text to compute Z array

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            creating Z array is O(S)
            populating Z array is O(S)

            O(S)
    """

    n = len(input_text)
    l = 0
    r = 0
    Z = [0] * n

    for k in range(1,n):
        #out of box
        if k > r:
            l = r = k
            while (r < n and input_text[r-l] == input_text[r]):
                r+= 1

            Z[k] = r - l
            r -= 1


        # in box
        else:
            k1 = k - l
            if (Z[k1] + k <= r):
                Z[k] = Z[k1]
            else:
                r += 1
                while (r < n and input_text[r-l-k1] == input_text[r]):
                    r += 1

                r -= 1
                Z[k] = r - k + 1
                l=k

    return Z

def create_good_prefix_table(pattern: str) -> list[int]:
    """
        Function description: Creates good prefix table for good prefix shifts

        Input:
            pattern : input pattern to create table from

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            populating Z array is O(S)
            creating good prefix table is O(S)
            populating good prefix table is O(S)

            O(S)
    """

    # get Z values
    Z = z_algorithm(pattern)    # O(S) where S is the length of the string

    good_prefix_table = [0] * (len(pattern) + 1)    # O(S)

    # O(S)
    # If a prefix reoccurs then store the index where it occurs at the end of the prefix in the pattern
    # scan from right to left
    for i in range(len(pattern)-1, -1, -1):
        j = Z[i] - 1    # end of prefix in the pattern
        good_prefix_table[j] = i    # store index of next occurrence of prefix at the end of prefix in the pattern

    return good_prefix_table

def create_matched_suffix_table(pattern: str)-> list[int]:
    """
        Function description: Creates a matched suffix table for matched suffix shifts

        Input:
            pattern : input pattern to create table from

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            reversing pattern O(S)
            creating Z array is O(S)
            reversing Z array is O(S)
            creating matched suffix table is O(S)
            populating matched suffix table is O(S)

            O(S)
    """
    if not len(pattern):
        return []

    m = len(pattern)


    Z = z_algorithm(pattern[::-1])  #O(S) where S is the length of the string
    Z.reverse() # O(S)
    table = [0] * m # O(S)
    table[0] = Z[0]

    for i in range(1,m):

        # if length of the suffix of the reversed string equals the length of the string at a given i
        # then the prefix must be identical to the suffix at the given i
        # update the matched prefix value of table[i]
        if Z[i] == i + 1:
            table[i] = Z[i]

        # else use previous value from i-1
        else:
            table[i] = table[i-1]

    table[-1] = m - 1
    return table

def create_bad_character_table(pattern: str) -> list[list[int]]:
    """
        Function description: Creates a bad character table to calculate bad character shifts

        Input:
            pattern : input pattern to create table from

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            reversing pattern O(S)
            creating Z array is O(S)
            reversing Z array is O(S)
            creating matched suffix table is O(S)
            populating matched suffix table is O(S)

            O(S)
    """
    assci_range = (ASCII_END - ASCII_START)
    p = len(pattern)
    arr = [[-1] * assci_range] * (p+1)
    temp = [-1] * assci_range

    for i in range(len(pattern)-1,-1,-1):
        temp[ord(pattern[i]) - ASCII_START] = i
        arr[i] = temp[:]

    return arr

def boyer_moore_algorithm(text: str, pattern: str):

    if not len(pattern) or not len(text):
        return []

    bad_char_table = create_bad_character_table(pattern)


    p = len(pattern)
    t = len(text)
    k = t - p
    res = []

    good_prefix_table = create_good_prefix_table(pattern)
    matched_suffix_table = create_matched_suffix_table(pattern)

    print_text_and_indices(text)
    print_text_and_indices(pattern)
    print_arr(good_prefix_table, "good suffix table:")
    print_arr(matched_suffix_table, "matched prefix table:")


    while k >= 0:
        k1 = 0

        while k1 < p and text[k+k1] == pattern[k1]:

            k1 += 1

        if k1 == p:
            res.append(k)
            good_shift = p - matched_suffix_table[k1 - 1]
            k = k - good_shift
            continue

        bad_char_val = bad_char_table[k1][ord(text[k+k1]) - ASCII_START]
        bad_char_shift = p if bad_char_val == -1 else max(1, bad_char_val - k1)

        good_prefix_val = good_prefix_table[k1-1]
        good_shift = p - matched_suffix_table[k1-1] if good_prefix_val == 0 else good_prefix_val

        k = k - max(good_shift, bad_char_shift)


    return res

def print_text_and_indices(text: str):

    char_str = "  ".join(text)
    print(char_str)

    print_arr(list(range(len(text))), "character indices:")

def print_arr(arr: list[int], desc: str):

    index_str = "  ".join(str(num) for num in arr)
    print(desc)
    print(index_str)


# txt = "aacababacabbcaacababacabbcabcabcabcabcacababbabb"
# pat = "acababacab"
# print_text_and_indices(pat)
#
# print(boyer_moore_algorithm(txt, pat))

def run_tests():
    cases = [
        ("abcde", "bcd", [1]),
        ("abababab", "ab", [0,2,4,6]),
        ("aaaaa", "aaa", [0,1,2]),
        ("abcdef", "gh", []),
        ("abcdef", "", []),
        ("", "abc", []),
        ("abc", "abcd", []),
        ("abcde", "abcde", [0]),
        ("aaaaaaaaaa", "aa", [0,1,2,3,4,5,6,7,8]),
        ("aaaaab", "aaab", [2]),
        #("abc$%abc$%abc", "$%", [3,8]),
        ("a"*10000, "b", []),
        ("abc"*1000, "abc", list(range(0,3000,3))),
        ("xxxxxxabcdef", "abcdef", [6]),
        ("abcdefxxxxx", "abc", [0]),
        ("abcdabcd", "cdab", [2]),
    ]

    for text, pat, expected in cases:
        result = boyer_moore_algorithm(text, pat)
        result.sort()
        assert result == expected, f"FAILED: {text}, {pat}, got {result}, expected {expected}"
    print("All test cases passed!")

run_tests()


# print(create_matched_suffix_table(pat))

# print(boyer_moore_algorithm(txt, pat))