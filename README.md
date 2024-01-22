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