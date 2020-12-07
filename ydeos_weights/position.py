# coding: utf-8

r"""Notion of position across the library."""

import collections
from ydeos_units.units import convert

# Generic position. The unit is specified
Position = collections.namedtuple('Position', 'x y z unit')

# Position where all coordinates are in metres
PositionM = collections.namedtuple('PositionM', 'x y z')


def position2positionm(position):
    r"""Convert a Position (specified unit) to a PositionM (metres)."""
    return PositionM(convert(position.x, from_unit=position.unit, to_unit="m"),
                     convert(position.y, from_unit=position.unit, to_unit="m"),
                     convert(position.z, from_unit=position.unit, to_unit="m"))
