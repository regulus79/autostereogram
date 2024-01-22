# Autostereogram
A python script for easily generating autostereograms from depth images.

# Usage

`python generate.py <path/to/input> <path/to/output> [<optional/path/to/pattern>] [--depth-scale=<float>] [--random-pattern-width=<int>]`

The first argument is a path to the input image. Videos as inputs are not yet supported.
The second agument is a path to where the script should save the generated autostereogram.
The third argument is an optional path to the pattern image. If this is left blank, a random noise pattern will be used instead.

There are also optional arguments for setting the depth scale and the width of the randomly generated pattern (if no pattern image is given).