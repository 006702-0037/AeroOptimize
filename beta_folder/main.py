from vsp_sim import VSPAeroUnsteadyAnalysis
from parse_apc_data import get_prop
from math_utils import convergence
import matplotlib.pyplot as plt

simulation_specs = {"AIR_DENSITY": 1.225,
                    "SPEED_OF_SOUND": 343.1,
                    "CLIMB_VELOCITY": 0,
                    "CPU_NUM": 24,
                    "REV_NUM": 10,
                    "RPM": 2000}

test_prop = get_prop("PE0-FILES_WEB/27x13E-PERF.PE0")
unsteady = VSPAeroUnsteadyAnalysis(test_prop, simulation_specs)


print(test_prop)
plt.plot(unsteady[0], unsteady[1])
#thust=convergence(unsteady[1])
#print(thust)
#print(thust*0.2248089431)
#print()
plt.show()

plt.plot(unsteady[0], unsteady[2])
#pwr=convergence(unsteady[2])
#print(pwr)
#print(pwr*0.00134102)
#print()
plt.show()
