import hazelcast
import threading
import time

client1 = hazelcast.HazelcastClient()
client2 = hazelcast.HazelcastClient()
client3 = hazelcast.HazelcastClient()

queue = client1.get_queue("queue")

def produce():
    for i in range(100):
        queue.offer("value-" + str(i))
    queue.offer(1)
    queue.offer(1)
    print("Producer has finished producing.")

def consume(n, client):
    queue = client.get_queue("queue")
    consumed_count = 0
    while True:
        head = queue.take().result()
        if head == 1:
            break
        print(f"Node{n} Consuming {head}")
        consumed_count += 1

producer_thread = threading.Thread(target=produce)
consumer_thread_1 = threading.Thread(target=consume, args=(1,client2))
consumer_thread_2 = threading.Thread(target=consume, args=(2,client3))

producer_thread.start()
time.sleep(0.1)
consumer_thread_1.start()
consumer_thread_2.start()

producer_thread.join()

client1.shutdown()

consumer_thread_1.join()
consumer_thread_2.join()

client2.shutdown()
client3.shutdown()

