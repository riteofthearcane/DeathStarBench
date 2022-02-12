import subprocess
import os
import random
import time
from sklearn import preprocessing

NUM_THREADS = str(4)
NUM_CONNECTIONS = str(20)
DURATIONS = str(10)
REQUESTS_PER_SECOND = str(100)

def generateRand():
    return round(random.uniform(0, 1), 3)

def runBenchMark():
    values = []

    for _ in range(4):
        values.append(generateRand())
    
    # Normalize Values
    normalized_arr = preprocessing.normalize([values])

    os.environ["SEARCH_RATIO"] = normalized_arr[0]
    os.environ["RECOMMEND_RATIO"] = normalized_arr[1]
    os.environ["USER_RATIO"] = normalized_arr[2]
    os.environ["RESERVE_RATIO"] = normalized_arr[3]

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
    for _ in range(15):
        runBenchMark()

if __name__ == "__main__":
    main()


