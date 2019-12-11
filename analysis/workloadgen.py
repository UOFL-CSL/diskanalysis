# Generates workloadgen configs
import random

# Current experimentation 
sectorOffset = 2048
lbaRange = 20971520

def generate_random_config(count, lbaRange, distribution):
    output = []

    for i in range(count):
        lba = random.randint(0, lbaRange)

        output.append(str(lba) + ";" + str(distribution))

    return output

randomLbas = generate_random_config(100, lbaRange, 0.01)

for l in randomLbas:
    print(l)