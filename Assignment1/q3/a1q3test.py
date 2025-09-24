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
    """

    # contains index and suffix from that index
    temp = [(i, input_text[i:]) for i in range(len(input_text))]  # O(S) where S is the length of the input string

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
    """

    char_idx = ord(input_char) - ASCII_START # O(1) get char index

    return char_idx if input_char != ENDING_CHAR else -1 # O(1) return and check if char is ENDING_CHAR


def get_count_table(input_text: str):
    """
        Function description: This function produces a count table which contains the number of occurrences of a character before a given index

        Input:
            input_text : input text to compute count table

        Time complexity: O(S * A) where S is the length of the string and A is the alphabet size

        Time complexity analysis :

             generating return array is O(S)
             generating temp array is O(A)
             populating return array is O(S * A)
    """

    n = len(input_text)
    arr = [None] * (n + 1) # O(S) where S is the length of the string
    temp = [0] * (ASCII_END - ASCII_START + 1)  # O(A) where A is the alphabet size

    # O(S)
    # loop through text and for every character update temp position and update array for current index
    for i in range(len(input_text)):

        char_idx = get_character_idx(input_text[i]) # O(1)
        temp[char_idx] = temp[char_idx] + 1 # O(1)
        arr[i] = temp[:] #O(A)

    arr[-1] = [0] * (ASCII_END - ASCII_START + 1)   # O(1)

    return arr # O(1)

def search_for_pattern_special(bwt_text: str, suffix_array: list[int], pattern: str):
    """
        Function description: This functions returns a list of indices where the pattern occurs in a given text and
        accounts for wildcard characters (#) which can be substituted for any character

        Input:
            bwt_text: the burrow wheeler transform text used for pattern matching
            suffix_array : the suffix array of the original string
            pattern : the pattern to be matched

        Time complexity: O(S^W) where S is the length of the string (pattern),W is the number of wildcards in the pattern,
        A is the alphabet size

        Time complexity analysis :

             to sort the bwt text and use it for pattern matching is O(S * log(S))
             producing the rank table is O(S + A)
             producing the count table is O(S * A)
             finally to run the recursive pattern matching using search_for_pattern_aux is O(S^W)

             O(S^W + (S * log(S)))

    """

    # Initialize all starting values
    n = len(bwt_text)
    sp = 0
    ep = n - 1

    first = sorted(bwt_text) # O(S * log(S)) where S is the length of the string
    rank_table = get_rank_table(''.join(first)) # O(S + A) where S is the length of the string and A is the alphabet size
    k = len(pattern) - 1

    count_table = get_count_table(bwt_text) # O(S * A)

    res = [False for _ in range(n)] # O(S)
    ret = []

    def search_for_pattern_aux(k: int, sp: int, ep: int, temp_char=""):
        """
            Function description: This function recursively moves through the pattern until the pattern is completed found
            in the text being searched in or breaks. If the pattern is found all the relevant indices in the suffix array
            is turned True in the res array to the return array with all the indices

            Input:
                k: the index in the pattern that is character being checked
                sp : the starting point index in the bwt text
                ep : the ending point index in the bwt text
                temp_char : if a wildcard is met the temp_char variable will substitute the wildcard

            Time complexity: O(S^W) where S is the length of the string (pattern) and W is the number of wildcards in the pattern

            Time complexity analysis :

                 to loop through the pattern is O(S)
                 if a wildcard is met then we must create a branch for each character from sp to ep which is O(S)
                 the number of branches created could be the length of the string and the range sp to ep is worst case the length of S
                 thus the time complexity is exponential for searching the pattern

            Space complexity: O(1)

            Space complexity analysis:

                O(1) for input index k
                O(1) for input sp
                O(1) for input ep
                O(1) for temp_char
                No additional arrays or other data structures formed
        """

        # this boolean becomes True when a wild card is found in the current branch
        # if stop_add is true then disregard adding the indices of current branch but still add child branch indices
        stop_add = False

        # only run if there is a pattern left (k >= 0) or there are more characters to match (sp < ep)
        while k >= 0 and sp <= ep:

            # temp char is true if a wild card was found in the previous iteration

            if temp_char:

                # if last char was a wild chard then update it to temp char sent in branch
                char = temp_char
                # make temp_char False again so char does not get replaced with empty string
                temp_char = False
            else:

                # if we haven't met a wild card then make char the next character
                char = pattern[k]

            # if the next char we found is wild card then search for pattern for all characters from sp to ep
            if char == "#":
                for idx in range(sp, ep + 1):

                    # only run if the character is not the ENDING_CHAR
                    if bwt_text[idx] != ENDING_CHAR:
                        search_for_pattern_aux(k, sp, ep, bwt_text[idx])

                # make stop add true to disregard indices of current branch
                stop_add = True
                # this branch is no longer valid so break from loop
                break


            char_idx = get_character_idx(char) # O(1)
            sp = rank_table[char_idx] + count_table[sp - 1][char_idx]   # O(1)
            ep = rank_table[char_idx] + count_table[ep][char_idx] - 1   #O (1)

            if sp > ep:
                break

            k -= 1

        # leave current branch if stop_add is True
        if stop_add:
            return

        # else convert indices into true to add to returning list after
        for i in range(sp, ep + 1):
            res[suffix_array[i]] = True

    search_for_pattern_aux(k, sp, ep)

    # add pattern matched indices into return list and return
    for i in range(n):
        if res[i]:
            ret.append(i)

    return ret

def run_test(pat, txt):

    if len(pat) == 0 or len(txt) == 0:
        return []

    txt = txt + ENDING_CHAR
    suffix_array = compute_suffix_array(txt)
    bwt_text = get_bwt_text(suffix_array, txt)

    res = search_for_pattern_special(bwt_text, suffix_array, pat)
    return res

# def run_test(txt, pat, expected):
#     txt = txt + ENDING_CHAR
#     suffix_array = compute_suffix_array(txt)
#     bwt_text = get_bwt_text(suffix_array, txt)
#
#     res = search_for_pattern_special(bwt_text, suffix_array, pat)
#     if res == expected:
#         print(f"PASS: pat='{pat}', txt='{txt}' -> {res}")
#     else:
#         print(f"FAIL: pat='{pat}', txt='{txt}' -> got {res}, expected {expected}")


# # --- Test cases ---
#
# # 1. Exact match once
# run_test("abcde", "bcd", [2])
#
# # 2. Exact match multiple
# run_test("ababababa", "aba", [1, 3, 5, 7])
#
# # 3. No match
# run_test("abcdef", "gh", [])
#
# # 4. Wildcard at start
# run_test("xabcy", "#abc", [1])
#
# # 5. Wildcard in middle
# run_test("abcdef", "a#c", [1])
#
# # 6. Wildcard at end
# run_test("abcdef", "de#", [4])
#
# # 7. Multiple wildcards (assignment example)
# run_test("bbebabababebebababab", "be##ba#", [2, 10, 12])
#
# # 8. Pattern all wildcards
# run_test("abcdef", "###", [1, 2, 3, 4])
#
# # 9. Pattern longer than text
# run_test("abc", "abcd", [])
#
# # 10. Pattern equals text, with wildcards
# run_test("abcdef", "######", [1])
#
# # 11. Overlapping matches with wildcards
# run_test("aaaaaa", "a#a", [1, 2, 3, 4])
