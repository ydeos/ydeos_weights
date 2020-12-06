#!/usr/bin/python
# coding: utf-8

r"""Tests for the weights module."""

import pytest
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from aocutils.geom.point import Point
from ydeos_weights.weights import Weight, WeightsCollection, find_corrector
from ydeos_weights.io import load_weights_from_file
from _helpers import path_from_file


def test_total_weight():
    w1 = Weight.from_point(10, Point.from_xyz(2, 3, 4))
    w2 = Weight.from_point(10, Point.from_xyz(2, 3, 4))
    w3 = Weight.from_point(15, Point.from_xyz(2, 3, 4))

    weights = WeightsCollection()
    weights.add_weight(w1)
    weights.add_weight(w2)
    weights.add_weight(w3)

    assert weights.weight == 35


def test_negative_weight():
    r"""Weight with a negative value (here -10)."""
    with pytest.raises(ValueError):
        _ = Weight.from_point(-10, Point.from_xyz(2, 3, 4))


def test_surfacic_weight():
    shell = BRepPrimAPI_MakeBox(10, 10, 10).Shell()
    w = Weight.from_surface_surfacic(surfacic_weight=1, surface=shell).weight
    assert 600 - 1e-6 <= w <= 600 + 1e-6


def test_cg():
    w1 = Weight.from_point(10, Point.from_xyz(2, 5, 20))
    w2 = Weight.from_point(10, Point.from_xyz(10, 5, 30))

    weights = WeightsCollection()
    weights.add_weight(w1)
    weights.add_weight(w2)

    assert weights.weight == 20
    assert weights.point.X() == 6
    assert weights.point.Y() == 5
    assert weights.point.Z() == 25


def test_file():
    data_file_path = path_from_file(__file__, "test_weights_files/weights_new.csv")
    weights, w_unit, p_unit = load_weights_from_file(data_file_path, convert_position_to_meters=True)
    assert weights.weight == 5  # 2500g + 2500g converted  to kilos
    assert weights.point.X() == 0.550  # meters !!
    assert weights.point.Y() == 0.0  # meters !!
    assert weights.point.Z() == -0.2  # meters !!
    assert w_unit == "g"
    assert p_unit == "m"

    weights, w_unit, p_unit = load_weights_from_file(data_file_path, convert_position_to_meters=False)
    assert weights.weight == 5  # 2500g + 2500g converted  to kilos
    assert weights.point.X() == 550.  # not converted to meters
    assert weights.point.Y() == 0.0  # not converted to meters
    assert weights.point.Z() == -200.  # not converted to meters
    assert w_unit == "g"
    assert p_unit == "mm"


def test_find_corrector_weight():
    w1 = Weight.from_point(10, Point.from_xyz(10, 0, -10))
    weights = WeightsCollection()
    weights.add_weight(w1)
    corrector = find_corrector(weights,
                               target_weight=20,
                               target_x=50,
                               target_y=0,
                               target_z=0)
    assert corrector.weight == 10
    assert corrector.point.X() == 90
    assert corrector.point.Y() == 0
    assert corrector.point.Z() == 10

    # should work with the weight instead of the collection
    corrector = find_corrector(w1,
                               target_weight=20,
                               target_x=50,
                               target_y=0,
                               target_z=0)
    assert corrector.weight == 10
    assert corrector.point.X() == 90
    assert corrector.point.Y() == 0
    assert corrector.point.Z() == 10

    w1 = Weight.from_point(10, Point.from_xyz(10, 0, 0))
    weights = WeightsCollection()
    weights.add_weight(w1)
    corrector = find_corrector(weights,
                               target_weight=20,
                               target_x=0,
                               target_y=0,
                               target_z=0)
    assert corrector.weight == 10
    assert corrector.point.X() == -10
    assert corrector.point.Y() == 0
    assert corrector.point.Z() == 0

    w1 = Weight.from_point(10, Point.from_xyz(0, 0, 0))
    weights = WeightsCollection()
    weights.add_weight(w1)
    corrector = find_corrector(weights,
                               target_weight=20,
                               target_x=0,
                               target_y=0,
                               target_z=0)
    assert corrector.weight == 10
    assert corrector.point.X() == 0
    assert corrector.point.Y() == 0
    assert corrector.point.Z() == 0
