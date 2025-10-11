import sys

ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

def z_algorithm(text: str):
    """
        Function description: Creates a Z array which contains the length of the prefix matched of a given index with the text itself

        Input:
            text : input text to create Z array

        Time complexity: O(S) where S is the length of the string

        Time complexity analysis : Given S is the length of the string,

            creating Z array is O(S)
            populating Z array is O(S)

            O(S)
    """
    n = len(text)
    l = 0
    r = 0
    Z = [0] * n

    # loop left to right
    for k in range(1, n):
        # out of box
        if k > r:
            l = r = k

            # fill out current Z box
            while (r < n and text[r - l] == text[r]):
                r += 1

            # store length of Z box
            Z[k] = r - l
            r -= 1


        # in box
        else:
            k1 = k - l

            # length does not exceed Z box -> copy previous Z values
            if (Z[k1] + k <= r):
                Z[k] = Z[k1]

            # length exceeds Z box -> continue pattern matching from end of Z box
            else:

                l = r = k
                while (r < n and text[r - l] == text[r]):
                    r += 1

                # store length of Z box
                Z[k] = r - l
                r -= 1

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
    arr = [[-1] * assci_range for _ in range(p+1)]
    temp = [-1] * assci_range

    for i in range(len(pattern)-1,-1,-1):
        temp[ord(pattern[i]) - ASCII_START] = i
        arr[i] = temp[:]

    return arr

def boyer_moore_algorithm(pattern: str, text: str):

    if not len(pattern) or not len(text):
        return []

    bad_char_table = create_bad_character_table(pattern)
    good_prefix_table = create_good_prefix_table(pattern)
    matched_suffix_table = create_matched_suffix_table(pattern)

    p = len(pattern)
    t = len(text)
    k = t - p
    res = []

    while k >= 0:
        k1 = 0

        # move through the pattern left to right
        while k1 < p and text[k+k1] == pattern[k1]:
            k1 += 1

        # if k1 reaches the length of the pattern
        if k1 == p:

            # append index into res
            res.append(k+1)

            # next best shift is the previous matched-suffix shift
            good_shift = p - matched_suffix_table[k1 - 1]
            k = k - max(1,good_shift)
            continue

        # get the bad character shift
        bad_char_val = bad_char_table[k1][ord(text[k+k1]) - ASCII_START]
        if bad_char_val == -1:
            bad_char_shift = 1
        else:
            bad_char_shift = max(1, k1 - bad_char_val)

        # get the good prefix shift
        good_prefix_val = good_prefix_table[k1-1]

        # if not good prefix shift then choose the matched suffix shift
        good_shift = p - matched_suffix_table[k1-1] if good_prefix_val == 0 else good_prefix_val

        k = k - max(good_shift, bad_char_shift)

    return res

# this function reads a file and return its content
def read_file(file_path: str) -> str:
    f = open(file_path, 'r')


    line = f.readlines()
    f.close()
    return line

def write_file(output_path: str, result: list[int]):
    with open(output_path, "w") as file:
        file.write("\n".join(map(str, result)))


if __name__ == '__main__':
    print("Number of arguments passed : ", len(sys.argv))
    # this is the program name
    print("Oth argument : ", sys.argv[0])
    # first argument/file path
    # second argument/file path
    print("First argument : ", sys.argv[1])
    print("Second argument : ", sys.argv[2])

    OUTPUT_FILE_NAME = "output_a1q2.txt"

    txt = read_file(sys.argv[1])
    pat = read_file(sys.argv[2])


    res = boyer_moore_algorithm("".join(pat), "".join(txt))
    write_file(OUTPUT_FILE_NAME, res)

    print("\nContent of first file : ", read_file(sys.argv[1]))
    print("\nContent of second file : ", read_file(sys.argv[2]))
