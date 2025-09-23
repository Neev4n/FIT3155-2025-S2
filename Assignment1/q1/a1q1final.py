ASCII_START = 37
ASCII_END = 126
ENDING_CHAR = "!"

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

                l = r = k
                while (r < n and text[r-l] == text[r]):
                    r += 1

                Z[k] = r - l
                r -= 1

    return Z


def pattern_match_wildcard(pattern: str, text: str):



    pat_length = len(pattern)
    text_length = len(text)
    components = []
    component_indices = []
    curr_component = ""
    curr_index = 0
    max_start = text_length - pat_length + 1
    count = [0] * (max_start)

    if max_start < 0 or pat_length == 0 or text_length == 0:
        return []

    for char_index in range(pat_length):

        if pattern[char_index] == "#":
            if curr_component:
                components.append(curr_component)
                component_indices.append(curr_index)
                curr_component = ""

            curr_index = char_index + 1


        else:
            curr_component += pattern[char_index]

    if curr_component:
        components.append(curr_component)
        component_indices.append(curr_index)

    if not components:
        return list(range(max_start))

    num_components = len(components)


    for pat_pos, component in zip(component_indices, components):
        combined = component + ENDING_CHAR + text
        Z = z_algorithm(combined)

        for i in range(len(component), len(combined)):
            if Z[i] >= len(component):
                text_pos = i - len(component) - 1
                start_pos = text_pos - pat_pos
                if 0 <= start_pos < max_start:
                    count[start_pos] += 1

    res = [i + 1 for i in range(max_start) if count[i] == num_components]
    return res

    # print(components)
    # print(component_indices)


# if __name__ == '__main__':
#     txt = "bbebabababebebababab"
#     pat = "be##ba#"
#     print(pattern_match_wildcard(txt, pat))

# def run_test(txt, pat, expected):
#
#
#     res = pattern_match_wildcard(txt, pat)
#     if res == expected:
#         print(f"PASS: pat='{pat}', txt='{txt}' -> {res}")
#     else:
#         print(f"FAIL: pat='{pat}', txt='{txt}' -> got {res}, expected {expected}")
#
#
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



