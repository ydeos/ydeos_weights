#!/usr/bin/python
# coding: utf-8

r"""Weights file with a templated line example use.

The templated line is not use to create the weights collection.
This is useful when we want to know how mush weight is already defined in
a weights file before applying a dict to the templated weights file.

"""

from ydeos_weights.io import load_weights_from_file

# convert position to meters
weights, _, _ = load_weights_from_file("./example_weights_files/weights_new_with_templated_line.csv",
                                       convert_position_to_meters=True)

for weight in weights.weights:
    print(f"{weight.name} : {weight.weight} [kg] @ {weight.point.x}, {weight.point.y}, {weight.point.z}")

print(f"Total: {weights.weight} [kg]")
