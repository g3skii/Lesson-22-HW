#სავარჯიშო 1

import time
import threading
import multiprocessing



def make_tea(name, seconds):
    print(f"{name}: იწყება")
    time.sleep(seconds)
    print(f"{name}: მზადაა")


teas = [("მწვანე ჩაი", 1.0), ("შავი ჩაი", 1.5), ("ბალახის ჩაი", 2.0)]


def exercise_1():
    # 1. თანმიმდევრულად
    start = time.perf_counter()
    for name, seconds in teas:
        make_tea(name, seconds)
    sequential_time = time.perf_counter() - start
    print(f"თანმიმდევრულად: {sequential_time:.1f} წმ")


    start = time.perf_counter()
    threads = []
    for name, seconds in teas:
        t = threading.Thread(target=make_tea, args=(name, seconds))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    threaded_time = time.perf_counter() - start
    print(f"thread-ებით: {threaded_time:.1f} წმ")


    print(f"დაჩქარება: {sequential_time / threaded_time:.1f}x")

def cpu_task(n):
    while n > 0:
        n -= 1


def io_task(seconds):
    time.sleep(seconds)


def run_sequential(task, jobs):
    for job in jobs:
        task(job)


def run_threads(task, jobs):
    threads = [threading.Thread(target=task, args=(job,)) for job in jobs]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def run_processes(task, jobs):
    processes = [multiprocessing.Process(target=task, args=(job,)) for job in jobs]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


def measure(runner, task, jobs):
    start = time.perf_counter()
    runner(task, jobs)
    return time.perf_counter() - start


def exercise_2():
    cpu_jobs = [10_000_000] * 4
    io_jobs = [1.0] * 4
    runners = [run_sequential, run_threads, run_processes]

    print("| თანმიმდევრულად | thread-ები | პროცესები")
    for label, task, jobs in [("CPU-bound", cpu_task, cpu_jobs),
                              ("I/O-bound", io_task, io_jobs)]:
        times = [measure(runner, task, jobs) for runner in runners]
        base = times[0]
        cells = [f"{t:.2f} წმ ({base / t:4.1f}x)" for t in times]
        print(f"{label} | " + " | ".join(cells))

if __name__ == "__main__":
    exercise_1()
    print()
    exercise_2()

