def createLoserTree(loserTree, dataArray, n):
    '''Initialize the loser tree and data array by the branch number n.
     Assign all members of the loser tree and the data array.
     And adjust the to a real 'Loser Tree'.'''
    for i in range(n):
        loserTree.append(0)
        dataArray.append(i - n)

    for i in range(n):
        adjust(loserTree, dataArray, n, n - 1 - i)


# Unlike the HeapSort, the LoserTree adjust from bottom to top.
def adjust(loserTree, dataArray, n, s):
    t = (s + n) / 2
    while t > 0:
        if dataArray[s] > dataArray[loserTree[t]]:
            s, loserTree[t] = loserTree[t], s
        t /= 2
