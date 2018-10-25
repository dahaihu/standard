a, b = input(), input()
lines = b.strip().split(' ')
mark = {'skr', 'm4a1', 'ak'}
count = 0
for line in lines:
    if ''.join(line) in mark:
        count += 1
print(count)
