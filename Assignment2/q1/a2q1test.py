

def modular_exponentiation(a : int, b : int, n : int):

    # find the solution for a^b mod n

    # find binary representation of b

    binary_rep = bin(b)
    #print(binary_rep)
    len_bin = len(binary_rep)
    curr_bit_pos = 0

    def get_next_bit_pos():
        nonlocal curr_bit_pos
        curr_bit_pos += 1
        while curr_bit_pos < len_bin and binary_rep[len_bin - curr_bit_pos - 1] == "0":
            curr_bit_pos += 1

    get_next_bit_pos()
    curr = a % n
    res = 1

    for i in range(1,len_bin - 2):
        curr = (curr * curr) % n

        if binary_rep[len_bin - i - 1] == "1":
            res = (curr * res) % n

    return res

print(modular_exponentiation(7, 560, 561))

