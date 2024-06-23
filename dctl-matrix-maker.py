#!/usr/bin/env python3

import os.path
from sys import argv
from colour import matrix_colour_correction, read_image
from colour_checker_detection import detect_colour_checkers_segmentation

if len(argv) < 3:
    print("Usage: {} source.exr target.exr [output.dctl]".format(argv[0]))
    exit(1)

source_filename = argv[1]
target_filename = argv[2]

if len(argv) > 3:
    dctl_filename = argv[3]
else:
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dctl_filename = "{}_to_{}_{}.dctl".format(
        source_filename.rsplit(".", 1)[0],
        target_filename.rsplit(".", 1)[0],
        now,
    )

sources = detect_colour_checkers_segmentation(read_image(source_filename))
targets = detect_colour_checkers_segmentation(read_image(target_filename))
if len(sources) != 1 or len(targets) != 1:
    raise Exception(
        "Expected 1 source color checker and 1 target, but found {} sources and {} targets".format(
            len(sources),
            len(targets),
        )
    )
source = sources[0]
target = targets[0]

matrix = matrix_colour_correction(source, target)

dctl = f"""
// {source_filename} to {target_filename}
__DEVICE__ float3 transform(int p_Width, int p_Height, int p_X, int p_Y, float p_R, float p_G, float p_B)
{{
  const float r = (p_R * {matrix[0][0]}f) + (p_G * {matrix[0][1]}f) + (p_B * {matrix[0][2]}f);
  const float g = (p_R * {matrix[1][0]}f) + (p_G * {matrix[1][1]}f) + (p_B * {matrix[1][2]}f);
  const float b = (p_R * {matrix[2][0]}f) + (p_G * {matrix[2][1]}f) + (p_B * {matrix[2][2]}f);
  return make_float3(r, g, b);
}}
"""

print("Matrix:\n", matrix)
print("Writing DCTL to", dctl_filename)
with open(dctl_filename, "w") as f:
    f.write(dctl)
