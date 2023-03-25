import os

target_dir = "chemistry_exps_small"
#for rootdir, subdirs, filenames in os.walk("chemistry_exps"):
for rootdir, subdirs, filenames in os.walk("chemistry_exps_small_output"):
    for filename in filenames:
        if ".txt" not in filename: continue
        with open(os.path.join(target_dir, filename)) as f:
            exp = f.read()
            #if len(exp) <= 1000:
            with open(os.path.join(target_dir + "_nlp", filename), "w") as g:
                g.write(exp)
