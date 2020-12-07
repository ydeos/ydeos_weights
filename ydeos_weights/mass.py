# coding: utf-8

r"""Model for mass, weight and collections of masses / weights.

All masses are modeled using kilograms and meters.

"""

import abc
import logging
from typing import List, Optional, Union
from OCC.Core.TopoDS import TopoDS_Shape
from aocutils.analyze.global_ import GlobalProperties
from aocutils.types_ import topo_lut
from ydeos_units.units import convert
from ydeos_weights.position import Position, PositionM, position2positionm
from ydeos_weights.force import Force
from ydeos_weights.constants import GRAVITY_STANDARD

logger = logging.getLogger(__name__)


class AbstractMass(object):
    r"""Abstract class for mass."""
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def mass_kg(self):
        r"""The mass in [kg]."""
        raise NotImplementedError

    @property
    def weight_N(self):
        r"""The weight in [N]."""
        return self.mass_kg * GRAVITY_STANDARD

    @property
    @abc.abstractmethod
    def cg_m(self):
        r"""Return the point/centre of gravity. Its coordinates are [m]."""
        raise NotImplementedError

    @property
    def force_N_m(self):
        r"""Gravitational force exerted on mass in global coordinates"""
        return Force(fx=0, fy=0, fz=-self.weight_N, px=self.cg_m.x, py=self.cg_m.y, pz=self.cg_m.z)


class Mass(AbstractMass):
    r"""A mass [kg] with a CG position [m] in 3D space."""
    def __init__(self):
        self._mass_kg = 0.
        self._cg_m = None
        self._name = ""

    @classmethod
    def from_position_m(cls, mass_kg: float, cg_m: PositionM, name: str = ""):
        r"""
        Construct a Mass from a mass [kg] and a point/position [m].

        Parameters
        ----------
        mass_kg : mass in kilograms.
        cg_m : CG 3D position in meters [m]
        name : name given to the mass

        """
        if not isinstance(mass_kg, (float, int)):
            msg = "mass_kg should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        if mass_kg < 0.:
            msg = "mass_kg should be positive"
            logger.error(msg)
            raise ValueError(msg)

        if not isinstance(cg_m, PositionM):
            msg = "point_m should be a PositionM instance"
            logger.error(msg)
            raise ValueError(msg)

        obj = cls()
        obj._mass_kg = mass_kg
        obj._cg_m = cg_m
        obj._name = name

        return obj

    @classmethod
    def from_line_linear(cls,
                         linear_mass_kg_per_m: float,
                         linear_entity: TopoDS_Shape,
                         cad_unit: str,
                         name: str = ""):
        r"""Construct a Weight from linear mass [kg / m] and length.

        Parameters
        ----------
        linear_mass_kg_per_m : Linear mass [kg/m]
        linear_entity : An OCC linear shape
        cad_unit : the 1D unit in which the linear_entity Shape is defined.
        name : name given to the mass

        """
        linear_types = GlobalProperties.linear_types
        if topo_lut[linear_entity.ShapeType()] not in linear_types:
            msg = "topo_lut[linear_entity.ShapeType()] should be a linear type"
            logger.error(msg)
            raise AssertionError(msg)
        mass_kg = linear_mass_kg_per_m * convert(GlobalProperties(linear_entity).length,
                                                 from_unit=cad_unit,
                                                 to_unit="m")
        return Mass.from_line_fixed(mass_kg, linear_entity, cad_unit, name)

    @classmethod
    def from_line_fixed(cls,
                        mass_kg: float,
                        linear_entity: TopoDS_Shape,
                        cad_unit: str,
                        name: str = ""):
        r"""Construct a Mass with its CG at the CG of the linear entity.

        Parameters
        ----------
        mass_kg : Total mass [kg]
        linear_entity : An OCC linear shape
        cad_unit : the 1D unit in which the linear_entity Shape is defined.
        name : name given to the mass

        """
        if not isinstance(mass_kg, (float, int)):
            msg = "mass_kg should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        if mass_kg < 0.:
            msg = "mass_kg should be positive or zero"
            logger.error(msg)
            raise ValueError(msg)

        if topo_lut[linear_entity.ShapeType()] not in GlobalProperties.linear_types:
            msg = "linear_entity.ShapeType() should be a linear type"
            logger.error(msg)
            raise ValueError(msg)

        obj = cls()
        obj._mass_kg = mass_kg
        position_gp_pnt = GlobalProperties(linear_entity).centre
        position_m = position2positionm(Position(position_gp_pnt.X(),
                                                 position_gp_pnt.Y(),
                                                 position_gp_pnt.Z(),
                                                 unit=cad_unit))
        obj._cg_m = position_m
        obj._name = name
        return obj

    @classmethod
    def from_surface_surfacic(cls,
                              surfacic_mass_kg_per_m2: float,
                              surface: TopoDS_Shape,
                              cad_unit: str,
                              name: str = ""):
        r"""Construct a Mass from surfacic mass [kg / m2] and surface.

        The CG is at the CG of the surface.

        Parameters
        ----------
        surfacic_mass_kg_per_m2 : Surfacic mass [kg/m2]
        surface : An OCC surfacic shape
        cad_unit : the 1D unit in which the surface Shape is defined.
        name : name given to the mass

        """
        assert topo_lut[surface.ShapeType()] in GlobalProperties.surfacic_types
        mass_kg = surfacic_mass_kg_per_m2 * convert(GlobalProperties(surface).area,
                                                    from_unit=f"{cad_unit}2",
                                                    to_unit="m2")
        return Mass.from_surface_fixed(mass_kg, surface, cad_unit, name)

    @classmethod
    def from_surface_fixed(cls,
                           mass_kg: float,
                           surface: TopoDS_Shape,
                           cad_unit: str,
                           name: str = ""):
        r"""Construct a Mass with its CG at the CG of the surface.

        Parameters
        ----------
        mass_kg : Total mass [kg]
        surface : An OCC surfacic shape
        cad_unit : the 1D unit in which the surface Shape is defined.
        name : name given to the mass

        """
        assert isinstance(mass_kg, (float, int))
        assert(mass_kg >= 0.)
        assert topo_lut[surface.ShapeType()] in GlobalProperties.surfacic_types
        obj = cls()
        obj._mass_kg = mass_kg
        position_gp_pnt = GlobalProperties(surface).centre
        position_m = position2positionm(Position(position_gp_pnt.X(),
                                                 position_gp_pnt.Y(),
                                                 position_gp_pnt.Z(),
                                                 unit=cad_unit))
        obj._cg_m = position_m
        obj._name = name
        return obj

    @classmethod
    def from_volume_volumic(cls,
                            volumic_mass_kg_per_m3: float,
                            volume: TopoDS_Shape,
                            cad_unit: str,
                            name: str):
        r"""Construct a Mass from volumic mass [kg/m3] and volume.

        The CG is at the CG of the volume.

        Parameters
        ----------
        volumic_mass_kg_per_m3 : Volumic mass [kg/m3]
        volume : An OCC volumic shape
        cad_unit : the 1D unit in which the volume Shape is defined.
        name : name given to the mass

        """
        if topo_lut[volume.ShapeType()] not in GlobalProperties.volumic_types:
            msg = "volume.ShapeType() should be of volumic type"
            logger.error(msg)
            raise ValueError(msg)
        mass_kg = volumic_mass_kg_per_m3 * convert(GlobalProperties(volume).volume,
                                                   from_unit=f"{cad_unit}3",
                                                   to_unit="m3")
        return Mass.from_volume_fixed(mass_kg, volume, cad_unit, name)

    @classmethod
    def from_volume_fixed(cls,
                          mass_kg: float,
                          volume: TopoDS_Shape,
                          cad_unit: str,
                          name: str = ""):
        r"""
        Construct a Mass with its CG at the CG of the volume.

        Parameters
        ----------
        mass_kg : Total mass [kg]
        volume : An OCC volumic shape
        cad_unit : the 1D unit in which the volume Shape is defined.
        name : name given to the mass

        """
        assert isinstance(mass_kg, (float, int))
        assert(mass_kg >= 0.)
        assert topo_lut[volume.ShapeType()] in GlobalProperties.volumic_types
        obj = cls()
        obj._mass_kg = mass_kg
        position_gp_pnt = GlobalProperties(volume).centre
        position_m = position2positionm(Position(position_gp_pnt.X(),
                                                 position_gp_pnt.Y(),
                                                 position_gp_pnt.Z(),
                                                 unit=cad_unit))
        obj._cg_m = position_m
        obj._name = name
        return obj

    @property
    def mass_kg(self) -> float:
        r"""Total mass [kg] of the Mass"""
        return self._mass_kg

    @property
    def cg_m(self) -> PositionM:
        r"""Centre of gravity coordinates [m]"""
        return self._cg_m

    @property
    def name(self) -> str:
        r"""Name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Mass <{self.name}> : {self.mass_kg} [kg] @ {self.cg_m.x} {self.cg_m.y} {self.cg_m.z} [m]"


class MassesCollection(AbstractMass):
    r"""A collection of masses."""

    def __init__(self, masses: Optional[List[Mass]] = None):
        if masses is None:
            self._masses = list()
        else:
            if not isinstance(masses, list):
                msg = "masses should be a list or None"
                logger.error(msg)
                raise ValueError(msg)
            for w in masses:
                if not isinstance(w, Mass):
                    msg = "w should be a Mass instance"
                    logger.error(msg)
                    raise ValueError(msg)
            self._masses = masses

    def add_mass(self, mass: Mass) -> None:
        r"""Add a Mass to the collection."""
        if not isinstance(mass, Mass):
            msg = "mass should be a Mass instance"
            logger.error(msg)
            raise ValueError(msg)

        self._masses.append(mass)

    @property
    def masses(self) -> List[Mass]:
        r"""List of masses making up theMassesCollection."""
        return self._masses

    @property
    def mass_kg(self) -> float:
        r"""Total mass [kg] of the collection."""
        return sum([w.mass_kg for w in self._masses])

    @property
    def cg_m(self) -> PositionM:
        r"""Centre of gravity as a gp_Pnt."""
        total_x, total_y, total_z = 0., 0., 0.
        for m in self._masses:
            total_x += m.mass_kg * m.cg_m.x
            total_y += m.mass_kg * m.cg_m.y
            total_z += m.mass_kg * m.cg_m.z
        total_mass = self.mass_kg
        return PositionM(total_x / total_mass, total_y / total_mass, total_z / total_mass)


def find_corrector(masses: Union[Mass, MassesCollection],
                   target_mass_kg: float,
                   target_x_m: float,
                   target_y_m: float,
                   target_z_m: float,
                   override_z: Optional[Union[float, int]] = None) -> Mass:
    r"""
    Find the Mass that has to be added to a Masses collection so that
    the final collection complies with the specified parameters.

    Parameters
    ----------
    masses : MassesCollection or Mass or any implementation of AbstractMass
    target_mass_kg : The final mass when adding the existing mass(es) and the new mass
    target_x_m : The final CG X position [m] of existing mass(s) + new mass
    target_y_m : The final CG Y position [m] of existing mass(s) + new mass
    target_z_m : The final CG Z position [m] of existing mass(s) + new mass
    override_z : A forced position of Z [m] for the new mass
                 (a value of None gets the new mass in its natural position)

    Returns
    -------
    Mass : the mass required to reach the specified mass, x, y and z

    """
    if masses.mass_kg > target_mass_kg:
        msg = f"masses total ({masses.mass_kg:.6f}) should not exceed " \
              f"target_mass ({target_mass_kg:.6f})"
        logger.error(msg)
        raise ValueError(msg)
    corrector_mass_kg = target_mass_kg - masses.mass_kg
    x = ((target_x_m * target_mass_kg) - (masses.mass_kg * masses.cg_m.x)) / corrector_mass_kg
    y = ((target_y_m * target_mass_kg) - (masses.mass_kg * masses.cg_m.y)) / corrector_mass_kg
    z = ((target_z_m * target_mass_kg) - (masses.mass_kg * masses.cg_m.z)) / corrector_mass_kg

    if override_z is None:
        return Mass.from_position_m(corrector_mass_kg, PositionM(x, y, z))
    else:
        # assert isinstance(override_z, float) or isinstance(override_z, int)
        if not isinstance(override_z, (float, int)):
            msg = "override_z should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        return Mass.from_position_m(corrector_mass_kg, PositionM(x, y, override_z))
