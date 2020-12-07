#!/usr/bin/python
# coding: utf-8

r"""Tests for the gravitational force of a mass."""

from ydeos_weights.mass import Mass, MassesCollection, find_corrector
from ydeos_weights.position import PositionM, Position


def test_total_force():
    w1 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w2 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w3 = Mass.from_position_m(15, PositionM(2, 3, 4))

    masses = MassesCollection()
    masses.add_mass(w1)
    masses.add_mass(w2)
    masses.add_mass(w3)

    expected_value = -343.23274999999995
    tol = 1e-9
    assert masses.force_N_m.fx == 0
    assert masses.force_N_m.fy == 0
    assert expected_value - tol <= masses.force_N_m.fz <= expected_value + tol


def test_corrector_force():
    w1 = Mass.from_position_m(10, PositionM(10, 0, -10))
    masses = MassesCollection()
    masses.add_mass(w1)
    corrector = find_corrector(masses,
                               target_mass_kg=20,
                               target_x_m=50,
                               target_y_m=0,
                               target_z_m=0)
    expected_value = -98.06649999999999
    tol = 1e-9
    assert corrector.force_N_m.fx == 0
    assert corrector.force_N_m.fy == 0
    assert expected_value - tol <= corrector.force_N_m.fz <= expected_value + tol
    assert corrector.force_N_m.px == 90
    assert corrector.force_N_m.py == 0
    assert corrector.force_N_m.pz == 10
