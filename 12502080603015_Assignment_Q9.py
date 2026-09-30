import heapq
import threading

print("=== Threaded Job Scheduler Simulation ===")

w, n = map(int, input("Enter number of workers and jobs: ").split())

jobs = []

for i in range(n):
    arrival, job_id, priority, duration, resources = input(
        f"Enter job {i + 1} (arrival_time job_id priority duration resources): "
    ).split()

    jobs.append((
        int(arrival),
        job_id,
        int(priority),
        int(duration),
        int(resources),
        i
    ))

jobs.sort(key=lambda x: (x[0], x[5]))

worker_heap = [(0, i + 1) for i in range(w)]
heapq.heapify(worker_heap)

job_queue = []
job_index = 0
results = []
lock = threading.Lock()

while job_index < n or job_queue:
    if not job_queue:
        next_arrival = jobs[job_index][0]
        while worker_heap and worker_heap[0][0] <= next_arrival:
            finish_time, worker_id = heapq.heappop(worker_heap)
            heapq.heappush(worker_heap, (finish_time, worker_id))

        current_time = next_arrival

        while job_index < n and jobs[job_index][0] <= current_time:
            arrival, job_id, priority, duration, resources, order = jobs[job_index]
            heapq.heappush(
                job_queue,
                (-priority, order, arrival, job_id, duration, resources)
            )
            job_index += 1
    else:
        current_time = min(
            worker_heap[0][0],
            jobs[job_index][0] if job_index < n else float("inf")
        )

        while job_index < n and jobs[job_index][0] <= current_time:
            arrival, job_id, priority, duration, resources, order = jobs[job_index]
            heapq.heappush(
                job_queue,
                (-priority, order, arrival, job_id, duration, resources)
            )
            job_index += 1

    if not job_queue:
        continue

    worker_free_time, worker_id = heapq.heappop(worker_heap)

    if worker_free_time > current_time:
        current_time = worker_free_time

        while job_index < n and jobs[job_index][0] <= current_time:
            arrival, job_id, priority, duration, resources, order = jobs[job_index]
            heapq.heappush(
                job_queue,
                (-priority, order, arrival, job_id, duration, resources)
            )
            job_index += 1

    if job_queue:
        _, order, arrival, job_id, duration, resources = heapq.heappop(job_queue)

        start_time = max(current_time, arrival)
        finish_time = start_time + duration

        with lock:
            results.append(
                (job_id, worker_id, start_time, finish_time, start_time - arrival)
            )

        heapq.heappush(worker_heap, (finish_time, worker_id))

results.sort(key=lambda x: x[0])

total_wait = sum(result[4] for result in results)
average_wait = total_wait / n

for job_id, worker_id, start_time, finish_time, wait in results:
    print(f"{job_id} W{worker_id} {start_time} {finish_time}")

print(f"AVG_WAIT {average_wait:.2f}")