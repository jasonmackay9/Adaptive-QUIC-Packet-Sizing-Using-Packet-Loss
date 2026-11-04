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

network = Network(loss_probabilities)

num_packets = 10000

for packet_size in loss_probabilities.keys():
    delivered = 0

    for _ in range(num_packets):
        if network.transmit(packet_size):
            delivered += 1

    lost = num_packets - delivered

    print(f"Packet size: {packet_size}")
    print(f"Packets sent: {num_packets}")
    print(f"Packets delivered: {delivered}")
    print(f"Packets lost: {lost}")
    print(f"Observed loss rate: {lost / num_packets:.4f}")
    print()