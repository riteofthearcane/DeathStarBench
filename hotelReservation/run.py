import subprocess
import os
import random
import time
import numpy as np
import json
import matplotlib.pyplot as plt

NUM_THREADS = str(5)
NUM_CONNECTIONS_PER_THREAD = str(500)
DURATIONS = str(40)
RUNS = 3
MAX_THROUGHPUT = str(50000) # Gigantic number that we know we won't surpass
SLEEP_DURATION = 1


def gen_rand():
    return round(random.uniform(0, 1), 3)

def parse_time(time_str):
    s = 0
    while not time_str[s].isalpha():
        s += 1
    digits = time_str[:s]
    unit = time_str[s:]
    num_val = float(digits)
    mult = 1.0
    # microsecond
    if unit == "us":
        mult = 1e-6
    # millisecond
    elif unit == "ms":
        mult = 1e-3
    # second
    elif unit == "s":
        mult = 1.0
    else:
        raise ValueError("Unknown unit in: " + time_str)
    return num_val * mult

def run_benchmark(search_ratio, recommend_ratio, user_ratio, reserve_ratio, num_threads, num_connections, duration, max_throughput):
    
    # Normalize Values
    # normalized_arr = np.random.rand(4,1)
    # normalized_arr = normalized_arr/normalized_arr.sum(axis=0,keepdims=1)


    # os.environ["SEARCH_RATIO"] = str(round(normalized_arr[0][0], 3))
    # os.environ["RECOMMEND_RATIO"] = str(round(normalized_arr[1][0], 3))
    # os.environ["USER_RATIO"] = str(round(normalized_arr[2][0], 3))
    # os.environ["RESERVE_RATIO"] = str(round(normalized_arr[3][0], 3))

    os.environ["SEARCH_RATIO"] = str(search_ratio)
    os.environ["RECOMMEND_RATIO"] = str(recommend_ratio)
    os.environ["USER_RATIO"] = str(user_ratio)
    os.environ["RESERVE_RATIO"] = str(reserve_ratio)

    cmd = ["./wrk2/wrk", 
                    "-D", 
                    "exp",
                    "-t",
                    num_threads,
                    "-c", 
                    num_connections,
                    "-d", 
                    duration, 
                    "-L", 
                    "-s", 
                    "./wrk2/scripts/hotel-reservation/mixed-workload_type_1.lua",
                    "http://0.0.0.0:5000", 
                    "-R", 
                    max_throughput]
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
        # print("Words: " + words[0])
        latency_map[words[0]] = words[1]

    return latency_map

def make_chart(data):
    x = list(data.keys())
    y = list(data.values())
    
    plt.plot(x, y)
    plt.xlabel("Requests per second")
    plt.ylabel("Latency (s)")
    plt.savefig('chart4.png')

def main():
    results = {}
    for num_connections in range(500, 1500, 500): # i in range(0,RUNS,1): # 
        res = run_benchmark(0, 0, 0, 1, NUM_THREADS, str(num_connections), DURATIONS, MAX_THROUGHPUT)
        print(res)
        print("\n\n\n")
        median_str = parse_results(res)["50.000%"]
        median = parse_time(median_str)
        results[2] = median
        time.sleep(SLEEP_DURATION)

    with open("data1.json", "w") as f:
        json.dump(results, f)

    make_chart(results)

if __name__ == "__main__":
    main()
