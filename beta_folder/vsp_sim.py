# TODO: add error handling for VSPAero

import openvsp as vsp
from math import pi

RPM_TO_RADSEC = pi / 30


def vsp_init():
    vsp.VSPCheckSetup()
    vsp.VSPRenew()
    vsp.ClearVSPModel()


def load_prop(sim, prop):
    prop_id = vsp.AddGeom("PROP")

    # check if other rotor metrics can be set or are simply calculated
    vsp.SetParmVal(prop_id, "Density", "Mass_Props", prop["DENSITY"])
    vsp.SetParmVal(prop_id, "PointMass", "Mass_Props", prop["MASS"])

    vsp.SetParmVal(prop_id, "RadiusFrac", "XSec_0", prop["HUBTRA"])

    # found that 0.3 is beneficial for some rotors, just bullshitted this tho, not sure if even necessary
    vsp.SetParmVal(prop_id, "OutCluster", "Design", 0.3)


    # could also set blade solidity in vspaero after finding mean chord
    vsp.SetParmVal(prop_id, "AF", "Design", prop["ACTIVITY_FACTOR"])
    vsp.SetParmVal(prop_id, "AFLimit", "Design", prop["ACTIVITY_FACTOR_LIMIT"])
    vsp.SetParmVal(prop_id, "Diameter", "Design", 2 * prop["BLADE_RADIUS"])
    vsp.SetParmVal(prop_id, "NumBlade", "Design", prop["BLADE_NUM"])
    vsp.SetParmVal(prop_id, "Beta34", "Design", prop["PITCH_34"]) # might need to be degrees not radians, same w/twist
    vsp.SetParmVal(prop_id, "PropMode", "Design", vsp.PROP_BLADES)

    # should measurements be chord/r or just chord?? same with thickness
    # these are set to default curve type for now, larger sets of data (apc) will likely need different curve types
    vsp.SetPCurve(prop_id, 5, prop["THICK"][0], prop["THICK"][1], vsp.CEDIT)
    vsp.SetPCurve(prop_id, 1, prop["TWIST"][0], prop["TWIST"][1], vsp.PCHIP)
    vsp.SetPCurve(prop_id, 4, prop["SWEEP"][0], prop["SWEEP"][1], vsp.LINEAR)
    vsp.SetPCurve(prop_id, 0, prop["CHORD"][0], prop["CHORD"][1], vsp.CEDIT)


    # load params for the prop's unsteady group
    unsteady_prop_id = vsp.FindUnsteadyGroup(0)
    vsp.SetParmVal(unsteady_prop_id, "RPM", "UnsteadyGroup", sim["RPM"])

    vsp.Update()

    # check on apc website for what the actual hub diameter is, not stated in data file
    vsp.SetParmVal(prop_id, "RadiusFrac", "XSec_0", (1.75/2)/(27/2)) #on the 27x13E
    #vsp.SetParmVal(prop_id, "RadiusFrac", "XSec_0", 0)
    vsp.Update()
    return prop_id, unsteady_prop_id


def load_sim(sim, prop):
    aero_id = vsp.FindContainer("VSPAEROSettings", 0)

    vsp.SetParmVal(aero_id, "UniformPropRPMFlag", "VSPAERO", 1)
    vsp.SetParmVal(aero_id, "GeomSet", "VSPAERO", vsp.SET_ALL)
    vsp.SetParmVal(aero_id, "Rho", "VSPAERO", sim["AIR_DENSITY"])
    vsp.SetParmVal(aero_id, "ManualVrefFlag", "VSPAERO", 1)
    vsp.SetParmVal(aero_id, "RotateBladesFlag", "VSPAERO", 1)
    vsp.SetParmVal(aero_id, "ActuatorDiskFlag", "VSPAERO", 0)
    vsp.SetParmVal(aero_id, "AutoTimeStepFlag", "VSPAERO", 1)
    vsp.SetParmVal(aero_id, "AutoTimeNumRevs", "VSPAERO", sim["REV_NUM"])
    vsp.SetParmVal(aero_id, "NCPU", "VSPAERO", sim["CPU_NUM"])
    vsp.SetParmVal(aero_id, "Vinf", "VSPAERO", sim["CLIMB_VELOCITY"])

    vsp.SetParmVal(aero_id, "Vref", "VSPAERO", prop["BLADE_RADIUS"] * sim["RPM"] * RPM_TO_RADSEC)
    vsp.SetParmVal(aero_id, "Machref", "VSPAERO",
                   prop["BLADE_RADIUS"] * sim["RPM"] * RPM_TO_RADSEC / sim["SPEED_OF_SOUND"])

    vsp.Update()
    return aero_id


def load_analysis(sim, prop):
    # force AnalysisMethod to be vsp.VORTEX_LATTICE, later change to be customizable with sim["ANALYSIS_METHOD"]
    # check if possible to enable 2nd order karman-tsein mach correction and enable hover ramp

    geom_analysis = "VSPAEROComputeGeometry"
    vsp.SetAnalysisInputDefaults(geom_analysis)
    vsp.SetIntAnalysisInput(geom_analysis, "AnalysisMethod", [vsp.VORTEX_LATTICE])

    sweep_analysis = "VSPAEROSweep"
    vsp.SetAnalysisInputDefaults(sweep_analysis)
    vsp.SetIntAnalysisInput(sweep_analysis, "AnalysisMethod", [vsp.VORTEX_LATTICE])
    vsp.SetIntAnalysisInput(sweep_analysis, "GeomSet", [vsp.SET_ALL], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "ManualVrefFlag", [1], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "RotateBladesFlag", [1], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "ActuatorDiskFlag", [0], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "AutoTimeStepFlag", [1], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "AutoTimeNumRevs", [sim["REV_NUM"]], 0)
    vsp.SetIntAnalysisInput(sweep_analysis, "NCPU", [sim["CPU_NUM"]])
    vsp.SetDoubleAnalysisInput(sweep_analysis, "Rho", [sim["AIR_DENSITY"]], 0)
    vsp.SetDoubleAnalysisInput(sweep_analysis, "Vinf", [sim["CLIMB_VELOCITY"]])
    vsp.SetDoubleAnalysisInput(sweep_analysis, "Vref", [prop["BLADE_RADIUS"] * sim["RPM"] * RPM_TO_RADSEC])
    vsp.SetDoubleAnalysisInput(sweep_analysis, "Machref",
                               [prop["BLADE_RADIUS"] * sim["RPM"] * RPM_TO_RADSEC / sim["SPEED_OF_SOUND"]])

    vsp.Update()
    vsp.WriteVSPFile("propeller.vsp3")
    return geom_analysis, sweep_analysis


def VSPAeroUnsteadyAnalysis(prop, sim):
    # initialize vspaero and load prop/sim data
    vsp_init()
    load_prop(sim, prop)
    load_sim(sim, prop)

    # load analysis data into vspaero and execute each
    for analysis in load_analysis(sim, prop):
        vsp.ExecAnalysis(analysis)


        # test only
        '''
        for i in list(prop.keys()):
            print(f"{i}: {prop[i]}")
        vsp.WriteVSPFile("test.vsp3")
        exit()
        '''

    rotor_res = vsp.FindResultsID("VSPAERO_Rotor", 0)
    time = vsp.GetDoubleResults(rotor_res, "Time", 0)
    thrust = vsp.GetDoubleResults(rotor_res, "Thrust", 0)
    power = vsp.GetDoubleResults(rotor_res, "Power", 0)

    return time, thrust, power

# ihiohefwihofewijfewpoewfjpfewjipfweiodioerjogj;d.jfgoinedpirjgieurlgie
