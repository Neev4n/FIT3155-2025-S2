
def Z_Algorithm(pattern: str, text: str):

    full_txt = pattern + "$" + text


    n = len(full_txt)
    l = 0
    r = 0
    Z = [0] * n

    for k in range(1,n):
        #out of box
        if k > r:
            l = r = k
            while (r<n and full_txt[r-l] == full_txt[r]):
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
                while (r < n and full_txt[r-l-k1] == full_txt[r]):
                    r += 1

                r -= 1
                Z[k] = r - k + 1
                l=k

    return Z




txt = "xabcabzabc"
pat = "abc"
res = Z_Algorithm(pat, txt)
print(res)