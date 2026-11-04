import random

class Network:
    def __init__(self, loss_probabilities):
        self.loss_probabilities = loss_probabilities

    def transmit(self, packet_size):
        loss_probability = self.loss_probabilities[packet_size]
        return random.random() >= loss_probability

    