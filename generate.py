import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import math

rng=np.random.default_rng()
width,height=800,400
pattern_width=150


#pattern_img=Image.open("depthrenders/pattern1.png")
#pattern_img.load()
#pattern_img=pattern_img.resize((pattern_width,height))
#pattern=np.average(np.asarray(pattern_img,dtype="int32"),axis=2)/255
#pattern=pattern.transpose(1,0)
#print(pattern.shape)
pattern=rng.random((pattern_width,height))

img=Image.open("depthrenders/monkey/Image0001.png")
img.load()
img=img.resize((width,height))
imgdata=np.average(np.asarray(img,dtype="int32"),axis=2)/255

def depth(x,y):
    return 1 - imgdata[y,x]*0.2

def get_pattern_at_point(x,y):
    return pattern[round(x)%pattern_width,y]

# Return the pattern if x<0. This essentially seeds the image t
def get_data_at_pos(data,x,y):
    if x<0:
        return get_pattern_at_point(x,y)
    else:
        return data[round(x),y]
#data=np.tile(pattern,(10,1))
data=np.zeros((width,height))
pattern_offset=[0 for x in range(width)]
for x in range(width):
    for y in range(height):
        other_eye_pos=x-depth(x,y)*pattern_width
        data[x,y]=get_data_at_pos(data,other_eye_pos,y)
        #data[x,y]=get_pattern_at_point(x-depth(x,y)*10,y)
        #pattern_offset[y]+=1+depth(x,y)

plt.imshow(data.transpose(1,0),interpolation="nearest")
plt.show()
