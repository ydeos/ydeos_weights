#!/usr/bin/python
# coding: utf-8

r"""Tests for the weight of a mass."""

from ydeos_weights.mass import Mass, MassesCollection, find_corrector
from ydeos_weights.position import PositionM, Position


def test_total_weight():
    w1 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w2 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w3 = Mass.from_position_m(15, PositionM(2, 3, 4))

    masses = MassesCollection()
    masses.add_mass(w1)
    masses.add_mass(w2)
    masses.add_mass(w3)

    expected_value = 343.23274999999995
    tol = 1e-9
    assert expected_value - tol <= masses.weight_N <= expected_value + tol


def test_find_corrector():
    w1 = Mass.from_position_m(10, PositionM(10, 0, -10))
    masses = MassesCollection()
    masses.add_mass(w1)
    corrector = find_corrector(masses,
                               target_mass_kg=20,
                               target_x_m=50,
                               target_y_m=0,
                               target_z_m=0)
    expected_value = 98.06649999999999
    tol = 1e-9
    assert expected_value - tol <= corrector.weight_N <= expected_value + tol
