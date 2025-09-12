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

def Z_Algorithm(pattern: str, text: str):

    full_txt = pattern + "$" + text
    pat_length = len(pattern)

    n = len(full_txt)
    l = 0
    r = 0
    Z = [0] * n

    occurrences = []

    for k in range(1,n):
        #out of box
        if k > r:
            l = r = k
            while (r<n and (full_txt[r] == "#" or full_txt[r-l] == full_txt[r])):
                r+= 1

            if(r-l >= pat_length):
                occurrences.append(k)

            Z[k] = r - l
            r -= 1


        # in box
        else:
            k1 = k - l
            if (Z[k1] + k <= r):
                Z[k] = Z[k1]
            else:
                r += 1

                while (r < n and (full_txt[r] == "#" or full_txt[r-l-k1] == full_txt[r] )):
                    r += 1

                r -= 1

                if (r - l + 1 >= pat_length):
                    occurrences.append(k)

                Z[k] = r - k + 1
                l=k

    return occurrences



if __name__ == '__main__':
    print("Number of arguments passed : ", len(sys.argv))
    # this is the program name
    print("Oth argument : ", sys.argv[0])
    # first argument/file path
    # second argument/file path
    print("First argument : ", sys.argv[1])
    print("Second argument : ", sys.argv[2])

    OUTPUT_FILE_NAME = "output a1q1.txt"

    txt = read_file(sys.argv[1])
    pat = read_file(sys.argv[2])

    res = Z_Algorithm(pat, txt)
    write_file(OUTPUT_FILE_NAME, res)

    #print("\nContent of first file : ", read_file(sys.argv[1]))
    #print("\nContent of second file : ", read_file(sys.argv[2]))