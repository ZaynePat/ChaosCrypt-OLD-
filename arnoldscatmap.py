# PIL for image IO, numpy for array ops
from PIL import Image
from numpy import *
import os
#from scipy.misc import lena,imsave
#from scipy.misc import imsave

# load image
im = array(Image.open("cat.jpg"))
N = im.shape[0]

# Read output directory from external file `output_dir.txt` (created alongside this script).
# If the file is missing or empty, default to a local folder named `arnold_output`.
cfg_path = "output_dir.txt"
if os.path.exists(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as fh:
        output_dir = fh.read().strip() or "arnold_output"
else:
    output_dir = "arnold_output"

os.makedirs(output_dir, exist_ok=True)

# create x and y components of Arnold's cat mapping
x,y = meshgrid(range(N),range(N))
xmap = (2*x+y) % N
ymap = (x+y) % N

for i in range(N+1):
	result = Image.fromarray(im)
	# save each iteration into the configured output directory
	result.save(os.path.join(output_dir, "cat_%03d.png" % i))
	im = im[xmap,ymap]