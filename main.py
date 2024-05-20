from vsp_sim import VSPAeroUnsteadyAnalysis
import matplotlib.pyplot as plt
from math import pi

simulation_specs = {"AIR_DENSITY": 1.225,
                    "SPEED_OF_SOUND": 343.1,
                    "LIFT_CURVE_SLOPE": 2*pi,
                    "CLIMB_VELOCITY": 0,
                    "CPU_NUM": 24,
                    "REV_NUM": 5,
                    "RPM": 6514.670107661428}

standard_prop = {"BLADE_RADIUS": 0.3429,
                 "BLADE_NUM": 2,
                 "BLADE_TIP_PITCH_ANGLE": 0.1522,
                 "BLADE_CHORD": 0.04902,
                 "BLADE_THICKNESS": 0.00001}

unsteady = VSPAeroUnsteadyAnalysis(standard_prop, simulation_specs)

plt.plot(unsteady[0], unsteady[1])
plt.show()
