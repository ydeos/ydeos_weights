#!/usr/bin/python
# coding: utf-8

r"""Weights example use."""

import logging
from ydeos_weights.io import load_from_file, write_to_file


def main():
    # convert position to meters
    weights, _, _ = load_from_file("./example_weights_files/weights_new.csv",
                                   convert_position_to_meters=True)

    for weight in weights.weights:
        print(f"{weight.name} : {weight.weight} [kg] @ {weight.point.x}, {weight.point.y}, {weight.point.z}")

    write_to_file("weights_m.csv", weights, weight_unit="kg", distance_unit="m")

    print("*" * 8)

    # Do not convert position to meters
    weights, _, _ = load_from_file("./example_weights_files/weights_new.csv",
                                   convert_position_to_meters=False)

    for weight in weights.weights:
        print(f"{weight.name} : {weight.weight} [kg] @ {weight.point.x}, {weight.point.y}, {weight.point.z}")

    write_to_file("weights_mm.csv", weights, weight_unit="kg", distance_unit="mm")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                               ':: %(lineno)3d :: %(message)s')

    main()
