import subprocess
import os
import random
import time
import numpy as np
import json
import matplotlib.pyplot as plt

NUM_THREADS = str(2) # set these equal to max number of threads on the server
NUM_CONNECTIONS = str(100)
DURATIONS = str(30)
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
    
    # skip to requests/sec
    while 'Requests/sec:' not in lines[i].strip() :
        i += 1
    words = lines[i].split()
    req_sec = words[1]

    return latency_map, req_sec 

def make_chart(data, x_label, y_label, out, fig):
    plt.figure(fig)
    x = list(data.keys())
    y = list(data.values())
    
    plt.plot(x, y)
    plt.title("100 Connections")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(out)

def main():
    lat_results = {}
    req_results = {}
    for num_reqs in range(2000, 3700, 100): # i in range(0,RUNS,1): # 
        res = run_benchmark(0, 0, 0, 1, NUM_THREADS, NUM_CONNECTIONS, DURATIONS, str(num_reqs))
        print(res)
        print("\n\n\n")
        lat_map, real_num_reqs = parse_results(res)
        median_str = lat_map["50.000%"]
        median_lat = parse_time(median_str)
        lat_results[num_reqs] = median_lat
        req_results[num_reqs] = float(real_num_reqs)
        time.sleep(SLEEP_DURATION)

    make_chart(lat_results, "Specified Requests/Sec", "Latency(s)", "lat_chart.png", 0)
    make_chart(req_results, "Specified Requests/Sec", "Actual Requests/Sec", "req_chart.png", 1)
# with this configuration seem to be hitting max r/s at 2800!!
# max config seems to be 100 connections w 2 threads at throughput of 2900 r/s

# these statistics will be different on the server side
# Need to see if 
if __name__ == "__main__":
    main()
