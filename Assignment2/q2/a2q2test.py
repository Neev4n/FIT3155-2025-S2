
all_fibs = [1,2]

def produce_fib_nums(num: int):

    a = 1
    b = 2

    while b < num:

        temp = a + b
        a = b
        b = temp

        global all_fibs
        all_fibs.append(temp)

def binary_search_fib_index(num: int, l : int, r: int) -> int:

    while l <= r:

        mid = (l+r)//2

        if all_fibs[mid] == num:
            return mid

        elif all_fibs[mid] < num:
            l = mid + 1

        else:
            r = mid - 1

    return r

def produce_fib_encoding(num: int):

    fib_idx = binary_search_fib_index(num, 0, len(all_fibs) - 1)

    binary_num_lst = ["0" for _ in range(fib_idx+1)]

    total = num

    while total != 0 and fib_idx >= 0:
        total -= all_fibs[fib_idx]
        binary_num_lst[fib_idx] = "1"
        fib_idx = binary_search_fib_index(total, 0, fib_idx - 2)

    binary_num_lst.append("1")
    return ''.join(binary_num_lst)

def produce_all_fib_encodings(pos_ints : list[int]):
    max_fib = max(pos_ints)
    produce_fib_nums(max_fib)
    res = []

    for num in pos_ints:
        res.append(produce_fib_encoding(num))

    return res

print(produce_all_fib_encodings([9,2,7]))

