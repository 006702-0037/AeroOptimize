import re
from math import pi

INCH_TO_METER = 0.0254
#DEG_TO_RAD = pi / 180
DEG_TO_RAD=1
LB_INCH_TO_KG_M = 27679.905


def extract_curve_data(file, prop):
    data_pattern = r'(?:-?\d*\.\d+|-?\d+)(?:\s+(?:-?\d*\.\d+|-?\d+)){12}'
    columns = [("CHORD", 1), ("PITCH", 2), ("SWEEP", 5), ("TWIST", 7), ("THICK", 6)]

    for match in re.findall(data_pattern, file):
        vals = match.split()

        for name, index in columns:
            prop[name][0].append(float(vals[0]))
            prop[name][1].append(float(vals[index]))


def extract_prop_features(file, prop):
    blade_pattern = r'(?=.*NUMBER OF BLADES)(\d+(\.\d+)?)'
    hubtra_pattern = r'HUBTRA.*?(\d+(\.\d+)?)'
    mass_pattern = r'TOTAL WEIGHT \(Kg\).*?(\d+(\.\d+)?)'
    density_pattern = r'AVERAGE DENSITY.*?=\s*(-?[\d\.]+(?:[eE][+-]?\d+)?).*'
    activity_pattern = r'ACTIVITY FACTOR.*?=\s*(-?[\d\.]+(?:[eE][+-]?\d+)?).*'
    activity_limit_pattern = r'INNER LIMIT \(NORMALIZED\).*?(\d+(\.\d+)?)'

    blade_num = re.search(blade_pattern, file).group(1)
    hubtra = re.search(hubtra_pattern, file).group(1)
    blade_mass = re.search(mass_pattern, file).group(1)
    blade_density = re.search(density_pattern, file).group(1)
    blade_activity = re.search(activity_pattern, file).group(1)
    blade_activity_limit = re.search(activity_limit_pattern, file).group(1)

    prop["BLADE_NUM"] = int(blade_num)
    prop["HUBTRA"] = float(hubtra)
    prop["DENSITY"] = float(blade_density)
    prop["MASS"] = float(blade_mass)
    prop["ACTIVITY_FACTOR"] = float(blade_activity)
    prop["ACTIVITY_FACTOR_LIMIT"] = float(blade_activity_limit)


def format_data(prop):
    prop["BLADE_RADIUS"] = prop["CHORD"][0][-1]  # truly could be any curve type


    # normalize curve data
    for curve in ["TWIST", "CHORD", "SWEEP", "THICK", "PITCH"]:
        prop[curve][0] = [i / prop["BLADE_RADIUS"] for i in prop[curve][0]]

    # make quantity geometric
    prop["CHORD"][1] = [i / prop["BLADE_RADIUS"] for i in prop["CHORD"][1]]

    # convert to metric

    #prop["SWEEP"][1] = [i * INCH_TO_METER for i in prop["SWEEP"][1]]

    prop["SWEEP"][1] = [(i/prop["BLADE_RADIUS"])*(180/pi) for i in prop["SWEEP"][1]]
    setback=4
    for i in range(1,setback):
        prop["SWEEP"][1][-i]=prop["SWEEP"][1][-setback]
    # might need to decrease tip clustering



    prop["HUBTRA"]/=prop["BLADE_RADIUS"]
    prop["DENSITY"] *= LB_INCH_TO_KG_M
    prop["TWIST"][1] = [i * DEG_TO_RAD for i in prop["TWIST"][1]]

    # find 3/4 pitch
    pitch_rearrange=[(prop["PITCH"][0][i],prop["PITCH"][1][i]) for i in range(len(prop["PITCH"][0]))]
    pitch_rearrange.sort(key=lambda x: abs(x[0] - 0.75))
    prop["PITCH_34"]=pitch_rearrange[0][1]
    prop["PITCH_34"]*=DEG_TO_RAD

    prop["BLADE_RADIUS"] *= INCH_TO_METER


def get_prop(file_path):
    new_prop = {"BLADE_RADIUS": 0.0,
                "BLADE_NUM": 0,
                "DENSITY": 0.0,
                "MASS": 0.0,
                "HUBTRA": 0.0,
                "ACTIVITY_FACTOR": 0.0,
                "ACTIVITY_FACTOR_LIMIT": 0.0,
                "PITCH_34": 0.0,
                "PITCH": [[], []],
                "TWIST": [[], []],
                "CHORD": [[], []],
                "SWEEP": [[], []],
                "THICK": [[], []]}

    with open(file_path) as prop_file:
        file_lines = prop_file.read()

        extract_curve_data(file_lines, new_prop)
        extract_prop_features(file_lines, new_prop)
        format_data(new_prop)

    return new_prop
