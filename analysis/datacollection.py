# Fio Data Parser
import json
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path

plt.style.use("seaborn")

# Results directory
rDir = "../results/"

# Contains the fio result outputs
experimentData = {}
experimentData["iops"] = []
experimentData["write_bw"] = []
experimentData["runtime"] = []

# LBAs that are repeated in the experiment
experimentData["lbas"] = []

# Experiment Names
exps = ["random_4k_1m_notrace", "random_4k_1m_trace"]

# Output of the algorithm
algorithmOutput = {}

for exp in exps:
    for i in range(1,4):
        output = open("../results/" + exp + "_" + str(i) + ".txt")
        parsed = json.load(output)

        writejob = parsed["jobs"][0]["write"]
        iops = writejob["iops"]
        runtime = writejob["runtime"]
        bw = writejob["bw"]
        
        experimentData["runtime"].append(runtime)
        experimentData["write_bw"].append(bw)
        experimentData["iops"].append(iops)

print(experimentData["write_bw"])

# Bandwidth plots
x = np.arange(2)
notrace = [sum(experimentData["write_bw"][:3])/3]
trace = [sum(experimentData["write_bw"][3:])/3]

notrace.append(sum(experimentData["iops"][:3])/3)
trace.append(sum(experimentData["iops"][3:])/3)

print(notrace)
print(trace)

fig, ax = plt.subplots()
r1 = ax.bar(x - 0.35/2, notrace, 0.35, label="Tracing Disabled")
r2 = ax.bar(x + 0.35/2, trace, 0.35, label="Tracing Enabled")

ax.set_title("Tracing Performance")
ax.set_xticks(x)
ax.set_xticklabels(['Bandwidth (MB/s)', 'IOPS'])
ax.legend()

fig.tight_layout()
plt.savefig("bandwidth1.png")

# Accuracy plots

# Default parameters:
# MinSup = 30 for w1 w2
# MinSup = 10 for w3

experiments = ["workload1", "workload2", "workload3", "workload3ms5"]
#cacheSizes = ["10k", "50k", "100k"]
cacheSizes = ["10k", "50k", "100k", "250k"]
offset = 2048

for exp in experiments:
    print(exp)
    workload_config = open(rDir + exp + "_config.txt", "r")

    expectedLbas = {}

    for line in workload_config:
        split = line.split(";")

        if len(split) <= 1:
            continue

        lba = int(split[0])+offset

        expectedLbas[str(lba) + " " + str(lba+1)] = 1

    workload_config.close()

    x = []
    y = []

    for size in cacheSizes:
        print(size)
        hits = 0
        filename = rDir + exp + "_output_" + size + ".txt"

        if not path.exists(filename):
            continue

        results = open(filename, "r")
        for line in results:
            if line.strip('\n') in expectedLbas:
                hits += 1
        results.close()

        print(hits/len(expectedLbas.keys()))

        x.append(size)
        y.append(hits/len(expectedLbas.keys()))

    plt.figure()
    plt.plot(x, y, linestyle="--", marker="o")
    plt.ylim(0, 1.05)
    plt.title(exp)
    plt.ylabel("Accuracy")
    plt.xlabel("ARC Main Cache Size")
    plt.savefig(exp + ".png")