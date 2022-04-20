import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from SwingUpFuzzy import SwingUpFuzzy
from StabilizerFuzzy import StabilizerFuzzy


def main():
    print("SIMULADOR PÊNDULO")
    print("-----------------")
    print(f"1 - Swing Up")
    print(f"2 - Estabilização")
    print()

    simulation_option = int(input("Escolha uma opção: "))

    if simulation_option == 1:
        print()
        print(f"Você escolheu 'Swing Up'")
        print()
    elif simulation_option == 2:
        print()
        print(f"Você escolheu 'Estabilização'")
        print()

    angle = float(input("Digite um ângulo inicial do pêndulo: "))
    angular_velocity = float(input("Digite a velocidade angular do pêndulo: "))

    if simulation_option == 1:
        swing_up_fuzzy = SwingUpFuzzy()

        swing_up_fuzzy.plot_antecedents()
        swing_up_fuzzy.plot_consequents()

        swing_up_output = swing_up_fuzzy.simulate(angle, angular_velocity)

        print(f"Força aplicada no swing up do pêndulo: {swing_up_output}")

    elif simulation_option == 2:
        cart_position = float(input("Digite a posição do carrinho: "))
        cart_velocity = float(input("Digite a velocidade do carrinho: "))

        stabilizer_fuzzy = StabilizerFuzzy()

        stabilizer_fuzzy.plot_antecedents()
        stabilizer_fuzzy.plot_consequents()

        stabilization_output = stabilizer_fuzzy.simulate(angle, angular_velocity, cart_position, cart_velocity)

        print(f"Força aplicada na estabilização do pêndulo: {stabilization_output}")


if __name__ == "__main__":
    main()
