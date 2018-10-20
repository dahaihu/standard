def func(value):
    res = 0
    carry = 1 if value >= 0 else -1
    value = value if value >= 0 else -value
    while value:
        value, yu = divmod(value, 10)
        res = res * 10 + yu
    return res if carry >= 0 else -res


print(func(-2132))
