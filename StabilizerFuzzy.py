import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy.control import Antecedent, Consequent, Rule, ControlSystemSimulation, ControlSystem


class StabilizerFuzzy:
    def __init__(self):
        self.angle: Antecedent = None
        self.angular_velocity: Antecedent = None
        self.cart_position: Antecedent = None
        self.cart_velocity: Antecedent = None
        self.applied_force: Consequent = None
        self.rules: 'list[Rule]' = None

        self.set_antecedents()
        self.set_consequents()
        self.set_rules()

    def set_antecedents(self):
        self.angle = Antecedent(np.arange(-30, 30, 0.5), 'angle')

        self.angle['NVB'] = fuzz.trapmf(self.angle.universe, [-30, -30, -18, -12])
        self.angle['NB'] = fuzz.trimf(self.angle.universe, [-16.5, -10.5, -4.5])
        self.angle['N'] = fuzz.trimf(self.angle.universe, [-9, -4.5, 0])
        self.angle['ZO'] = fuzz.trimf(self.angle.universe, [-3, 0, 3])
        self.angle['P'] = fuzz.trimf(self.angle.universe, [0, 4.5, 9])
        self.angle['PB'] = fuzz.trimf(self.angle.universe, [4.5, 10.5, 16.5])
        self.angle['PVB'] = fuzz.trapmf(self.angle.universe, [12, 18, 30, 30])

        self.angular_velocity = Antecedent(np.arange(-6, 6, 0.1), 'angularVelocity')

        self.angular_velocity['NB'] = fuzz.trapmf(self.angular_velocity.universe, [-6, -6, -4.2, -1.7])
        self.angular_velocity['N'] = fuzz.trimf(self.angular_velocity.universe, [-3.6, -1.7, 0])
        self.angular_velocity['ZO'] = fuzz.trimf(self.angular_velocity.universe, [-1.7, 0, 1.7])
        self.angular_velocity['P'] = fuzz.trimf(self.angular_velocity.universe, [0, 1.7, 3.6])
        self.angular_velocity['PB'] = fuzz.trapmf(self.angular_velocity.universe, [1.7, 4.2, 6, 6])

        self.cart_position = Antecedent(np.arange(-0.4, 0.4, 0.05), 'cartPosition')

        self.cart_position['NBIG'] = fuzz.trapmf(self.cart_position.universe, [-0.4, -0.4, -0.3, -0.15])
        self.cart_position['NEG'] = fuzz.trimf(self.cart_position.universe, [-0.3, -0.15, 0])
        self.cart_position['Z'] = fuzz.trimf(self.cart_position.universe, [-0.15, 0, 0.15])
        self.cart_position['POS'] = fuzz.trimf(self.cart_position.universe, [0, 0.15, 0.3])
        self.cart_position['PBIG'] = fuzz.trapmf(self.cart_position.universe, [0.15, 0.3, 0.4, 0.4])

        self.cart_velocity = Antecedent(np.arange(-1, 1, 0.1), 'cartVelocity')

        self.cart_velocity['NEG'] = fuzz.trapmf(self.cart_velocity.universe, [-1, -1, -0.1, 0])
        self.cart_velocity['ZERO'] = fuzz.trimf(self.cart_velocity.universe, [-0.1, 0, 0.1])
        self.cart_velocity['POS'] = fuzz.trapmf(self.cart_velocity.universe, [0, 0.1, 1, 1])

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
            Rule(self.cart_position['NBIG'] & self.cart_velocity['NEG'], self.applied_force['PVVB']),
            Rule(self.cart_position['NEG'] & self.cart_velocity['NEG'], self.applied_force['PVB']),
            Rule(self.cart_position['Z'] & self.cart_velocity['NEG'], self.applied_force['PB']),
            Rule(self.cart_position['Z'] & self.cart_velocity['ZERO'], self.applied_force['Z']),
            Rule(self.cart_position['Z'] & self.cart_velocity['POS'], self.applied_force['NB']),
            Rule(self.cart_position['POS'] & self.cart_velocity['POS'], self.applied_force['NVB']),
            Rule(self.cart_position['PBIG'] & self.cart_velocity['POS'], self.applied_force['NVVB']),

            Rule(self.angle['NVB'] & self.angular_velocity['NB'], self.applied_force['NVVB']),
            Rule(self.angle['NVB'] & self.angular_velocity['N'], self.applied_force['NVVB']),
            Rule(self.angle['NVB'] & self.angular_velocity['ZO'], self.applied_force['NVB']),
            Rule(self.angle['NVB'] & self.angular_velocity['P'], self.applied_force['NB']),
            Rule(self.angle['NVB'] & self.angular_velocity['PB'], self.applied_force['N']),

            Rule(self.angle['NB'] & self.angular_velocity['NB'], self.applied_force['NVVB']),
            Rule(self.angle['NB'] & self.angular_velocity['N'], self.applied_force['NVB']),
            Rule(self.angle['NB'] & self.angular_velocity['ZO'], self.applied_force['NB']),
            Rule(self.angle['NB'] & self.angular_velocity['P'], self.applied_force['N']),
            Rule(self.angle['NB'] & self.angular_velocity['PB'], self.applied_force['Z']),

            Rule(self.angle['N'] & self.angular_velocity['NB'], self.applied_force['NVB']),
            Rule(self.angle['N'] & self.angular_velocity['N'], self.applied_force['NB']),
            Rule(self.angle['N'] & self.angular_velocity['ZO'], self.applied_force['N']),
            Rule(self.angle['N'] & self.angular_velocity['P'], self.applied_force['Z']),
            Rule(self.angle['N'] & self.angular_velocity['PB'], self.applied_force['P']),

            Rule(self.angle['ZO'] & self.angular_velocity['NB'], self.applied_force['NB']),
            Rule(self.angle['ZO'] & self.angular_velocity['N'], self.applied_force['N']),
            Rule(self.angle['ZO'] & self.angular_velocity['ZO'], self.applied_force['Z']),
            Rule(self.angle['ZO'] & self.angular_velocity['P'], self.applied_force['P']),
            Rule(self.angle['ZO'] & self.angular_velocity['PB'], self.applied_force['PB']),

            Rule(self.angle['P'] & self.angular_velocity['NB'], self.applied_force['N']),
            Rule(self.angle['P'] & self.angular_velocity['N'], self.applied_force['Z']),
            Rule(self.angle['P'] & self.angular_velocity['ZO'], self.applied_force['P']),
            Rule(self.angle['P'] & self.angular_velocity['P'], self.applied_force['PB']),
            Rule(self.angle['P'] & self.angular_velocity['PB'], self.applied_force['PVB']),

            Rule(self.angle['PB'] & self.angular_velocity['NB'], self.applied_force['Z']),
            Rule(self.angle['PB'] & self.angular_velocity['N'], self.applied_force['P']),
            Rule(self.angle['PB'] & self.angular_velocity['ZO'], self.applied_force['PB']),
            Rule(self.angle['PB'] & self.angular_velocity['P'], self.applied_force['PVB']),
            Rule(self.angle['PB'] & self.angular_velocity['PB'], self.applied_force['PVVB']),

            Rule(self.angle['PVB'] & self.angular_velocity['NB'], self.applied_force['P']),
            Rule(self.angle['PVB'] & self.angular_velocity['N'], self.applied_force['PB']),
            Rule(self.angle['PVB'] & self.angular_velocity['ZO'], self.applied_force['PVB']),
            Rule(self.angle['PVB'] & self.angular_velocity['P'], self.applied_force['PVVB']),
            Rule(self.angle['PVB'] & self.angular_velocity['PB'], self.applied_force['PVVB'])
        ]

    def simulate(self, angle, angular_velocity, cart_position, cart_velocity) -> float:
        simulation = ControlSystemSimulation(ControlSystem(self.rules))

        simulation.input['angle'] = angle
        simulation.input['angularVelocity'] = angular_velocity
        simulation.input['cartPosition'] = cart_position
        simulation.input['cartVelocity'] = cart_velocity
        simulation.compute()

        applied_force_value = simulation.output['appliedForce']

        self.plot_simulation(simulation)

        return applied_force_value

    def plot_antecedents(self):
        self.angle.view()
        self.angular_velocity.view()
        self.cart_position.view()
        self.cart_velocity.view()

        plt.show()

    def plot_consequents(self):
        self.applied_force.view()

        plt.show()

    def plot_simulation(self, simulation: ControlSystemSimulation):
        self.angle.view(simulation)
        self.angular_velocity.view(simulation)
        self.cart_position.view(simulation)
        self.cart_velocity.view(simulation)
        self.applied_force.view(simulation)

        plt.show()
