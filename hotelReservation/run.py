import subprocess
import os
import random
import time
import numpy as np

NUM_THREADS = str(4)
NUM_CONNECTIONS = str(20)
DURATIONS = str(10)
REQUESTS_PER_SECOND = str(100)
RUNS = 5
SLEEP_DURATION = 1

def generateRand():
    return round(random.uniform(0, 1), 3)

def runBenchMark():
    
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
    
    subprocess.run(["./wrk2/wrk", 
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
                    REQUESTS_PER_SECOND])

    # Delete Env when finished
    del os.environ["SEARCH_RATIO"]
    del os.environ["RECOMMEND_RATIO"]
    del os.environ["USER_RATIO"]
    del os.environ["RESERVE_RATIO"]


def main():
    for _ in range(RUNS):
        runBenchMark()
        time.sleep(SLEEP_DURATION)

if __name__ == "__main__":
    main()


