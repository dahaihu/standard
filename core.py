def func(S, A, B):
    if not any((S, A, B)):
        return True
    if A and B:
        if S[0] == A[0] and S[0] == B[0]:
            if not func(S[1:], A[1:], B):
                return func(S[1:], A, B[1:])
            return True
        elif S[0] == A[0]:
            return func(S[1:], A[1:], B)
        elif S[0] == B[0]:
            return func(S[1:], A, B[1:])
        else:
            return False
    if A:
        if S != A:
            return False
        return True
    if B:
        if S != B:
            return False
        return True

    return False

A = "chdkeold"
B = "jgkhqp"
S = "chdjkgkheqopld"

A = "aebc"
B = "axbd"
S = "axaebdbc"


A = "aac"
B = "bba"
S = "aabcab"
print(func(S, A, B))


