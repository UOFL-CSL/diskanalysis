# Generates workloadgen configs
import random

# Current experimentation 
sectorOffset = 2048
lbaRange = 20971520

def generate_random_config(count, lbaRange, distribution):
    output = []

    for i in range(count):
        lba = random.randint(0, lbaRange)

        output.append(str(lba) + ";" + f"{distribution:f}")

    return output

randomLbas = generate_random_config(100, lbaRange, 0.00001)

config = open("config.txt", "w")

for l in randomLbas:
    config.write(l + "\n")

config.close()