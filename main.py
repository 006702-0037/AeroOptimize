from vsp_sim import VSPAeroUnsteadyAnalysis
import matplotlib.pyplot as plt

simulation_specs = {"AIR_DENSITY": 1.225,
                    "SPEED_OF_SOUND": 343.1,
                    "CLIMB_VELOCITY": 0,
                    "CPU_NUM": 24,
                    "REV_NUM": 5,
                    "RPM": 6514.670107661428}

standard_prop = {"BLADE_RADIUS": 0.3429,
                 "BLADE_NUM": 2,
                 "TWIST": ([0.2, 0.75, 1.0], [0.1522 * (1 / 0.2), 0.1522 * (1 / 0.75), 0.1522]),
                 "CHORD": ([0.2, 1 / 3, 7 / 15, 0.6, 43 / 60, 5 / 6, 0.95, 29 / 30, 59 / 60, 1.0], [0.04902] * 10),
                 "SWEEP": ([0.2, 1.0], [0.0, 0.0]),
                 "THICKNESS": ([0.2, 7 / 30, 4 / 15, 0.3, 0.4, 0.5, 0.6, 11 / 15, 13 / 15, 1.0], [0.00001] * 10)}

unsteady = VSPAeroUnsteadyAnalysis(standard_prop, simulation_specs)
plt.plot(unsteady[0], unsteady[1])
plt.show()
