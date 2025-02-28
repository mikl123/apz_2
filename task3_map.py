import hazelcast

hz_client = hazelcast.HazelcastClient()

capital_cities = hz_client.get_map("val").blocking()
for i in range(1001):
    capital_cities.put(i, f"value_{i}")

hz_client.shutdown()