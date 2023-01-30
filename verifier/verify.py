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
            elif step.tag == 'StopStir':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StopStir'")
                for each_attrib in step.attrib:
                    if each_attrib != 'vessel':
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'HeatChill':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'HeatChill'")
                if 'temp' not in step.attrib:
                    raise Exception(f"You must have 'temp' when doing 'HeatChill'")
                if 'time' not in step.attrib:
                    raise Exception(f"You must have 'time' when doing 'HeatChill'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'temp', 'stir', 'stir_speed', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'HeatChillToTemp':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'HeatChillToTemp'")
                if 'temp' not in step.attrib:
                    raise Exception(f"You must have 'temp' when doing 'HeatChillToTemp'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'active', 'temp', 'continue_heatchill', 'stir', 'stir_speed', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'StartHeatChill':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StartHeatChill'")
                if 'temp' not in step.attrib:
                    raise Exception(f"You must have 'temp' when doing 'StartHeatChill'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'temp', 'purpose']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'StopHeatChill':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StopHeatChill'")
                for each_attrib in step.attrib:
                    if each_attrib != 'vessel':
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'EvacuateAndRefill':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'EvacuateAndRefill'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'gas', 'repeats']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Purge':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Purge'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'gas', 'time', 'pressure', 'flow_rate']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'StartPurge':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StartPurge'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'gas', 'pressure', 'flow_rate']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'StopPurge':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'StopPurge'")
                for each_attrib in step.attrib:
                    if each_attrib != 'vessel':
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Filter':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Filter'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'filtrate_vessel', 'stir', 'stir_speed', 'temp', 'continue_heatchill', 'volume']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'FilterThrough':
                if 'from_vessel' not in step.attrib:
                    raise Exception(f"You must have 'from_vessel' when doing 'FilterThrough'")
                if 'to_vessel' not in step.attrib:
                    raise Exception(f"You must have 'to_vessel' when doing 'FilterThrough'")
                if 'through' not in step.attrib:
                    raise Exception(f"You must have 'through' when doing 'FilterThrough'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['from_vessel', 'to_vessel', 'through', 'eluting_solvent', 'eluting_volume', 'eluting_repeats', 'residence_time']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'WashSolid':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'WashSolid'")
                if 'solvent' not in step.attrib:
                    raise Exception(f"You must have 'solvent' when doing 'WashSolid'")
                if 'volume' not in step.attrib:
                    raise Exception(f"You must have 'volume' when doing 'WashSolid'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'solvent', 'volume', 'filtrate_vessel', 'temp', 'stir', 'stir_speed', 'time', 'repeats']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Wait':
                if 'time' not in step.attrib:
                    raise Exception(f"You must have 'time' when doing 'Wait'")
                for each_attrib in step.attrib:
                    if each_attrib != 'time':
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")     
            elif step.tag == 'Repeat':
                if 'repeats' not in step.attrib:
                    raise Exception(f"You must have 'repeats' when doing 'Repeat'")
                if 'children' not in step.attrib:
                    raise Exception(f"You must have 'children' when doing 'Repeat'")
                if 'loop_variables' not in step.attrib:
                    raise Exception(f"You must have 'loop_variables' when doing 'Repeat'")
                if 'iterative' not in step.attrib:
                    raise Exception(f"You must have 'iterative' when doing 'Repeat'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['repeats', 'children', 'loop_variables', 'iterative']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'CleanVessel':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'CleanVessel'")
                if 'solvent' not in step.attrib:
                    raise Exception(f"You must have 'solvent' when doing 'CleanVessel'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'solvent', 'volume', 'temp', 'repeats']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Crystallize':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Crystallize'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'ramp_time', 'ramp_temp']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Dissolve':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Dissolve'")
                if 'solvent' not in step.attrib:
                    raise Exception(f"You must have 'solvent' when doing 'Dissolve'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'solvent', 'volume', 'amount', 'temp', 'time', 'stir_speed']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Dry':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Dry'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'pressure', 'temp', 'continue_heatchill']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Evaporate':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Evaporate'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'pressure', 'temp', 'stir_speed']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Irradiate':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Irradiate'")
                if 'time' not in step.attrib:
                    raise Exception(f"You must have 'time' when doing 'Irradiate'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'wavelength', 'color', 'temp', 'stir', 'stir_speed', 'cooling_power']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'Irradiate':
                if 'vessel' not in step.attrib:
                    raise Exception(f"You must have 'vessel' when doing 'Irradiate'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['vessel', 'time', 'temp', 'stir_speed','reagent', 'volume', 'amount', 'add_time']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'ResetHandling':
                for each_attrib in step.attrib:
                    if each_attrib not in ['solvent', 'volume', 'repeats']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")
            elif step.tag == 'RunColumn':
                if 'from_vessel' not in step.attrib:
                    raise Exception(f"You must have 'from_vessel' when doing 'RunColumn'")
                if 'to_vessel' not in step.attrib:
                    raise Exception(f"You must have 'to_vessel' when doing 'RunColumn'")
                if 'column' not in step.attrib:
                    raise Exception(f"You must have 'column' when doing 'RunColumn'")
                for each_attrib in step.attrib:
                    if each_attrib not in ['from_vessel', 'to_vessel', 'column']:
                        raise Exception(f"The attribute {each_attrib} in the {step.tag} procedure is not allowed")




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



