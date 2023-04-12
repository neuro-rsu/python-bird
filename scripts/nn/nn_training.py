"""Модуль, занимающийся обучением нейросети."""

import numpy as np


def network_fitting(best_network, inputs, outputs, max_epochs, print_number):
    """Реализует процесс обучения нейросети.

    Параметры:
    best_network - объект, представляющий собой нейросеть;
    inputs, outputs - входы и выходы нейросети;
    max_epochs - максимальное число эпох обучения;
    вывод результата в консоль каждые print_number эпох.

    """
    best_cost = 1000000
    best_net_results = np.empty(len(inputs))

    for i in range(1, max_epochs + 1):
        mutated_network = best_network.clone()
        mutated_network.mutate()
        mutated_cost = 0
        current_net_result = np.empty(len(inputs))

        for j, line in enumerate(inputs):
            result = mutated_network.feed_forward(line)
            mutated_cost += abs(result[0] - outputs[j])
            current_net_result[j] = result[0]

        if mutated_cost < best_cost:
            best_network = mutated_network
            best_cost = mutated_cost
            best_net_results = current_net_result

        if i % print_number == 0:
            for k, res in enumerate(best_net_results):
                print(f"{inputs[k][0]}, {inputs[k][1]} | {res}")

            print(f"Loss: {best_cost * 100}%")
            print(f"Epoch: {i}")
            print("-" * 80)
