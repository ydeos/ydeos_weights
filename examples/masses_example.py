#!/usr/bin/python
# coding: utf-8

r"""Masses example use."""

import logging
from ydeos_weights.io import load_masses_from_file, write_to_file


def main():
    r"""Main function of example"""
    masses, _, _ = load_masses_from_file("./example_mass_files/masses.csv")
    for mass in masses.masses:
        print(mass)
    write_to_file("masses_kg_m.csv", masses)  # will write in kg and m

    # Write the file using g and mm
    write_to_file("masses_g_mm.csv", masses, mass_unit="g", distance_unit="mm")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                               ':: %(lineno)3d :: %(message)s')

    main()
