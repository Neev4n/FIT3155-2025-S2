def compute_suffix_array(input_text, len_text):
    # Array of structures to store rotations and their indexes
    suff = [(i, input_text[i:]) for i in range(len_text)]
    # Sorts rotations using comparison function defined above
    suff.sort(key=lambda x: x[1])
    # Stores the indexes of sorted rotations
    suffix_arr = [i for i, _ in suff]
    # Returns the computed suffix array
    return suffix_arr

def get_last_character(suffix_array: list[int], input_text: str):

    lst = []
    for index in suffix_array:
        lst.append(input_text[index-1])

    return lst

def get_rank_table(input_text: str):

    table = [-1] * 27

    for i in range(1,len(input_text)):

        idx = ord(input_text[i]) - ord('a')

        if table[idx] == -1:
            table[idx] = i

    table[-1] = 0

    return table

def get_character_idx(char: str):
    char_idx = ord(char) - ord('a')

    return char_idx if char != "$" else -1

def get_count_table(input_text: str):

    n = len(input_text)
    arr = [None] * n
    temp = [0] * 27

    for i in range(len(input_text)):

        char_idx = get_character_idx(input_text[i])
        temp[char_idx] = temp[char_idx] + 1
        arr[i] = temp[:]

    return arr

def inverse_bwt(bwt_text : str, suffix_array: list[int]):

    first = sorted(bwt_text)
    rank_table = get_rank_table(''.join(first))
    pos = 0
    res = "$" + bwt_text[pos]

    count_table = get_count_table(bwt_text)

    while len(res) < len(bwt_text):
        char = res[-1]
        num_occ = count_table[pos][ord(char) - ord('a')]
        pos = rank_table[ord(char) - ord('a')] + num_occ
        add = bwt_text[pos]
        res += add

    return res[::-1]

def search_for_pattern(bwt_text : str, suffix_array: list[int], pattern: str):

    n = len(bwt_text)

    sp = 1
    ep = n-1

    first = sorted(bwt_text)
    rank_table = get_rank_table(''.join(first))
    k = len(pattern) - 1

    count_table = get_count_table(bwt_text)

    while k >= 0 and sp <= ep:

        char = pattern[k]
        char_idx = get_character_idx(char)
        sp = rank_table[char_idx] + count_table[sp - 1][char_idx]
        ep = rank_table[char_idx] + count_table[ep][char_idx] - 1

        if sp > ep:
            return []


        k -= 1

    return suffix_array[sp:ep+1]

text = "googol$"
pattern = "gogo"
suffix_array = compute_suffix_array(text, len(text))
bwt_text = ''.join(get_last_character(suffix_array,text))


# print(inverse_bwt(bwt_text, suffix_array))

print(search_for_pattern(bwt_text, suffix_array, pattern))