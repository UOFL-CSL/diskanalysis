# Fio Data Parser
import json
import matplotlib as plt

# Contains the fio result outputs
experimentData = {}
experimentData["iops"] = []
experimentData["write_bw"] = []
experimentData["runtime"] = []

# LBAs that are repeated in the experiment
experimentData["lbas"] = []

# Output of the algorithm
algorithmOutput = {}

for i in range(1,11):
    output = open("results_" + str(i) + ".txt")
    parsed = json.load(output)

    writejob = parsed["jobs"][0]["write"]
    iops = writejob["iops"]
    runtime = writejob["runtime"]
    bw = writejob["bw"]
    
    experimentData["runtime"].append(runtime)
    experimentData["write_bw"].append(bw)
    experimentData["iops"].append(iops)