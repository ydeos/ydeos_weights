#!/usr/bin/python
# coding: utf-8

r"""Tests for the mass module."""

import pytest
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from ydeos_weights.mass import Mass, MassesCollection, find_corrector
from ydeos_weights.position import PositionM, Position
from ydeos_weights.io import load_masses_from_file
from _helpers import path_from_file


def test_total_mass():
    w1 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w2 = Mass.from_position_m(10, PositionM(2, 3, 4))
    w3 = Mass.from_position_m(15, PositionM(2, 3, 4))

    masses = MassesCollection()
    masses.add_mass(w1)
    masses.add_mass(w2)
    masses.add_mass(w3)

    assert masses.mass_kg == 35


def test_negative_weight():
    r"""Weight with a negative value (here -10)."""
    with pytest.raises(ValueError):
        _ = Mass.from_position_m(-10, PositionM(2, 3, 4), allow_negative_mass=False)


def test_surfacic_weight():
    shell = BRepPrimAPI_MakeBox(10, 10, 10).Shell()

    # Cad is defined in m
    w = Mass.from_surface_surfacic(surfacic_mass_kg_per_m2=1, surface=shell, cad_unit='m').mass_kg
    assert 600 - 1e-6 <= w <= 600 + 1e-6

    # Cad is defined in mm
    w = Mass.from_surface_surfacic(surfacic_mass_kg_per_m2=1, surface=shell, cad_unit='mm').mass_kg
    assert 600*1e-6 - 1e-12 <= w <= 600*1e-6 + 1e-12


# TODO : test volumic


def test_cg():
    w1 = Mass.from_position_m(10, PositionM(2, 5, 20))
    w2 = Mass.from_position_m(10, PositionM(10, 5, 30))

    masses = MassesCollection()
    masses.add_mass(w1)
    masses.add_mass(w2)

    assert masses.mass_kg == 20
    assert masses.cg_m.x == 6
    assert masses.cg_m.y == 5
    assert masses.cg_m.z == 25


def test_file():
    data_file_path = path_from_file(__file__, "test_masses_files/masses.csv")
    masses_collection, w_unit, p_unit = load_masses_from_file(data_file_path)
    assert masses_collection.mass_kg == 5  # 2500g + 2500g converted  to kilos
    assert masses_collection.cg_m.x == 0.550  # meters !!
    assert masses_collection.cg_m.y == 0.0  # meters !!
    assert masses_collection.cg_m.z == -0.2  # meters !!
    assert w_unit == "g"
    assert p_unit == "mm"


def test_find_corrector():
    w1 = Mass.from_position_m(10, PositionM(10, 0, -10))
    masses = MassesCollection()
    masses.add_mass(w1)
    corrector = find_corrector(masses,
                               target_mass_kg=20,
                               target_x_m=50,
                               target_y_m=0,
                               target_z_m=0)
    assert corrector.mass_kg == 10
    assert corrector.cg_m.x == 90
    assert corrector.cg_m.y == 0
    assert corrector.cg_m.z == 10

    # should work with the weight instead of the collection
    corrector = find_corrector(w1,
                               target_mass_kg=20,
                               target_x_m=50,
                               target_y_m=0,
                               target_z_m=0)
    assert corrector.mass_kg == 10
    assert corrector.cg_m.x == 90
    assert corrector.cg_m.y == 0
    assert corrector.cg_m.z == 10

    w1 = Mass.from_position_m(10, PositionM(10, 0, 0))
    masses = MassesCollection()
    masses.add_mass(w1)
    corrector = find_corrector(masses,
                               target_mass_kg=20,
                               target_x_m=0,
                               target_y_m=0,
                               target_z_m=0)
    assert corrector.mass_kg == 10
    assert corrector.cg_m.x == -10
    assert corrector.cg_m.y == 0
    assert corrector.cg_m.z == 0

    w1 = Mass.from_position_m(10, PositionM(0, 0, 0))
    masses = MassesCollection()
    masses.add_mass(w1)
    corrector = find_corrector(masses,
                               target_mass_kg=20,
                               target_x_m=0,
                               target_y_m=0,
                               target_z_m=0)
    assert corrector.mass_kg == 10
    assert corrector.cg_m.x == 0
    assert corrector.cg_m.y == 0
    assert corrector.cg_m.z == 0
