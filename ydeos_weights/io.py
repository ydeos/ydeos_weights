# coding: utf-8

r"""Read and write for weights collections."""

from typing import Optional
from aocutils.geom.point import Point
from ydeos_units.units import kg, m
from ydeos_weights.weights import WeightsCollection, Weight


def load_from_file(filename: str, convert_position_to_meters: Optional[bool] = False) -> WeightsCollection:
    r"""Load the weights collection from a weights file.

    Parameters
    ----------
    filename : Path to the file
        The file has the following format:
        # comment
        weight_unit, position_unit
        weight_1, x_coordinate_1, y_coordinate_1, z_coordinate_1, name
        weight_2, x_coordinate_2, y_coordinate_2, z_coordinate_2, name
        ...
        weight_n, x_coordinate_n, y_coordinate_n, z_coordinate_n, name
    convert_position_to_meters : should the XYZ coordinates be converted from position_unit to meters

    """
    weights = WeightsCollection()

    with open(filename) as f:
        # Do not consider comment lines and empty lines
        lines = list(filter(lambda l: not l.startswith("#") and len(l) > 0, f.readlines()))

        # units
        units_data = (lines[0].strip()).split(",")
        weight_unit = units_data[0].strip()
        position_unit = units_data[1].strip()

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
                kwargs_weight = {weight_unit: w}

                if convert_position_to_meters is True:
                    x = m(**{position_unit: x})
                    y = m(**{position_unit: y})
                    z = m(**{position_unit: z})

                weight = Weight.from_point(kg(**kwargs_weight), Point.from_xyz(x, y, z), name)
                weights.add_weight(weight)
            else:
                # This is a templated line, do not use it to compute the weights collection
                pass

    return weights


def write_to_file(filename: str,
                  weights_collection: WeightsCollection,
                  weight_unit="kg",
                  distance_unit="m") -> None:
    r"""Write a weights collection to a CSV weights file."""
    with open(filename, 'w') as f:
        f.write("# weight_unit, position_unit\n")
        f.write("# weight, x, y, z, name\n")
        f.write(f"{weight_unit}, {distance_unit}\n")

        for weight in weights_collection.weights:
            f.write(f"{weight.weight}, {weight.point.x}, {weight.point.y}, {weight.point.z}, {weight.name}\n")