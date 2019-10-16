#####################################
# Naive Sliding Window Algorithm
# Computer Systems Laboratory
# University of Louisville
#####################################
import math

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


def naive(filename):
    file = open(filename, "r")

    pairs = {}

    # Parse all of the itemsets out, space delimited integers
    for line in file:
        line = line.strip("\n")
        items = line.split(" ")

        # Skip transactions with only 1 item

        if len(items) == 1:
            continue

        # Add every pair to our hash table (N^2 pairs)
        # Increment the count for each occurrence
        for item in items:
            for item2 in items:
                if item == item2:
                    continue

                pair = pair_map(int(item), int(item2))

                if pair not in pairs:
                    pairs[pair] = 1
                else:
                    pairs[pair] += 1

    return pairs


result = naive("web1m_100000.txt")

count = 0
for k, v in result.items():
    if v > 10:
        print(str(pair_unmap(k)) + " " + str(v))
        count += 1

print(count)


