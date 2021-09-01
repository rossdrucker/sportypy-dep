"""Extensions of the BaseFeature class to be specific to baseball fields.

The features are all parameterized by the basic characteristics of an ice rink,
with the default being an NHL ice rink. A user can manually specify their own
field parameters in the BaseballField() class that will adjust the placement of
these features, however the features themselves will be consistent across all
baseball surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseBaseballFeature(BaseFeature):
    """An extension of the BaseFeature class specifically for baseball.

    The following attributes are specific to baseball features only. For more
    information on inherited attributes, please see the BaseFeature class
    definition. The default values are provided to ensure that the feature can
    at least be created, and will default to a regulation NHL ice rink.

    Attributes
    ----------
    feature_radius : float (default: 0.0)
        The radius needed to draw the feature. This may not be needed for all
        features

    feature_thickness : float (default: 0.0)
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed
    """

    def __init__(self, feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = 'ft', *args, **kwargs):

        # Set the full-sized dimensions of the rink
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)


class FieldConstraint(BaseBaseballFeature):
    """Constraint of the field.

    This is simply a pass statement due to the irregular shape of baseball
    fields.
    """

    pass


class HomePlate(BaseBaseballFeature):
    """The design of home plate.
    
    The back tip of home plate is used as the origin of the coordinate system,
    which will be used as a basis for all other measurements and dimensions on
    the field.    
    """

    def __init__(self, home_plate_side_length = 17.0 / 12.0, *args, **kwargs):
        self.home_plate_side_length = home_plate_side_length

        super().__init__(*args, **kwargs)
    
    def _get_centered_feature(self):
        home_plate_df = pd.DataFrame({
            'x': [
                0.0,
                -self.home_plate_side_length / 2.0,
                -self.home_plate_side_length / 2.0,
                self.home_plate_side_length / 2.0,
                self.home_plate_side_length / 2.0,
                0.0
            ],

            'y': [
                0.0,
                np.sqrt(1 - ((self.home_plate_side_length / 2.0) ** 2)),
                np.sqrt(1 - ((self.home_plate_side_length / 2.0) ** 2)) +
                (self.home_plate_side_length / 2.0),
                np.sqrt(1 - ((self.home_plate_side_length / 2.0) ** 2)) +
                (self.home_plate_side_length / 2.0),
                np.sqrt(1 - ((self.home_plate_side_length / 2.0) ** 2)),
                0.0
            ]
        })
        
        return home_plate_df


class Base(BaseBaseballFeature):
    """A base on a baseball diamond.
    
    Bases are typically square in shape, although in the view of the field they
    are typically diamond (e.g. a square rotated 45 degrees).
    """

    def __init__(self, base_side_length = 15.0 / 12.0, *args, **kwargs):
        self.base_side_length = base_side_length

        super().__init__(*args, **kwargs)
    
    def _get_centered_feature(self):
        """Generate the coordinates needed to form a base.

        The base is a rotated square (aka a diamond) with the proper side
        lengths.
        """

        base_df = self.create_diamond(
            height = self.base_side_length * np.sqrt(2) * 0.5,
            width = self.base_side_length * np.sqrt(2) * 0.5
        )

        return base_df

