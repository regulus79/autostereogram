import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import math
import argparse

parser = argparse.ArgumentParser(
    prog="python generate.py",
    description="Generate Autostereograms from depthmaps"
)

parser.add_argument("input_path",type=str,help="Path to the input depth image.")
parser.add_argument("output_path",type=str,help="Path to where the script should save the autostereogram.")
parser.add_argument("pattern_path",type=str,help="Optional path to the pattern image which the script should use.",nargs="?")
parser.add_argument("--depth-scale",type=float,help="Set the depth scale of the autostereogram (higher value means the shape pops out of the page more) Default: 0.2",nargs="?",default=0.2)
parser.add_argument("--random-pattern-width",type=int,help="Set the width of the random pattern in pixels. Only used when no pattern image is given. Default: image_width//10",nargs="?")

args=parser.parse_args()

input_path=args.input_path
output_path=args.output_path
pattern_path=args.pattern_path
depth_scale=args.depth_scale

rng=np.random.default_rng()

# Load input image from path. Convert to grayscale, since depthmaps only require one channel
img=Image.open(input_path).convert("L")
img.load()

# Save image dimensions for easy access later in program
width,height=img.size

# Convert input image to numpy array
imgdata=np.asarray(img,dtype="int32")/255


# Load/Create the base pattern

pattern=None
random_pattern_width=args.random_pattern_width or width//10 # Default value for random-dot autostereography

# If a path was given for the pattern image, then load it as the base pattern
if pattern_path:
    pattern_img=Image.open(pattern_path)
    pattern_img.load()
    pattern=np.asarray(pattern_img,dtype="int32")
    # Transpose axes, since PIL seems to use h,w instead of w,h
    pattern=pattern.transpose(1,0,2)
else:
    # If no pattern path was provided, then generate random noise as the pattern
    pattern=rng.random((random_pattern_width,height))

# Helper functions
def depth(x,y):
    return 1 - imgdata[y,x]*depth_scale

def get_pattern_at_point(x,y):
    return pattern[round(x)%pattern.shape[0],y%pattern.shape[1],:]

# Return the pattern if x<0. This essentially seeds the image with the pattern outside of view on the left; the pattern may get distorted as the image is constructed from left-to-right.
def get_data_at_pos(data,x,y):
    if x<0:
        return get_pattern_at_point(x,y)
    else:
        return data[round(x),y,:]

# Generate the output image data (TODO: Make this pure numpy and remove the nested for-loops)
data=np.zeros((width,height,3))
for x in range(width):
    for y in range(height):
        # Calculate the position which the other eye should be guided to in order to match the depth
        other_eye_pos=x-depth(x,y)*pattern.shape[0]
        # Set the current pixel to be the same as the pixel which the other eye is looking at.
        data[x,y]=get_data_at_pos(data,other_eye_pos,y)

# Save image to file
output_img=Image.fromarray(data.transpose(1,0,2).astype("uint8"))
output_img.save(output_path)

plt.imshow(data.transpose(1,0,2).astype("uint8"),interpolation="nearest")
plt.show()
