def how_many_ways(digitarray):
    if not digitarray or digitarray[0] == '0':
        return 0
    a = [1, 1]
    for i in range(1, len(digitarray)):
        if digitarray[i] == '0':
            if (digitarray[i-1] == '1' or digitarray[i-1] == '2'):
                a.append(a[-2])
            else:
                return 0
        elif digitarray[i-1] == '1' or (digitarray[i-1] == '2' and digitarray[i] <= '6'):
            a.append(a[-1] + a[-2])
        else:
            a.append(a[-1])
    return a[-1]




digitarray = "226"
# digitarray = "10"
#
print(how_many_ways(digitarray))
