# coding: utf-8

r"""Model for weights and collections of weights"""

import abc
import logging
from typing import List, Optional, Union

from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape

from aocutils.analyze.global_ import GlobalProperties
from aocutils.types_ import topo_lut
from aocutils.geom.point import Point

logger = logging.getLogger(__name__)


class AbstractWeight(object):
    r"""Abstract class for weights"""
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def weight(self):
        r"""Return the weight"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def point(self):
        r"""Return the point/centre of gravity"""
        raise NotImplementedError


class Weight(AbstractWeight):
    r"""A weight with a position in 3D space"""
    def __init__(self):
        self._weight = 0.
        self._point = None
        self._name = ""

    @classmethod
    def from_point(cls, weight: float, point: Point, name: str = ""):
        r"""Construct a Weight from a weight and a point/position

        Parameters
        ----------
        weight : unitless weight
        point : 3D position as an aocutils.geom.point.Point object
        name : name given to the weight

        """
        if not isinstance(weight, (float, int)):
            msg = "weight should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        if weight < 0.:
            msg = "weight should be positive"
            logger.error(msg)
            raise ValueError(msg)

        if not isinstance(point, Point):
            msg = "point should be a Point instance"
            logger.error(msg)
            raise ValueError(msg)

        obj = cls()
        obj._weight = weight
        obj._point = point
        obj._name = name

        return obj

    @classmethod
    def from_line_linear(cls, linear_weight: float, linear_entity: TopoDS_Shape, name: str = ""):
        r"""Construct a Weight from linear weight and length with its CG at
        the CG of the linear_entity

        Parameters
        ----------
        linear_weight : Linear weight, i.e. weight per unit length
        linear_entity : An OCC linear shape
        name : name given to the weight

        """
        linear_types = GlobalProperties.linear_types
        if topo_lut[linear_entity.ShapeType()] not in linear_types:
            msg = "topo_lut[linear_entity.ShapeType()] should be a linear type"
            logger.error(msg)
            raise AssertionError(msg)
        weight = linear_weight * GlobalProperties(linear_entity).length
        return Weight.from_line_fixed(weight, linear_entity, name)

    @classmethod
    def from_line_fixed(cls, weight: float, linear_entity: TopoDS_Shape, name: str = ""):
        r"""Construct a Weight with its CG at the CG of the linear entity

        Parameters
        ----------
        weight : Total weight, unitless
        linear_entity : An OCC linear shape
        name : name given to the weight

        """
        if not isinstance(weight, (float, int)):
            msg = "weight should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        if weight < 0.:
            msg = "weight should be positive or zero"
            logger.error(msg)
            raise ValueError(msg)

        if topo_lut[linear_entity.ShapeType()] not in GlobalProperties.linear_types:
            msg = "linear_entity.ShapeType() should be a linear type"
            logger.error(msg)
            raise ValueError(msg)

        obj = cls()
        obj._weight = weight
        obj._point = GlobalProperties(linear_entity).centre
        obj._name = name
        return obj

    @classmethod
    def from_surface_surfacic(cls, surfacic_weight: float, surface: TopoDS_Shape, name: str = ""):
        r"""Construct a Weight from surfacic weight and surface with its CG
        at the CG of the surface

        Parameters
        ----------
        surfacic_weight : Surfacic weight, i.e. weight per unit area
        surface : An OCC surfacic shape
        name : name given to the weight

        """
        assert topo_lut[surface.ShapeType()] in GlobalProperties.surfacic_types
        weight = surfacic_weight * GlobalProperties(surface).area
        return Weight.from_surface_fixed(weight, surface, name)

    @classmethod
    def from_surface_fixed(cls, weight: float, surface: TopoDS_Shape, name: str = ""):
        r"""Construct a Weight with its CG at the CG of the surface

        Parameters
        ----------
        weight : Total weight
        surface : An OCC surfacic shape
        name : name given to the weight

        """
        assert isinstance(weight, (float, int))
        assert(weight >= 0.)
        assert topo_lut[surface.ShapeType()] in GlobalProperties.surfacic_types
        obj = cls()
        obj._weight = weight
        obj._point = GlobalProperties(surface).centre
        obj._name = name
        return obj

    @classmethod
    def from_volume_volumic(cls, volumic_weight: float, volume: TopoDS_Shape, name: str):
        r"""Construct a Weight from volumic weight and volume with its CG at
        the CG of the volume

        Parameters
        ----------
        volumic_weight : Volumic weight, i.e. weight per unit volume
        volume : An OCC volumic shape
        name : name given to the weight

        """
        if topo_lut[volume.ShapeType()] not in GlobalProperties.volumic_types:
            msg = "volume.ShapeType() should be of volumic type"
            logger.error(msg)
            raise ValueError(msg)
        weight = volumic_weight * GlobalProperties(volume).volume
        return Weight.from_volume_fixed(weight, volume, name)

    @classmethod
    def from_volume_fixed(cls, weight: float, volume: TopoDS_Shape, name: str = ""):
        r"""Construct a Weight with its CG at the CG of the volume

        Parameters
        ----------
        weight : Total weight
        volume : An OCC volumic shape
        name : name given to the weight

        """
        assert isinstance(weight, (float, int))
        assert(weight >= 0.)
        assert topo_lut[volume.ShapeType()] in GlobalProperties.volumic_types
        obj = cls()
        obj._weight = weight
        obj._point = GlobalProperties(volume).centre
        obj._name = name
        return obj

    @property
    def weight(self) -> float:
        r"""Total weight of the Weight"""
        return self._weight

    @property
    def point(self) -> Point:
        r"""Centre of gravity as aocutils.geom.point.Point"""
        return self._point

    @property
    def name(self) -> str:
        r"""Name"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class WeightsCollection(AbstractWeight):
    r"""A collection of weights"""

    def __init__(self, weights: Optional[List[Weight]] = None):
        if weights is None:
            self._weights = list()
        else:
            if not isinstance(weights, list):
                msg = "weights should be a list or None"
                logger.error(msg)
                raise ValueError(msg)
            for w in weights:
                if not isinstance(w, Weight):
                    msg = "w should be a Weight instance"
                    logger.error(msg)
                    raise ValueError(msg)
            self._weights = weights

    def add_weight(self, weight: Weight) -> None:
        r""" Add a Weight to the collection"""
        if not isinstance(weight, Weight):
            msg = "weight should be a Weight instance"
            logger.error(msg)
            raise ValueError(msg)

        self._weights.append(weight)

    @property
    def weights(self) -> List[Weight]:
        r"""Return a list of the weights making up the WeightsCollection"""
        return self._weights

    @property
    def weight(self) -> float:
        r"""Total weight of the collection"""
        return sum([w.weight for w in self._weights])

    @property
    def point(self) -> gp_Pnt:
        r"""Centre of gravity as a gp_Pnt"""
        total_x, total_y, total_z = 0., 0., 0.
        for w in self._weights:
            total_x += w.weight * w.point.X()
            total_y += w.weight * w.point.Y()
            total_z += w.weight * w.point.Z()
        return gp_Pnt(total_x / self.weight,
                      total_y / self.weight,
                      total_z / self.weight)


def find_corrector(weights: Union[Weight, WeightsCollection],
                   target_weight: float,
                   target_x: float,
                   target_y: float,
                   target_z: float,
                   override_z: Optional[Union[float, int]] = None) -> Weight:
    r"""Find the Weight that has to be added to a Weights collection so that
    the final collection complies with the specified parameters

    Parameters
    ----------
    weights : WeightsCollection or Weight or any implementation of AbstractWeight
    target_weight : The final weight when adding the existing weight(s) and the new weight
    target_x : The final CG X position of existing weight(s) + new weight
    target_y : The final CG Y position of existing weight(s) + new weight
    target_z : The final CG Z position of existing weight(s) + new weight
    override_z : A forced position of Z for the new weight (a value of None gets the new weight in its natural position)

    Returns
    -------
    Weight : the weight required to reach the specified weight, x, y and z

    """
    if weights.weight > target_weight:
        msg = "weights total (%.4f) should not exceed " \
              "target_weight (%.4f)" % (weights.weight, target_weight)
        logger.error(msg)
        raise ValueError(msg)
    corrector_weight = target_weight - weights.weight
    x = ((target_x * target_weight) - (weights.weight * weights.point.X())) / corrector_weight
    y = ((target_y * target_weight) - (weights.weight * weights.point.Y())) / corrector_weight
    z = ((target_z * target_weight) - (weights.weight * weights.point.Z())) / corrector_weight

    if override_z is None:
        return Weight.from_point(corrector_weight, Point.from_xyz(x, y, z))
    else:
        # assert isinstance(override_z, float) or isinstance(override_z, int)
        if not isinstance(override_z, (float, int)):
            msg = "override_z should be a float or an int"
            logger.error(msg)
            raise ValueError(msg)

        return Weight.from_point(corrector_weight,
                                 Point.from_xyz(x, y, override_z))
