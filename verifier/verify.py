import argparse
import xml.etree.ElementTree as ET

mandatory_properties = {
    'Add': ['vessel', 'reagent'],
    'Separate': ['purpose', 'product_phase', 'from_vessel', 'separation_vessel', 'to_vessel'],
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
    'CleanVessel': ['vessel'],
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

reagent_properties = ["name", "inchi", "cas", "role", "preserve", "use_for_cleaning", "clean_with", "stir", "temp", "atmosphere", "purity"]


def parse_hardware(root, error_list, available_hardware):
    hardware_list = []
    tag_lst = list(root.iter('Hardware'))
    tags = []
    strs=[]
    error=""
    for item in tag_lst:
        tags += [elem.tag for elem in item.iter()]
        strs += [ET.tostring(item, encoding='unicode', method='xml').strip()]
    for item in tags:
        if item not in ["Hardware", "Component"]:
            error = "The Hardware section should only contain Component tags"
    for hardware in root.iter('Hardware'):
        for component in hardware.iter('Component'):
            if available_hardware:
                if component.attrib['id'] not in available_hardware:
                    wrong_hardware = component.attrib['id']
                    error_str = f"{wrong_hardware} is not defined in the given Hardware list. The available Hardware is: {', '.join(available_hardware)[:-2]}."
                    step_str = ET.tostring(component, encoding='unicode', method='xml').strip()
                    error_list.append({"step": "Hardware definition", "errors": [error_str]})
            hardware_list.append(component.attrib['id'])
    return hardware_list, error_list, (error, strs)


def parse_reagents(root, error_list, available_reagents):
    reagent_list = []
    for reagents in root.iter('Reagents'):
        for reagent in reagents.iter('Reagent'):
            if available_reagents:
                if reagent.attrib['name'] not in available_reagents:
                    wrong_reagent = reagent.attrib['name']
                    error_str = f"{wrong_reagent} is not defined in the given Reagents list. The available reagents are: {', '.join(available_reagents)[:-2]}."
                    error_list.append({"step": "Reagents definition", "errors": [error_str]})
            errors = []
            if 'name' not in reagent.attrib:
                errors.append(f"You must have 'name' property in Reagent")
            else:
                reagent_list.append(reagent.attrib['name'])
            for attr in reagent.attrib:
                if attr not in reagent_properties:
                    errors.append(f"The {attr} property in Reagent is not allowed")
            if errors:
                step_str = ET.tostring(reagent, encoding='unicode', method='xml').strip()
                error_list.append({"step": step_str, "errors": errors})
    return reagent_list

def verify_procedure(root, hardware, reagents, error_list):
    for procedure in root.iter('Procedure'):
        for step in procedure:
            errors = []
            # Check whether action is valid
            action = step.tag
            if action not in mandatory_properties:
                errors.append(f"There is no {action} action in XDL")
            else:
                for prop in mandatory_properties[action]:
                    if prop not in step.attrib:
                        errors.append(
                            f"You must have '{prop}' property when doing '{step.tag}'")
                for attr in step.attrib:
                    if attr not in optional_properties[action]:
                        allowed_actions = list(set(optional_properties[action] + mandatory_properties[action]))
                        errors.append(
                                f"The {attr} property in the {action} procedure is not allowed. The allowed properties are: {', '.join(allowed_actions)}.")
                # Check vessels are defined in Hardware
                #print(error_list)
                if len(error_list) == 0 or "Hardware" not in error_list[0]["step"].lower():
                    for attr in ['vessel', 'from_vessel', 'to_vessel']:
                        if attr in step.attrib and step.attrib[attr] not in hardware:
                            errors.append(
                                f"{step.attrib[attr]} is not defined in Hardware")
                # Check reagents are defined in Reagents
                if 'reagent' in step.attrib and step.attrib['reagent'] not in reagents:
                    reagent_name = step.attrib["reagent"]
                    errors.append(f"{reagent_name} is not defined in Reagents")
            if errors:
                step_str = ET.tostring(step, encoding='unicode', method='xml').strip()
                step_str = ' '.join(step_str.split())
                error_list.append({"step": step_str, "errors": errors})
    return error_list



def verify_synthesis(root, available_hardware, available_reagents):
    error_list = []
    hardware, hardware_list_error_list, (errors, strs) = parse_hardware(root, error_list, available_hardware)
    if errors != "":
        error_list.append({"step": "Hardware definition", "errors": [errors]})

        #return error_list
        #return [{"step": "Hardware definition", "errors": errors}]
    reagents = parse_reagents(root, error_list, available_reagents)
    return verify_procedure(root, hardware, reagents, error_list)

def verify_xdl(xdl, available_hardware=None, available_reagents=None):
    """
    Verify XDL and return errors
    :param xdl: The XDL string to verify
    :return: Returns an empty list if the input is valid. 
             Returns a string if the input cannot be parsed as XML.
             Returns a list of dictionary if it has errors. Each element has two fields.
               "step": The string of the line which contains error.
               "errors": The error messages for that line.
    """
    try:
        root = ET.fromstring(xdl)
    except Exception as e:
        return [{"errors": ["Input XDL cannot be parsed as XML, there is {} error".format(str(e).split(":")[0])]}]
    return verify_synthesis(root, available_hardware, available_reagents)
