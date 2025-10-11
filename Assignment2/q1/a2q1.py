import math
import random


def miller_rabin_randomized_primality(n: int, k: int) -> bool:

    s = 0
    t = n-1

    while t % 2 == 0:
        s = s+1
        t = t//2

    witnesses = []

    for _ in range(k):


        a = random.randint(2, n-2)

        while a in witnesses:
            a = random.randint(2, n - 2)


        x0 = pow(a, t, n)

        if x0 == 1:
            continue

        x_prev = x0
        x_i = x_prev

        for i in range(1,s):
            x_i = pow(x_prev, 2, n)

            if x_i == 1:
                if x_prev != n-1:
                    return False
                else:
                    break

            x_prev = x_i

        if x_i != 1:
            return False

        witnesses.append(a)

    return True

def generate_prime_number(d : int):
    if 100 <= d <= 1000:

        is_probably_prime = False

        while (not is_probably_prime):
            num = 2
            while (num % 2 == 0):

                lower = 10 ** (d - 1)
                upper = 10 ** d - 1
                num = random.randint(lower, upper)


            is_probably_prime = miller_rabin_randomized_primality(num, 4)
            feedback = "number: " + str(num) + " is prime: " + str(is_probably_prime)
            print(feedback)

        return num

    else:
        print("input not in range 100 <= d <= 1000")

print(generate_prime_number(300))






