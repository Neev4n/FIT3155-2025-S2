
def z_algorithm(text: str):

    n = len(text)
    l = 0
    r = 0
    Z = [0] * n

    for k in range(1,n):
        #out of box
        if k > r:
            l = r = k
            while (r < n and text[r-l] == text[r]):
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
                while (r < n and text[r-l-k1] == text[r]):
                    r += 1

                r -= 1
                Z[k] = r - k + 1
                l=k

    return Z

def create_good_prefix_table(pattern: str) -> list[int]:

    m = len(pattern)

    Z = z_algorithm(pattern)

    good_prefix_table = [0] * (len(pattern) + 1)

    for i in range(len(pattern)-1, -1, -1):
        j =  Z[i] - 1
        good_prefix_table[j] = i

    return good_prefix_table

def create_matched_prefix_table(pattern: str)-> list[int]:

    m = len(pattern)

    table = [0] * (m+1)

    Z = z_algorithm(pattern)

    for i in range(m-1, -1, -1):
        if Z[i] + i == m:
            table[i] = Z[i]
        else:
            table[i] = table[i+1]

    table[0] = m - 1
    return table

def create_bad_character_table(pattern: str) -> list[list[int]]:

    p = len(pattern)
    arr = [[-1] * 26] * p
    temp = [-1] * 26

    for i in range(len(pattern)-1,-1,-1):
        temp[ord(pattern[i]) - ord('a')] = i
        arr[i] = temp[:]

    return arr

def boyer_moore_algorithm(text: str, pattern: str):

    bad_char_table = create_bad_character_table(pattern)


    p = len(pattern)
    t = len(text)
    k = t - p
    res = []

    good_prefix_table = create_good_prefix_table(pattern)
    #matched_prefix_table = create_matched_prefix_table(pattern)

    #print_arr(good_suffix_table, "good suffix table:")
    #print_arr(matched_prefix_table, "matched prefix table:")


    while k >= 0:
        k1 = 0
        t1 = text[k + k1]
        p1 = pattern[k1]

        while k1 < p and text[k+k1] == pattern[k1]:


            k1 += 1

        if k1 == p:
            res.append(k)



        bad_char_val = bad_char_table[k1][ord(text[k+k1]) - ord('a')]
        bad_char_shift = p if bad_char_val == -1 else max(1, bad_char_val - k1)

        good_prefix_val = good_prefix_table[k1-1]
        #good_shift = matched_prefix_table[p - k1 - 1]+1 if good_prefix_val == -1 else good_suffix_val

        k = k - max(good_prefix_val, bad_char_shift)


    return res

def print_text_and_indices(text: str):

    char_str = "  ".join(text)
    print(char_str)

    print_arr(list(range(len(text))), "character indices:")

def print_arr(arr: list[int], desc: str):

    index_str = "  ".join(str(num) for num in arr)
    print(desc)
    print(index_str)


txt = "abaababbc"
pat = "abaaba"
print_text_and_indices(pat)

print(boyer_moore_algorithm(txt, pat))

# print(boyer_moore_algorithm(txt, pat))