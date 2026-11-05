import random

class Network:
    def __init__(self, loss_probabilities, bandwidth, overhead):
        self.loss_probabilities = loss_probabilities
        self.bandwidth = bandwidth
        self.overhead = overhead

    def payload_size(self, packet_size):
        return packet_size - self.overhead

    def transmission_time(self, packet_size):
        return (packet_size * 8) / self.bandwidth #transmission time in seconds

    def transmit(self, packet_size):
        loss_probability = self.loss_probabilities[packet_size]
        return random.random() >= loss_probability

    def expected_goodput(self, packet_size):
        loss_probability = self.loss_probabilities[packet_size]
        payload_efficiency = self.payload_size(packet_size) / packet_size
        return self.bandwidth * payload_efficiency * (1 - loss_probability)

    