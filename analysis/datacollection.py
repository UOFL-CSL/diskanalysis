# Fio Data Parser
import json
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

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
x = 1
notrace = sum(experimentData["write_bw"][:3])/3
trace = sum(experimentData["write_bw"][3:])/3

print(notrace)
print(trace)

fig, ax = plt.subplots()
r1 = ax.bar(x - 0.35/2, notrace, 0.35, label="Tracing Disabled")
r2 = ax.bar(x + 0.35/2, trace, 0.35, label="Tracing Enabled")

ax.set_title("Bandwidth Comparison")
ax.set_xticks([1])
ax.set_xticklabels('')
ax.set_ylabel("MB/s")
ax.legend()

fig.tight_layout()
plt.savefig("bandwidth1.png")