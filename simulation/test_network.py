
import unittest
import random
from network import Network


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.loss_probabilities = {
            1200: 0.001,
            1300: 0.002,
            1400: 0.005,
            1492: 0.01,
            1500: 0.03
        }

        self.network = Network(
            self.loss_probabilities,
            10_000_000,
            50
        )

    def test_payload_size(self):
        self.assertEqual(self.network.payload_size(1500), 1450)
        self.assertEqual(self.network.payload_size(1200), 1150)

    def test_transmission_time(self):
        expected_time = (1500 * 8) / 10_000_000

        self.assertAlmostEqual(
            self.network.transmission_time(1500),
            expected_time
        )

    def test_expected_goodput(self):
        expected_goodput = (
            10_000_000 * (1450 / 1500) * (1 - 0.03)
        )

        self.assertAlmostEqual(
            self.network.expected_goodput(1500),
            expected_goodput
        )

    def test_transmit(self):
        random.seed(1)

        num_packets = 10000
        delivered = 0

        for _ in range(num_packets):
            if self.network.transmit(1500):
                delivered += 1

        observed_loss_rate = (num_packets - delivered) / num_packets

        self.assertAlmostEqual(
            observed_loss_rate,
            self.loss_probabilities[1500],
            delta=0.01
        )


if __name__ == "__main__":
    unittest.main()
