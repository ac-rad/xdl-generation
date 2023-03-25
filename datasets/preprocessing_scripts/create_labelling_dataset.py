import os
import pandas as pd
import numpy as np
np.random.seed(42)

root1="chemistry_exps_small_output_cleaned"
root2="chemistry_exps_small_xdl_cleaned"
root3="chemistry_exps_small_nlp"

nlp=[]
xdl=[]
ours_loc=[]
path=[]
for rootdir, subdir, filenames in os.walk(root3):
    for filename in sorted(filenames):
        path.append(filename)
        str_ = "XDL #1:::\n"
        coin_flip = np.random.randint(2)
        assert coin_flip in [0, 1]
        ours_loc.append(coin_flip)
        if coin_flip == 0: # our xdl is first
            with open(os.path.join(root1, filename)) as f:
                str_ += f.read()
            str_ +="\n*************************\nXDL #2:::\n"
            with open(os.path.join(root2, filename)) as f:
                str_ += f.read()
        elif coin_flip == 1: # our xdl is second
            with open(os.path.join(root2, filename)) as f:
                str_ += f.read()
            str_ +="\n*************************\nXDL #2:::\n"
            with open(os.path.join(root1, filename)) as f:
                str_ += f.read()
        xdl.append(str_)
        with open(os.path.join(root3, filename)) as f:
            nlp.append(f.read())
data = {"nlp": nlp, "xdl": xdl, "path": path}
df = pd.DataFrame(data)
df.to_csv("xdl_chemistry_exp_dataset_final.csv")

data["ours_loc"]=ours_loc
df = pd.DataFrame(data)
df.to_csv("xdl_chemistry_exp_dataset_final_w_loc.csv")
