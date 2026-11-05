import random
from network import Network

random.seed(1)

loss_probabilities = {
    1200: 0.001,
    1300: 0.002,
    1400: 0.005,
    1492: 0.01,
    1500: 0.03
}

network = Network(loss_probabilities, 10_000_000, 50)

num_packets = 10000

for packet_size in loss_probabilities.keys():
    total_time = 0
    delivered = 0

    for _ in range(num_packets):
        total_time += network.transmission_time(packet_size)

        if network.transmit(packet_size):
            delivered += 1

    delivered_bytes = delivered * network.payload_size(packet_size)

    goodput = (delivered_bytes * 8) / total_time
    goodput_mbps = goodput / 1_000_000
    expected_goodput_mbps = network.expected_goodput(packet_size) / 1_000_000

    lost = num_packets - delivered

    print(f"Packet size: {packet_size}")
    print(f"Packets sent: {num_packets}")
    print(f"Packets delivered: {delivered}")
    print(f"Packets lost: {lost}")
    print(f"Observed loss rate: {lost / num_packets:.4f}")
    print(f"Goodput: {goodput_mbps:.4f} Mbps")
    print(f"Expected goodput: {expected_goodput_mbps:.4f} Mbps")
    print()