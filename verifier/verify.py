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
            if step.tag not in ['Add', 'Transfer', 'Stir']:
                raise Exception(f"There is no {step.tag} action in XDL")

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
