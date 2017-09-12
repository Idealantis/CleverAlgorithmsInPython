import time
def knapsackSolverDynamicProg(items,limit):
    startTime = time.time()
    # create an array with n+1 rows and w+1 columns
    table = [[0 for w in range(limit + 1)] for j in xrange(len(items) + 1)]
    for j in xrange(1,len(items)+1):
        item, wt, val = items[j-1] # get each individual item from items list
        for w in xrange(1,limit+1):
            if wt > w: # get each value from 1 to limit and check if it is less than total weight
                table[j][w] = table[j-1][w] # make the table[j][w] value 0
            else:
                # formula t(i,j) = max(t(i-1,j),vali+t(i-1,j-wi))
                table[j][w] = max(table[j-1][w],table[j-1][w-wt] + val)
    result = []
    w = limit
    for j in range(len(items),0,-1):
        # get the last column and the last element of last column becomes the total value
        # and then check the last cols value with the prev value if not same then consider that item
        wasAdded = table[j][w] != table[j-1][w]
        if wasAdded:
            item, wt, val = items[j-1] # get the item,wt, value of picked items
            result.append(items[j-1]) # append the item to the result
            w -= wt # decrease the weight so that we can go back to the 0th row
    endTime = time.time()
    totalTime = time.strftime('%Mm %Ss',time.gmtime(endTime - startTime))
    totalWeight,totalValue = 0,0
    for item, wt, val in result:
        totalWeight  += wt # calculate the total weight and total value
        totalValue += val # calculate the total value
    if totalWeight <= limit:
        totalValue = totalValue
        totalWeight = totalWeight
    else:
        totalValue = 0
        totalWeight = 0
    # return the items,totalWeight,totalValue,totalTime tuple
    return (result,totalWeight,totalValue,totalTime)
