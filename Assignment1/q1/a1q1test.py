import sys


# this function reads a file and return its content
def read_file(file_path: str) -> str:
    f = open(file_path, 'r')


    line = f.readlines()
    f.close()
    return line

def write_file(output_path: str, result: list[int]):
    with open(output_path, "w") as file:
        file.write("\n".join(map(str, result)))


def Z_Algorithm_final(pattern: str, text: str, Z: list[int]):

    full_txt = pattern + "$" + text
    pat_length = len(pattern)

    n = len(full_txt)
    l = 0
    r = 0

    occurrences = []

    for k in range(pat_length+1,n):

        #out of box
        if k > r:
            l = r = k
            while (r<n and (full_txt[r-l] == "#" or full_txt[r-l] == full_txt[r])):
                r+= 1

            if(r-l >= pat_length):
                occurrences.append(k-pat_length)

            Z[k] = r - l
            r -= 1


        # in box
        else:
            k1 = k - l
            if (Z[k1] + k <= r):
                Z[k] = Z[k1]
            else:
                l = r = k

                while (r < n and (full_txt[r - l] == "#" or full_txt[r - l] == full_txt[r])):
                    r += 1

                if (r - l >= pat_length):
                    occurrences.append(k - pat_length)

                Z[k] = r - l
                r -= 1

    return occurrences

def Z_Algorithm_pattern(pattern: str, Z: list):

    n = len(pattern)
    l = 0
    r = 0

    for k in range(1,n):

        #out of box
        if k > r:
            l = r = k
            while (r<n and (pattern[r] == "#" or pattern[r-l] == "#" or pattern[r-l] == pattern[r])):
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

                while (r < n and (pattern[r] == "#" or pattern[r-l-k1] == "#" or pattern[r-l-k1] == pattern[r])):
                    r += 1

                r -= 1

                Z[k] = r - k + 1
                l=k



if __name__ == '__main__':


    OUTPUT_FILE_NAME = "output a1q1.txt"

    txt = "bbebabababebebababab"
    pat = "be##ba#"

    Z = [0] * (len(txt) + len(pat) + 1)
    Z_Algorithm_pattern(pat, Z)
    res = Z_Algorithm_final(pat, txt, Z)

    print(res)
    print(Z)
    #write_file(OUTPUT_FILE_NAME, res)


    #print("\nContent of first file : ", read_file(sys.argv[1]))
    #print("\nContent of second file : ", read_file(sys.argv[2]))

    def run_test(txt, pat, expected):
        Z = [0] * (len(txt) + len(pat) + 1)
        Z_Algorithm_pattern(pat, Z)
        res = Z_Algorithm_final(pat, txt, Z)
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