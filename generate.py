import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import math
import sys

assert len(sys.argv)>2, "Please put provide both an input and output path.\nUsage: python generate.py <path to input image/video> <path to output image/video> [<path to pattern image/video>]"

input_path=sys.argv[1]
output_path=sys.argv[2]
pattern_path=sys.argv[3] if len(sys.argv)>3 else None

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
random_pattern_width=width//10 # Default value for random-dot autostereography

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
    return 1 - imgdata[y,x]*0.2

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
