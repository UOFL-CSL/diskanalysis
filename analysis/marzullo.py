#####################################
# Marzullo's Sliding Window Algorithm
# Computer Systems Laboratory
# University of Louisville
#####################################
import math
import time
import cProfile

from cache import ItemsetCache
from stream import StreamProvider
from tracer import Tracer

# Benchmarking variables
start = 0.0
end = 0.0

# Szudzik's Elegant Pairing Function
# http://szudzik.com/ElegantPairing.pdf
def pair_map(x, y):
    if x > y:
        x,y = y,x
    return (x * x + x + y) if (x >= y) else (y * y + x)


def pair_unmap(z):
    flooredRoot = math.floor(math.sqrt(z))
    condition = z - flooredRoot**2

    if condition < flooredRoot:
        return condition, flooredRoot
    else:
        return flooredRoot, condition - flooredRoot

def parse(filename, size):
    file = open(filename, "r")
    transactions = []

    # Parse all of the itemsets out, expecting space delimited integers
    count = 0
    for line in file:
        count += 1
        if count > size:
            break

        line = line.strip("\n")
        parsed_items = line.split(" ")

        # Skip transactions with only 1 item

        if len(parsed_items) == 1:
            continue

        transactions.append([int(x) for x in parsed_items])

    return transactions

# Base Apriori
def scan(filename, threshold, windowsize):
    transactions = parse(filename, windowsize)
    frequency = {}

    cache = ItemsetCache(5)

    # First pass
    for transaction in transactions:
        for item in transaction:
            if int(item) not in frequency:
                frequency[int(item)] = 1
            else:
                frequency[int(item)] += 1

    # Remove items under the threshold
    frequency = { k:v for k,v in frequency.items() if v >= threshold }

    # Create table of pairs that are frequent
    pairs = {}
    for item in frequency.keys():
        for item2 in frequency.keys():
            if item == item2:
                continue

            pairs[pair_map(item, item2)] = 1

    # Second pass
    for transaction in transactions:
        usedPairs = {}

        for item in transaction:
            if item not in frequency:
                continue

            for item2 in transaction:
                if item == item2 or item2 not in frequency:
                    continue

                mapping = pair_map(item, item2)
                if mapping in usedPairs:
                    continue

                pairs[mapping] += 1
                usedPairs[mapping] = 1

    count = 0
    for k,v in pairs.items():
        if v > 9:
            cache.add(k, v)
            i1, i2 = pair_unmap(k)
            print(str(i1) + " " + str(i2) + " " + str(v))
            count += 1

    print(count)

def marzullo_static(filename, threshold, windowsize):
    global start
    global end

    transactions = parse(filename, windowsize)

    print("Processing " + str(len(transactions)) + " transactions.")

    start = time.perf_counter()

    # Initialize our cache
    cache = ItemsetCache(300000, threshold)

    for transaction in transactions[:10000]:
        # Add all possible pairs to the cache
        for i in range(len(transaction)):
            for j in range(i+1, len(transaction)):
                cache.add(pair_map(transaction[i], transaction[j]))

    end = time.perf_counter()

    return cache

#cProfile.run('marzullo("web1m_100000.txt", 10, 100000)')
#result = marzullo("web1m_100000.txt", 10, 100000)

def marzullo_stream(threshold):
    global start
    global end

    start = time.perf_counter()

    # Initialize our cache
    cache = ItemsetCache(300000, threshold)

    trace = Tracer()

    def callback(transaction):
        # Add all possible pairs to the cache
        for i in range(len(transaction)):
            for j in range(i + 1, len(transaction)):
                cache.add(pair_map(transaction[i], transaction[j]))


    trace.start(callback)

    end = time.perf_counter()

    return cache

marzullo_stream(50)

'''
print("Frequent Items:")
for item, info in result.frequentItems.items():
    print("Item: " + str(pair_unmap(item)) + " Support: " + str(info[1]))

print("Items in main cache:")
for item, info in result.items.items():
    if info[1] >= 10:
        print("Item: " + str(pair_unmap(item)) + " Support: " + str(info[1]))

print("Elapsed time: " + str(end-start))

stream = StreamProvider()
stream.generateStreams(result)
print(stream.stream)'''