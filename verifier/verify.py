import argparse
import xml.etree.ElementTree as ET 

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
    for procedure in root.iter('Procedure'):
        for step in procedure:
            if step.tag not in ['Add', 'Transfer', 'Stir', 'Separate', 'StartStir', 'StopStir', 'HeatChill', 'HeatChillToTemp', 'StartHeatChill', 'StopHeatChill', 'EvacuateAndRefill', 'Purge', 'StartPurge', 'StopPurge', 'Filter', 'FilterThrough', 'WashSolid', 'Wait', 'Repeat', 'CleanVessel', 'Crystallize', 'Dissolve', 'Dry', 'Evaporate', 'Irradiate', 'Precipitate', 'ResetHandling', 'RunColumn']:
                raise Exception(f"There is no {step.tag} action in XDL")
            if 'vessel' in step.attrib and step.attrib['vessel'] not in hardware:
                raise Exception(f"{step.attrib['vessel']} is not defined in Hardware")
            if 'reagent' in step.attrib and step.attrib['reagent'] not in reagents:
                raise Exception(f"{step.attrib['reagent']} is not defined in Reagents")
                # raise Exception(print(step.attrib['reagent'], "is not defined in Reagents"))
            if step.tag == 'Add':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Add'")
                if 'reagent' not in step.attrib:
                    raise Exception(f"You must have 'reagent' when doing 'Add'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'reagent', 'volume', 'mass', 'amount', 'dropwise', 'time', 'stir', 'stir_speed', 'viscous', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Separate':
                if 'purpose' not in step.attrib:
                    raise Exception(f"You must have 'purpose' when doing 'Separate'")
                if 'product_phase' not in step.attrib:
                    raise Exception(f"You must have 'product_phase' when doing 'Separate'")
                if 'from_vessel' not in step.attrib:
                    raise Exception(f"You must have 'from_vessel' when doing 'Separate'")
                if 'separation_vessel' not in step.attrib:
                    raise Exception(f"You must have 'separation_vessel' when doing 'Separate'")
                if 'to_vessel' not in step.attrib:
                    raise Exception(f"You must have 'to_vessel' when doing 'Separate'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['purpose', 'product_phase', 'from_vessel', 'separation_vessel', 'to_vessel', 'waste_phase_to_vessel', 'solvent', 'solvent_volume', 'through', 'repeats', 'stir_time', 'stir_speed', 'settling_time']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Transfer':
                if 'from_vessel' not in step.attrib:
                    raise Exception(f"You must have 'from_vessel' when doing 'Transfer'")
                if 'to_vessel' not in step.attrib:
                    raise Exception(f"You must have 'to_vessel' when doing 'Transfer'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['from_vessel', 'to_vessel', 'volume', 'amount', 'time', 'viscous', 'rinsing_solvent', 'rinsing_volume', 'rinsing_repeats', 'solid']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'StartStir':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StartStir'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'stir_speed', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")

            elif step.tag == 'Stir':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Stir'")
                if 'time' not in step.attrib:
                    raise Exception(f"You must have 'time' when doing 'Stir'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'stir_speed', 'continue_stirring', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")

# ONE MORE CHANGE




def verify_synthesis(root):
    hardware = parse_hardware(root)
    reagents = parse_reagents(root)
    verify_procedure(root, hardware, reagents)


def verify_xdl(xdl):
    try:
        root = ET.fromstring(xdl)
    except:
        return "Input XDL cannot be parsed as XML"
    try:
        verify_synthesis(root)
    except Exception as e:
        return e
    return "Input XDL is correct!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    f = open(args.filename, "r")
    xdl = f.read()
    print(verify_xdl(xdl))
    # verify_xdl(xdl)


















'''
Questions:
1. difference between XDL and XML
2. difference between print() and f"" in Expection()
'''
