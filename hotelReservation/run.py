import subprocess
import os
import random
import time
import numpy as np
import json

NUM_THREADS = str(4)
NUM_CONNECTIONS = str(20)
DURATIONS = str(15)
REQUESTS_PER_SECOND = 100
RUNS = 3
SLEEP_DURATION = 1


def gen_rand():
    return round(random.uniform(0, 1), 3)

def run_benchmark():
    
    # Normalize Values
    normalized_arr = np.random.rand(4,1)
    normalized_arr = normalized_arr/normalized_arr.sum(axis=0,keepdims=1)


    # os.environ["SEARCH_RATIO"] = str(round(normalized_arr[0][0], 3))
    # os.environ["RECOMMEND_RATIO"] = str(round(normalized_arr[1][0], 3))
    # os.environ["USER_RATIO"] = str(round(normalized_arr[2][0], 3))
    # os.environ["RESERVE_RATIO"] = str(round(normalized_arr[3][0], 3))

    os.environ["SEARCH_RATIO"] = str(0)
    os.environ["RECOMMEND_RATIO"] = str(0)
    os.environ["USER_RATIO"] = str(0)
    os.environ["RESERVE_RATIO"] = str(1)

    cmd = ["./wrk2/wrk", 
                    "-D", 
                    "exp",
                    "-t",
                    NUM_THREADS,
                    "-c", 
                    NUM_CONNECTIONS,
                    "-d", 
                    DURATIONS, 
                    "-L", 
                    "-s", 
                    "./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
                    "http://0.0.0.0:5000", 
                    "-R", 
                    str(REQUESTS_PER_SECOND)]
    res = subprocess.check_output(cmd).decode("utf-8")

    # Delete Env when finished
    del os.environ["SEARCH_RATIO"]
    del os.environ["RECOMMEND_RATIO"]
    del os.environ["USER_RATIO"]
    del os.environ["RESERVE_RATIO"]

    return res

def parse_results(output):
    lines = output.splitlines()
    i = 0

    # skip to latency distribution
    while lines[i].strip() != 'Latency Distribution (HdrHistogram - Recorded Latency)':
        i += 1
    latency_map = {}
    for _ in range(8):
        i += 1
        words = lines[i].split()
        print("Words: " + words[0])
        latency_map[words[0]] = words[1]

    print("Val: " + latency_map["50.000%"])
    return latency_map["50.000%"]

def main():
    results = {}
    for _ in range(RUNS):
        global REQUESTS_PER_SECOND
        print(REQUESTS_PER_SECOND)
        res = run_benchmark()
        results[REQUESTS_PER_SECOND] = parse_results(res)
        time.sleep(SLEEP_DURATION)
        REQUESTS_PER_SECOND += 1000
    
    with open("data.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()


