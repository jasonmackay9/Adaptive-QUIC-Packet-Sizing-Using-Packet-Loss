import random
from network import Network
from potu import POTU

MAXIMUM_PACKET_SIZE = 1500

def run_experiment(seed, loss_probabilities, min_samples, num_packets):
    random.seed(seed)

    network = Network(loss_probabilities, 10_000_000, 50)
    potu = POTU(
        packet_sizes = [packet_size for packet_size in loss_probabilities.keys() if packet_size <= MAXIMUM_PACKET_SIZE],
        min_samples=min_samples,
        improvement_threshold=0.005)

    # Initial exploration
    exploration_time, exploration_delivered_bytes = run_potu_exploration(network, potu)

    # Select efficient packet size based on exploration results
    selected_packet_size = potu.select_efficient_packet_size(MAXIMUM_PACKET_SIZE, network.bandwidth, network.overhead)

    # Baseline transmission with maximum packet size
    baseline_time, baseline_delivered_bytes = run_baseline(network, MAXIMUM_PACKET_SIZE, num_packets)
    baseline_goodput = (baseline_delivered_bytes * 8) / baseline_time

    # POTU steady-state transmission (excluding exploration)
    potu_steady_state_time, potu_steady_state_delivered_bytes = run_potu_steady_state(network, potu, selected_packet_size, num_packets)
    potu_steady_state_goodput = (potu_steady_state_delivered_bytes * 8) / potu_steady_state_time

    # POTU overall performance (including exploration)
    potu_total_time = exploration_time + potu_steady_state_time
    potu_total_delivered_bytes = exploration_delivered_bytes + potu_steady_state_delivered_bytes
    potu_overall_goodput = (potu_total_delivered_bytes * 8) / potu_total_time

    # Percentage improvements
    steady_state_improvement = ((potu_steady_state_goodput - baseline_goodput) / baseline_goodput) * 100
    overall_improvement = ((potu_overall_goodput - baseline_goodput) / baseline_goodput) * 100

    return {
        "selected_packet_size": selected_packet_size,
        "baseline_goodput": baseline_goodput,
        "potu_steady_state_goodput": potu_steady_state_goodput,
        "potu_overall_goodput": potu_overall_goodput,
        "steady_state_improvement": steady_state_improvement,
        "overall_improvement": overall_improvement
    }

def run_baseline(network, packet_size, num_packets):
    total_time = 0
    delivered_bytes = 0

    for _ in range(num_packets):
        total_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)

        if delivered:
            delivered_bytes += network.payload_size(packet_size)

    return total_time, delivered_bytes

def run_potu_exploration(network, potu):
    exploration_time = 0
    exploration_delivered_bytes = 0

    while True:
        packet_size = potu.next_exploration_packet_size()

        if packet_size is None:
            break

        exploration_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)
        potu.record_sent(packet_size, delivered)

        if delivered:
            exploration_delivered_bytes += network.payload_size(packet_size)

    return exploration_time, exploration_delivered_bytes

def run_potu_steady_state(network, potu, packet_size, num_packets):
    total_time = 0
    delivered_bytes = 0

    for _ in range(num_packets):
        total_time += network.transmission_time(packet_size)

        delivered = network.transmit(packet_size)
        potu.record_sent(packet_size, delivered)

        if delivered:
            delivered_bytes += network.payload_size(packet_size)

    return total_time, delivered_bytes

loss_probabilities = {
    1200: 0.001,
    1300: 0.002,
    1400: 0.005,
    1492: 0.01,
    1500: 0.03
}

num_trials = 100
results = []

for seed in range(num_trials):
    result = run_experiment(seed = seed, loss_probabilities = loss_probabilities, min_samples = 100, num_packets = 10000)
    results.append(result)

average_steady_state_improvement = sum(result['steady_state_improvement'] for result in results) / num_trials
average_overall_improvement = sum(result['overall_improvement'] for result in results) / num_trials

print("MULTIPLE TRIAL RESULTS:")
print(f"Number of trials: {num_trials}")
print(f"Average steady-state improvement: {average_steady_state_improvement:.2f}%")
print(f"Average overall improvement: {average_overall_improvement:.2f}%")

print("\nPACKET SIZE SELECTION FREQUENCY:")

for packet_size in loss_probabilities:
    count = sum(
        result["selected_packet_size"] == packet_size
        for result in results
    )

    percentage = (count / num_trials) * 100

    print(f"{packet_size} bytes: {count} selections ({percentage:.1f}%)")

'''
results = run_experiment(seed = 1, loss_probabilities = loss_probabilities, min_samples = 100, num_packets = 10000)

print("SIMULATION RESULTS:")
print(f"Selected packet size: {results['selected_packet_size']}")
print(f"Baseline goodput: {results['baseline_goodput'] / 1_000_000:.4f} Mbps")
print(f"POTU steady-state goodput: {results['potu_steady_state_goodput'] / 1_000_000:.4f} Mbps")
print(f"POTU overall goodput: {results['potu_overall_goodput'] / 1_000_000:.4f} Mbps")
print(f"Steady-state improvement: {results['steady_state_improvement']:.2f}%")
print(f"Overall improvement: {results['overall_improvement']:.2f}%")
'''
