rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
def myfunction2(word):
    rows = [set(ele) for ele in ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']]
    for row in rows:
        for w in word:
            if w not in row:
                break
        else:
            return True
    return False


def myfunction1(s):
    res = [0, 0]
    for ele in s:
        if ele == 'R':
            res[0] += 1
        elif ele == 'L':
            res[0] -= 1
        elif ele == 'U':
            res[1] += 1
        elif ele == 'D':
            res[1] -= 1
    return res
