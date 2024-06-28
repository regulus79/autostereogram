# Autostereogram
A python script for easily generating autostereograms from depth images.

# Usage

`python generate.py <path/to/input> <path/to/output> [<optional/path/to/pattern>] [--depth-scale=<float>, default: 0.2] [--random-pattern-width=<int>, default: 1/10th of image width]`

# Examples

**Depth map:**
<br>
<img alt="depth map of the default Blender monkey 3d model" src="https://github.com/regulus79/autostereogram/blob/main/sample_images/chain_ring.png?raw=true" height=300>
<br>
**Pattern:**
<br>
<img alt="sample pattern of sky and grass" src="https://github.com/regulus79/autostereogram/blob/main/sample_patterns/grass_and_sky.png?raw=true" height=300>
<br>
**Output:**
<br>
<img alt="output autostereograph using the given pattern and depth map" src="https://github.com/regulus79/autostereogram/blob/main/sample_outputs/chain_ring_output_grass_and_sky.png?raw=true" height=500>

# How it works

Similarly to how the [Wikipedia article](https://en.wikipedia.org/wiki/Autostereogram) on the topic describes it, the autostereogram is created from left to right from a repeating pattern. Since the pattern repeats, people can relax their eyes and have them look at two different sections while tricking their brain to think it is one. This works for a flat surface, but more must be done to give the image depth.

To give depth to the autostereogram, one must first realize that the brain will think that an object is closer if the left eye sees it a little to the right and the right eye sees it a little to the left. In other words, the width of the repeating pattern must be less for that object so that the eyes must cross at a closer point in order to see it.

The way this program achieves this is by going column by column left-to-right and calculating for each pixel how far apart the eyes must be given the value of the depth map at the pixel. The pixel is set to be the same as the pixel value where the left eye must look are (if this would end up indexing outside of the image, it instead uses the corresponding pixel from the pattern. This acts to seed the pattern on the left of the image.)