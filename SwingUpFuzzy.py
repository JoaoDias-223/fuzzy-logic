import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystemSimulation, ControlSystem


class SwingUpFuzzy:
    def __init__(self):
        self.angle: Antecedent = None
        self.angular_velocity: Antecedent = None
        self.applied_force: Consequent = None
        self.rules: 'list[Rule]' = None

        self.set_antecedents()
        self.set_consequents()
        self.set_rules()

    def set_antecedents(self):
        self.angle = Antecedent(np.arange(0, 300, 1), 'angle')

        self.angle['NLS'] = fuzz.trimf(self.angle.universe, [90, 130, 170])
        self.angle['NBS'] = fuzz.trimf(self.angle.universe, [30, 150, 170])
        self.angle['SALN'] = fuzz.trimf(self.angle.universe, [170, 175, 180])
        self.angle['Z'] = fuzz.trimf(self.angle.universe, [180, 180, 180])
        self.angle['SALP'] = fuzz.trimf(self.angle.universe, [180, 185, 190])
        self.angle['PBS'] = fuzz.trimf(self.angle.universe, [190, 210, 330])
        self.angle['PLS'] = fuzz.trimf(self.angle.universe, [190, 230, 270])

        self.angular_velocity = Antecedent(np.arange(-10, 10, 0.1), 'angularVelocity')

        self.angular_velocity['NEG'] = fuzz.trapmf(self.angular_velocity.universe, [-10, -10, -1, 0])
        self.angular_velocity['ZS'] = fuzz.trapmf(self.angular_velocity.universe, [-0.1, 0, 0, 0.1])
        self.angular_velocity['POS'] = fuzz.trapmf(self.angular_velocity.universe, [0, 1, 10, 10])

    def set_consequents(self):
        self.applied_force = Consequent(np.arange(-6, 6, 0.2), 'appliedForce')

        self.applied_force['NVVB'] = fuzz.trapmf(self.applied_force.universe, [-6, -6, -4.8, -3.6])
        self.applied_force['NVB'] = fuzz.trimf(self.applied_force.universe, [-4.8, -3.6, -2.4])
        self.applied_force['NB'] = fuzz.trimf(self.applied_force.universe, [-3.6, -2.4, -1.2])
        self.applied_force['N'] = fuzz.trimf(self.applied_force.universe, [-2.4, -1.2, 0])
        self.applied_force['Z'] = fuzz.trimf(self.applied_force.universe, [-1.2, 0, 1.2])
        self.applied_force['P'] = fuzz.trimf(self.applied_force.universe, [0, 1.2, 2.4])
        self.applied_force['PB'] = fuzz.trimf(self.applied_force.universe, [1.2, 2.4, 3.6])
        self.applied_force['PVB'] = fuzz.trimf(self.applied_force.universe, [2.4, 3.6, 4.8])
        self.applied_force['PVVB'] = fuzz.trapmf(self.applied_force.universe, [3.6, 4.8, 6, 6])

    def set_rules(self):
        self.rules = [
            Rule(self.angle['NLS'] & self.angular_velocity['POS'], self.applied_force['NB']),
            Rule(self.angle['NBS'] & self.angular_velocity['POS'], self.applied_force['Z']),
            Rule(self.angle['SALN'] & self.angular_velocity['POS'], self.applied_force['N']),
            Rule(self.angle['Z'] & self.angular_velocity['ZS'], self.applied_force['P']),
            Rule(self.angle['SALP'] & self.angular_velocity['NEG'], self.applied_force['P']),
            Rule(self.angle['PBS'] & self.angular_velocity['NEG'], self.applied_force['Z']),
            Rule(self.angle['PLS'] & self.angular_velocity['NEG'], self.applied_force['PB'])
        ]

    def simulate(self, angle, angular_velocity) -> float:
        simulation = ControlSystemSimulation(ControlSystem(self.rules))

        simulation.input['angle'] = angle
        simulation.input['angularVelocity'] = angular_velocity
        simulation.compute()

        applied_force_value = simulation.output['appliedForce']

        self.plot_simulation(simulation)

        return applied_force_value

    def plot_antecedents(self):
        self.angle.view()
        self.angular_velocity.view()

        plt.show()

    def plot_consequents(self):
        self.applied_force.view()

        plt.show()

    def plot_simulation(self, simulation: ControlSystemSimulation):
        self.angle.view(simulation)
        self.angular_velocity.view(simulation)
        self.applied_force.view(simulation)

        plt.show()
