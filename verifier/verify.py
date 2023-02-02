import argparse
import xml.etree.ElementTree as ET

mandatory_properties = {
    'Add': ['vessel', 'reagent'],
    'Separate': ['purpose', 'product_phase', 'from_vessel', 'separation_vessel', 'to_vesse'],
    'Transfer': ['from_vessel', 'to_vessel'],
    'StartStir': ['vessel'],
    'Stir': ['vessel', 'time'],
    'StopStir': ['vessel'],
    'HeatChill': ['vessel', 'temp', 'time'],
    'HeatChillToTemp': ['vessel', 'temp'],
    'StartHeatChill': ['vessel', 'temp'],
    'StopHeatChill': ['vessel'],
    'EvacuateAndRefill': ['vessel'],
    'Purge': ['vessel'],
    'StartPurge': ['vessel'],
    'StopPurge': ['vessel'],
    'Filter': ['vessel'],
    'FilterThrough': ['from_vessel', 'to_vessel', 'through'],
    'WashSolid': ['vessel', 'solvent', 'volume'],
    'Wait': ['time'],
    'Repeat': ['repeats'],
    'CleanVessel': ['vessel', 'reagent'],
    'Crystallize': ['vessel'],
    'Dissolve': ['vessel', 'solvent'],
    'Dry': ['vessel'],
    'Evaporate': ['vessel'],
    'Irradiate': ['vessel', 'time'],
    'Precipitate': ['vessel'],
    'ResetHandling': [],
    'RunColumn': ['from_vessel', 'to_vessel']
}

optional_properties = {
    'Add': ['vessel', 'reagent', 'volume', 'mass', 'amount', 'dropwise', 'time', 'stir', 'stir_speed', 'viscous', 'purpose'],
    'Separate': ['purpose', 'product_phase', 'from_vessel', 'separation_vessel', 'to_vessel', 'waste_phase_to_vessel', 'solvent', 'solvent_volume', 'through', 'repeats', 'stir_time', 'stir_speed', 'settling_time'],
    'Transfer': ['from_vessel', 'to_vessel', 'volume', 'amount', 'time', 'viscous', 'rinsing_solvent', 'rinsing_volume', 'rinsing_repeats', 'solid'],
    'StartStir': ['vessel', 'stir_speed', 'purpose'],
    'Stir': ['vessel', 'time', 'stir_speed', 'continue_stirring', 'purpose'],
    'StopStir': ['vessel'],
    'HeatChill': ['vessel', 'temp', 'time', 'stir', 'stir_speed', 'purpose'],
    'HeatChillToTemp': ['vessel', 'temp', 'active', 'continue_heatchill', 'stir', 'stir_speed', 'purpose'],
    'StartHeatChill': ['vessel', 'temp', 'purpose'],
    'StopHeatChill': ['vessel'],
    'EvacuateAndRefill': ['vessel', 'gas', 'repeats'],
    'Purge': ['vessel', 'gas', 'time', 'pressure', 'flow_rate'],
    'StartPurge': ['vessel', 'gas', 'pressure', 'flow_rate'],
    'StopPurge': ['vessel'],
    'Filter': ['vessel', 'filtrate_vessel', 'stir', 'stir_speed', 'temp', 'continue_heatchill', 'volume'],
    'FilterThrough': ['from_vessel', 'to_vessel', 'through', 'eluting_solvent', 'eluting_volume', 'eluting_repeats', 'residence_time'],
    'WashSolid': ['vessel', 'solvent', 'volume', 'filtrate_vessel', 'temp', 'stir', 'stir_speed', 'time', 'repeats'],
    'Wait': ['time'],
    'Repeat': ['repeats', 'children', 'loop_variables', 'iterative'],
    'CleanVessel': ['vessel', 'solvent', 'volume', 'temp', 'repeats'],
    'Crystallize': ['vessel', 'ramp_time', 'ramp_temp'],
    'Dissolve': ['vessel', 'solvent', 'volume', 'amount', 'temp', 'time', 'stir_speed'],
    'Dry': ['vessel', 'time', 'pressure', 'temp', 'continue_heatchill'],
    'Evaporate': ['vessel', 'time', 'pressure', 'temp', 'stir_speed'],
    'Irradiate': ['vessel', 'time', 'wavelegth', 'color', 'temp', 'stir', 'stir_speed', 'cooling_power'],
    'Precipitate': ['vessel', 'time', 'temp', 'stir_speed', 'reagent', 'volume', 'amount', 'add_time'],
    'ResetHandling': ['solvent', 'volume', 'repeats'],
    'RunColumn': ['from_vessel', 'to_vessel', 'column'],
}


def parse_hardware(root):
    hardware_list = []
    for hardware in root.iter('Hardware'):
        for component in hardware.iter('Component'):
            hardware_list.append(component.attrib['id'])
    return hardware_list


def parse_reagents(root):
    reagent_list = []
    for reagents in root.iter('Reagents'):
        for reagent in reagents.iter('Reagent'):
            reagent_list.append(reagent.attrib['name'])
    return reagent_list


def verify_procedure(root, hardware, reagents):
    printed_error_list = []
    for procedure in root.iter('Procedure'):
        for step in procedure:
            errors = []
            # Check whether action is valid
            action = step.tag
            if action not in mandatory_properties:
                errors.append(f"There is no {action} action in XDL")
                # continue
            # if action not in mandatory_properties and action not in optional_properties:
            #     errors.append(f"This {action} action is not an allowed action.")
            #     continue
            # Check whether mandatory field is written
            else: 
                for prop in mandatory_properties[action]:
                    if prop not in step.attrib:
                        errors.append(
                            f"You must have '{prop}' property when doing '{step.tag}'")
                for attr in step.attrib:
                    if attr not in optional_properties[action]:
                        errors.append(
                            f"The {attr} property in the {action} procedure is not allowed")
                # Check vessels are defined in Hardware
                for attr in ['vessel', 'from_vessel', 'to_vessel']:
                    if attr in step.attrib and step.attrib[attr] not in hardware:
                        errors.append(
                            f"{step.attrib[attr]} is not defined in Hardware")
                # Check reagents are defined in Reagents
                if 'reagent' in step.attrib and step.attrib['reagent'] not in reagents:
                    errors(f"{step.attrib['reagent']} is not defined in Reagents")
                # print errors if exists
            
            if errors:
                # print("Has error")
                print("Error was found in", str(ET.tostring(step, encoding='unicode', method='xml').strip()))
                for error in errors:
                    print("-", error)
                    printed_error_list.append(error)
            # elif errors == []:
            #     print("NO error")


def verify_synthesis(root):
    hardware = parse_hardware(root)
    reagents = parse_reagents(root)
    verify_procedure(root, hardware, reagents)


def verify_xdl(xdl):
    try:
        root = ET.fromstring(xdl)
    except:
        print("Input XDL cannot be parsed as XML")
    verify_synthesis(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    f = open(args.filename, "r")
    xdl = f.read()
    verify_xdl(xdl)





    # unit test

    # has an option of checking whether the reagent and hardware in the allowed list provideds
