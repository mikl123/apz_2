import hazelcast
import multiprocessing
import time

key = "key_pes4"

def make_iter():
    global key
    hz_client = hazelcast.HazelcastClient()
    distributed_map = hz_client.get_map("map4").blocking()
    for i in range(10000):
        while True:
            value = distributed_map.get(key)
            new_value = value + 1
            if distributed_map.replace_if_same(key, value, new_value):
                break
            else:
                time.sleep(0.0001)
    hz_client.shutdown()

def run_concurrently():
    start_time = time.time()
    hz_client = hazelcast.HazelcastClient()
    distributed_map = hz_client.get_map("map4").blocking()
    distributed_map.put(key, 0)
    processes = []
    for _ in range(3):
        p = multiprocessing.Process(target=make_iter)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.4f} seconds")
    print(f"Map value ", distributed_map.get(key))
    hz_client.shutdown()

if __name__ == "__main__":
    run_concurrently()
