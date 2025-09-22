ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

def compute_suffix_array(input_text):
    """
        Function description: This function produces a suffix array which is a sorted array of integers that represent
        the starting positions of all suffixes of a given string in lexicographical

        Input:
            input_text : input text to compute suffix array

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            creating temp array is O(S)
            sorting temp array lexicographically is O(S) ASSUMING we use ukkonen's algorithm to produce the suffix array
            creating suffix array is O(S)

            O(S)

        Space complexity: O(S) given S is the length of the string

        Space complexity analysis:

            O(S) for input string
            O(S) for creating temp array
            O(S) for creating final suffix array to be returned

    """

    # contains index and suffix from that index
    temp = [(i, input[i:]) for i in range(len(input_text))]  # O(S) where S is the length of the input string

    temp.sort(key=lambda x: x[1])  # O(S) ASSUMING ukkonen's algorithm is used here instead

    suffix_arr = [i for i, _ in temp]   # O(S)

    return suffix_arr

def get_bwt_text(suffix_array: list[int], input_text: str):
    """
        Function description: This function produces a bwt string that is computed for every character in the suffix array
        by choosing the left adjacent character in the input string

        Input:
            suffix_array : suffix array of the input text
            input_text : text used to produce bwt text

        Time complexity: O(S) where S is the length of the true

        Time complexity analysis : Given S is the length of the string,

            bwt text is O(S)

            O(S)

        Space complexity: O(S) given S is the length of the string

        Space complexity analysis:

            O(S) for input string
            O(S) for input suffix array
            O(S) for bwt text returned

    """

    bwt_text = ""

    # O(S) where S is the length of the string
    for index in suffix_array:

        # identical to suffix array string but shifted left by one
        bwt_text += input_text[index - 1]   # O(1)

    return bwt_text

def get_rank_table(input_text: str):
    """
        Function description: This function produces a rank table which contains the index value of the first occurrence
        of a given character in the input text

        Input:
            input_text : text used to rank table

        Time complexity: O(S + A) where S is the length of the string and A is the length of the alphabet

        Time complexity analysis : Given S is the length of the string and A is the length of the alphabet,

             initializing the rank table is O(A)
             computing the values for the rank table is O(S)

             O(S + A)

        Space complexity: O(S + A) given S is the length of the string and A is the length of the alphabet

        Space complexity analysis:

            O(S) for input string
            O(A) for the rank table

            O(S + A)

        Auxiliary Space complexity : O(A)
    """

    table = [-1] * (ASCII_END - ASCII_START + 1) # O(A) where A is the length of the alphabet

    # O(S) where S is the length of the string
    for i in range(1, len(input_text)):

        char_idx = ord(input_text[i]) - ASCII_START

        # if character index has not already been updated then update else do not change
        if table[char_idx] == -1:
            table[char_idx] = i

    # initialize last index for the edge case that sp = 0
    table[-1] = 0

    return table


def get_character_idx(input_char: str):
    """
        Function description: This function returns the relevant index of a given character

        Input:
            input_char : input character to compute character index

        Time complexity: O(1)

        Time complexity analysis :

             calculating char_idx using ord() is O(1)
             checking if character is the ENDING_CHAR is O(1)

        Space complexity: O(1)

        Space complexity analysis:

            O(1) for input character
            O(1) for storing char_idx
    """

    char_idx = ord(input_char) - ASCII_START

    return char_idx if input_char != ENDING_CHAR else -1


def get_count_table(input_text: str):
    n = len(input_text)
    arr = [None] * (n + 1)
    temp = [0] * (ASCII_END - ASCII_START + 1)

    for i in range(len(input_text)):
        char_idx = get_character_idx(input_text[i])
        temp[char_idx] = temp[char_idx] + 1
        arr[i] = temp[:]

    arr[-1] = [0] * (ASCII_END - ASCII_START + 1)

    return arr


def search_for_pattern_special(bwt_text: str, suffix_array: list[int], pattern: str):
    n = len(bwt_text)

    sp = 0
    ep = n - 1

    first = sorted(bwt_text)
    rank_table = get_rank_table(''.join(first))
    k = len(pattern) - 1

    count_table = get_count_table(bwt_text)

    res = [False for _ in range(n)]
    ret = []

    def search_for_pattern_aux(k: int, sp: int, ep: int, temp_char=""):

        stop_add = False

        while k >= 0 and sp <= ep:

            if temp_char:
                char = temp_char
                temp_char = False
            else:
                char = pattern[k]

            if char == "#":
                for idx in range(sp, ep + 1):
                    if bwt_text[idx] != ENDING_CHAR:
                        search_for_pattern_aux(k, sp, ep, bwt_text[idx])

                stop_add = True
                break

            char_idx = get_character_idx(char)
            sp = rank_table[char_idx] + count_table[sp - 1][char_idx]
            ep = rank_table[char_idx] + count_table[ep][char_idx] - 1

            if sp > ep:
                break

            k -= 1

        if stop_add:
            return

        for i in range(sp, ep + 1):
            res[suffix_array[i]] = True

    search_for_pattern_aux(k, sp, ep)

    for i in range(n):
        if res[i]:
            ret.append(i + 1)

    return ret


def run_test(txt, pat, expected):
    txt = txt + ENDING_CHAR
    suffix_array = compute_suffix_array(txt)
    bwt_text = get_bwt_text(suffix_array, txt)

    res = search_for_pattern_special(bwt_text, suffix_array, pat)
    if res == expected:
        print(f"PASS: pat='{pat}', txt='{txt}' -> {res}")
    else:
        print(f"FAIL: pat='{pat}', txt='{txt}' -> got {res}, expected {expected}")


# --- Test cases ---

# 1. Exact match once
run_test("abcde", "bcd", [2])

# 2. Exact match multiple
run_test("ababababa", "aba", [1, 3, 5, 7])

# 3. No match
run_test("abcdef", "gh", [])

# 4. Wildcard at start
run_test("xabcy", "#abc", [1])

# 5. Wildcard in middle
run_test("abcdef", "a#c", [1])

# 6. Wildcard at end
run_test("abcdef", "de#", [4])

# 7. Multiple wildcards (assignment example)
run_test("bbebabababebebababab", "be##ba#", [2, 10, 12])

# 8. Pattern all wildcards
run_test("abcdef", "###", [1, 2, 3, 4])

# 9. Pattern longer than text
run_test("abc", "abcd", [])

# 10. Pattern equals text, with wildcards
run_test("abcdef", "######", [1])

# 11. Overlapping matches with wildcards
run_test("aaaaaa", "a#a", [1, 2, 3, 4])
