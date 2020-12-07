# coding: utf-8

r"""Read and write for weights collections."""

from typing import Tuple
from ydeos_units.units import kg, m, convert
from ydeos_weights.mass import MassesCollection, Mass
from ydeos_weights.position import Position, position2positionm


def load_masses_from_file(filename: str) -> Tuple[MassesCollection, str, str]:
    r"""Load the mass collection from a weights file.

    Parameters
    ----------
    filename : Path to the file
        The file has the following format:
        # comment
        mass_unit, position_unit
        mass_1, x_coordinate_1, y_coordinate_1, z_coordinate_1, name
        mass_2, x_coordinate_2, y_coordinate_2, z_coordinate_2, name
        ...
        mass_n, x_coordinate_n, y_coordinate_n, z_coordinate_n, name

    Returns
    -------
    masses collection, initial_mass_unit, initial_position_unit

    """
    masses = MassesCollection()

    with open(filename) as f:
        # Do not consider comment lines and empty lines
        lines = list(filter(lambda l: not l.startswith("#") and len(l) > 0, f.readlines()))

        # units
        units_data = (lines[0].strip()).split(",")
        initial_mass_unit = units_data[0].strip()
        initial_position_unit = units_data[1].strip()

        # data
        for line in lines[1:]:
            if "{{" not in line:
                # The line is a plain line (i.e. not a templated line)
                parts = (line.strip()).split(",")
                w = float(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                try:
                    name = parts[4].strip()
                except IndexError:
                    name = ""
                kwargs_weight = {initial_mass_unit: w}
                mass_kg = kg(**kwargs_weight)

                position = Position(x, y, z, initial_position_unit)
                position_m = position2positionm(position)

                mass = Mass.from_position_m(mass_kg, position_m, name)
                masses.add_mass(mass)
            else:
                # This is a templated line, do not use it to compute the weights collection
                pass

    return masses, initial_mass_unit, initial_position_unit


def write_to_file(filename: str,
                  masses_collection: MassesCollection,
                  mass_unit="kg",
                  distance_unit="m") -> None:
    r"""Write a weights collection to a CSV weights file."""
    with open(filename, 'w') as f:
        f.write("# mass_unit, position_unit\n")
        f.write("# mass, x, y, z, name\n")
        f.write(f"{mass_unit}, {distance_unit}\n")

        for mass in masses_collection.masses:
            f.write(f"{convert(mass.mass_kg, from_unit='kg', to_unit=mass_unit)}, "
                    f"{convert(mass.cg_m.x, from_unit='m', to_unit=distance_unit)}, "
                    f"{convert(mass.cg_m.y, from_unit='m', to_unit=distance_unit)}, "
                    f"{convert(mass.cg_m.z, from_unit='m', to_unit=distance_unit)}, "
                    f"{mass.name}\n")
