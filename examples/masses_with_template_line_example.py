#!/usr/bin/python
# coding: utf-8

r"""Weights file with a templated line example use.

The templated line is not use to create the weights collection.
This is useful when we want to know how mush weight is already defined in
a weights file before applying a dict to the templated weights file.

"""

from ydeos_weights.io import load_masses_from_file

# The file defines the masses in g and mm
# The loaded masses_collection will be in in kg and m
masses_collection, _, _ = load_masses_from_file("./example_mass_files/masses_with_templated_line.csv")

for mass in masses_collection.masses:
    print(mass)

print(f"Total: {masses_collection.mass_kg} [kg]")
