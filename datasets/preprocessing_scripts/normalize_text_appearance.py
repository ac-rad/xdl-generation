import os
import lxml.etree as etree

from xml.dom import minidom

root1="chemistry_exps_small_output"
root2="chemistry_exps_small_xdl"
root3="chemistry_exps_small_nlp"

os.makedirs("chemistry_exps_small_xdl_cleaned", exist_ok=True)
os.makedirs("chemistry_exps_small_output_cleaned", exist_ok=True)

parser = etree.XMLParser(remove_blank_text=True) 

for rootdir, subdirs, filenames in os.walk(root3):
    for filename in sorted(filenames):

        try:
            parsed_file=parsed_file = etree.parse("{}/{}".format(root1,filename), parser)
            parsed_bytes = (etree.tostring(parsed_file, pretty_print=True))
            parsed_string = str(parsed_bytes, 'utf-8')
            output_file = open("{}_cleaned/{}".format(root1,filename), "w")
            output_file.write(parsed_string)

            #dom = minidom.parse("{}/{}".format(root1,filename))
            #dom.writexml(open("{}_cleaned/{}".format(root1,filename), "w"))

        except:
            with open("{}/{}".format(root1,filename)) as f:
                with open("{}_cleaned/{}".format(root1,filename), "w") as g:
                    g.write(f.read())

        try:
            #dom = minidom.parse("{}/{}".format(root2,filename))
            #dom.writexml(open("{}_cleaned/{}".format(root2,filename), "w"))
            parsed_file=parsed_file = etree.parse("{}/{}".format(root2,filename), parser)
            parsed_bytes = (etree.tostring(parsed_file, pretty_print=True))
            parsed_string = str(parsed_bytes, 'utf-8')
            output_file = open("{}_cleaned/{}".format(root2,filename), "w")
            output_file.write(parsed_string)

        except:
            with open("{}/{}".format(root2,filename)) as f:
                with open("{}_cleaned/{}".format(root2,filename), "w") as g:
                    g.write(f.read())


