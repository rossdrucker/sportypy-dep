"""Extension of the BaseSurfacePlot class to create a hockey rink.

This is a second-level child class of the BaseSurface class, and as such will
have access to its attributes and methods. The default rink will be that of the
NHL, and main leagues will have their own subclass, but a user can manually
specify their own rink parameters to create a totally-customized rink. The
rink's features are parameterized by the basic dimensions of the rink, which
comprise the attributes of the class.

@author: Ross Drucker
"""

import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy.features.hockey_features as hockey
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class HockeyRink(BaseSurfacePlot):
    """A generic hockey rink subclass of BaseSurfacePlot.

    This allows for the creation of the hockey rink in a way that is entirely
    parameterized by the rink's baseline characteristics. The default will be
    the dimensions of an NHL rink. See the class definition for full details.

    Attributes
    ----------
    rotation : float (default: 0.0)
            The angle (in degrees) through which to rotate the final plot

    x_trans : float (default: 0.0)
        The amount that the x coordinates are to be shifted. By convention,
        the +x axis extends from the center of the ice surface towards the
        right-hand goal when viewing the rink in "TV View" (e.g. the rink is
        longer than it is tall)

    y_trans : float (default: 0.0)
        The amount that the y coordinates are to be shifted. By convention,
        the +y axis extends from the center of the ice surface towards the
        top of the rink when viewing the rink in "TV View" (e.g. the rink is
        longer than it is tall)

    rink_length : float (default: 200.0)
        The full length of the rink. Length is defined as the distance
        between the inner edge of the boards behind each goal at its widest
        point (the shorter measurement of the center line's rectangle)

    rink_width : float (default: 85.0)
        The full width of the rink. Width is defined as the distance between
        the inner edge of the boards between the team bench and the penalty
        box on the other side of the ice (the longer measurement of the center
        line's rectangle)

    rink_units : str (default: 'ft')
        The units with which to draw the rink

    nzone_length : float (default: 50.0)
        The length of the neutral zone, measured from the interior edges of
        the zone lines

    corner_radius : float (default: 28.0)
        The radius of the circle that comprise the rink's corners

    faceoff_circle_radius : float (default: 15.0)
        The radius of the faceoff circles, both centered and non-centered, on
        the ice

    faceoff_spot_radius : float (default: 0.5)
        The radius of the faceoff spots, both centered and non-centered, on the
        ice

    board_thickness : float (default: 4")
        The thickness of the boards. This is to give the boundary of the
        rink a clearer-to-see definition, although only the inner edge of
        the boards is considered in play and the boundary of the rink

    major_line_thickness : float (default: 1.0)
        The thickness of the major lines on the ice surface. Major lines are
        considered to be the center line (red line) and blue lines

    minor_line_thickness : float (default: 2.0 / 12)
        The thickness of the minor lines on the ice surface. Minor lines are
        those such as goal lines, hash marks, faceoff markings, or circle
        thicknesses

    goal_line_dist : float (default: 11.0)
        The distance from the end boards to the goal line. Be sure to set the
        'x_justify': and 'y_position' units correctly for this feature
    """

    def __init__(self, rotation = 0.0, x_trans = 0.0, y_trans = 0.0,
                 rink_length = 200.0, rink_width = 85.0, rink_units = 'ft',
                 nzone_length = 50.0, corner_radius = 28.0,
                 faceoff_circle_radius = 15.0,
                 center_faceoff_spot_radius = 0.5,
                 noncenter_faceoff_spot_radius = 1.0,
                 referee_crease_radius = 10.0, board_thickness = (2.0 / 12.0),
                 goal_line_dist = 11.0, goal_crease_radius = 6.0,
                 goal_frame_radius = 20.0 / 12.0,
                 ozone_dzone_faceoff_circle_x = 31.0,
                 ozone_dzone_faceoff_circle_y = 20.5,
                 zone_line_nzone_faceoff_dist_x = 5.0,
                 nzone_faceoff_spot_y = 22.0, major_line_thickness = 1.0,
                 minor_line_thickness = (2.0 / 12.0), colors_dict = None,
                 nzone = {}, ozone = {}, dzone = {}, center_line = {},
                 zone_line = {}, goal_line = {},
                 goalkeepers_restricted_area = {}, center_faceoff_circle = {},
                 ozone_dzone_faceoff_circle = {}, center_faceoff_spot = {},
                 ozone_dzone_faceoff_spot = {},
                 ozone_dzone_faceoff_spot_stripe = {},
                 ozone_dzone_faceoff_line_ul = {},
                 ozone_dzone_faceoff_line_ll = {},
                 ozone_dzone_faceoff_line_lr = {},
                 ozone_dzone_faceoff_line_ur = {},
                 nzone_faceoff_spot = {}, nzone_faceoff_spot_stripe = {},
                 referee_crease = {}, goal_crease_outline = {},
                 goal_crease_fill = {}, goal_frame_outline = {},
                 goal_fill = {}, **added_features):
        # Set the rotation of the plot to be the supplied rotation
        # value
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the rink's necessary shifts. This will overwrite the
        # default values of x_trans and y_trans inherited from the
        # BaseSurfacePlot (which is in turn inherited from BaseSurface)
        self.x_trans = x_trans
        self.y_trans = y_trans

        # Set the full-sized dimensions of the rink along with its
        # units of measure
        self.rink_length = rink_length
        self.rink_width = rink_width
        self.rink_units = rink_units

        # Set the base feature characteristics for the rink
        self.nzone_length = nzone_length
        self.corner_radius = corner_radius
        self.faceoff_circle_radius = faceoff_circle_radius
        self.center_faceoff_spot_radius = center_faceoff_spot_radius
        self.noncenter_faceoff_spot_radius = noncenter_faceoff_spot_radius
        self.board_thickness = board_thickness
        self.major_line_thickness = major_line_thickness
        self.minor_line_thickness = minor_line_thickness
        self.goal_line_dist = goal_line_dist
        self.goal_crease_radius = goal_crease_radius
        self.goal_frame_radius = goal_frame_radius
        self.ozone_dzone_faceoff_circle_x = ozone_dzone_faceoff_circle_x
        self.ozone_dzone_faceoff_circle_y = ozone_dzone_faceoff_circle_y
        self.zone_line_nzone_faceoff_dist_x = zone_line_nzone_faceoff_dist_x
        self.referee_crease_radius = referee_crease_radius

        # Calculate the thickness of both the offensive and defensive
        # zone, as well as the zone lines' positions
        self.ozone_length = (self.rink_length - self.nzone_length) / 2.0
        self.dzone_length = (self.rink_length - self.nzone_length) / 2.0
        self.zone_line_dist = self.nzone_length / 2.0
        self.zone_line_dist += (self.major_line_thickness / 2.0)
        self.nzone_faceoff_spot_x = self.nzone_length / 2.0
        self.nzone_faceoff_spot_x -= zone_line_nzone_faceoff_dist_x
        self.nzone_faceoff_spot_y = nzone_faceoff_spot_y

        # Create a container for the relevant features of an ice rink
        self._features = []

        # Initialize the x and y limits for the plot to be None. These
        # will get set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the standard colors of the rink
        standard_colors = {
            'boards': '#000000',
            'ozone_ice': '#ffffff',
            'nzone_ice': '#ffffff',
            'dzone_ice': '#ffffff',
            'center_line': '#c8102e',
            'zone_line': '#0033a0',
            'goal_line': '#c8102e',
            'goalkeepers_restricted_area': '#c8102e',
            'goal_crease_outline': '#c8102e',
            'goal_crease_fill': '#41b6e6',
            'referee_crease': '#c8102e',
            'center_faceoff_spot': '#0033a0',
            'faceoff_spot_outer_ring': '#c8102e',
            'faceoff_spot_stripe': '#c8102e',
            'center_faceoff_circle': '#0033a0',
            'ozone_dzone_faceoff_circle': '#c8102e',
            'faceoff_line': '#c8102e',
            'goal_frame': '#c8102e',
            'goal_fill': '#a5acaf'
        }

        # Combine the colors with a passed colors dictionary
        if not colors_dict:
            colors_dict = {}

        # Create the final color set for the features
        self.feature_colors = {**standard_colors, **colors_dict}

        # Initialize the boards. These will default to the boards of a
        # regulation NHL rink. NOTE: the zorder is set to be highest
        # here to be plotted over any other features that it may
        # connect with
        board_params = {
            'class': hockey.Boards,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.corner_radius,
            'feature_thickness': self.board_thickness,
            'facecolor': self.feature_colors['boards'],
            'edgecolor': self.feature_colors['boards'],
            'zorder': 100
        }
        self._initialize_feature(board_params)

        # Initialize the constraint on the rink to confine all features
        # to be contained within the boards. The feature itself is not
        # visible (as it's created by the hockey.Boards class)
        boards_constraint_params = {
            'class': hockey.BoardsConstraint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.corner_radius,
            'feature_thickness': self.board_thickness,
            'visible': False
        }
        self._initialize_feature(boards_constraint_params)

        # Set this feature to be the surface's constraint
        self._surface_constraint = self._features.pop(-1)

        # Initialize the neutral zone
        nzone_params = {
            'class': hockey.NeutralZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.nzone_length,
            'visible': True,
            'facecolor': self.feature_colors['nzone_ice'],
            'edgecolor': self.feature_colors['nzone_ice'],
            'zorder': 1
        }
        nzone_params = {**nzone_params, **nzone}
        self._initialize_feature(nzone_params)

        # Initialize the offensive zone
        ozone_params = {
            'class': hockey.OffensiveZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.corner_radius,
            'nzone_length': self.nzone_length,
            'feature_thickness': self.ozone_length,
            'visible': True,
            'facecolor': self.feature_colors['ozone_ice'],
            'edgecolor': self.feature_colors['ozone_ice'],
            'zorder': 1
        }
        ozone_params = {**ozone_params, **ozone}
        self._initialize_feature(ozone_params)

        # Initialize the defensive zone
        dzone_params = {
            'class': hockey.DefensiveZone,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.corner_radius,
            'nzone_length': self.nzone_length,
            'feature_thickness': self.dzone_length,
            'visible': True,
            'facecolor': self.feature_colors['dzone_ice'],
            'edgecolor': self.feature_colors['dzone_ice'],
            'zorder': 1
        }
        dzone_params = {**dzone_params, **dzone}
        self._initialize_feature(dzone_params)

        # Initialize the center line
        center_line_params = {
            'class': hockey.CenterLine,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.major_line_thickness,
            'facecolor': self.feature_colors['center_line'],
            'edgecolor': self.feature_colors['center_line'],
            'zorder': 10
        }
        center_line_params = {**center_line_params, **center_line}
        self._initialize_feature(center_line_params)

        # Initialize the zone line
        zone_line_params = {
            'class': hockey.ZoneLine,
            'x_anchor': self.zone_line_dist,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.major_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['zone_line'],
            'edgecolor': self.feature_colors['zone_line'],
            'zorder': 10
        }
        zone_line_params = {**zone_line_params, **zone_line}
        self._initialize_feature(zone_line_params)

        # Initialize the goal lines
        goal_line_params = {
            'class': hockey.GoalLine,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_anchor': (self.rink_length / 2.0) - self.goal_line_dist,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.corner_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['goal_line'],
            'edgecolor': self.feature_colors['goal_line'],
            'zorder': 10
        }
        goal_line_params = {**goal_line_params, **goal_line}
        self._initialize_feature(goal_line_params)

        # Initialize the goalkeeper's restricted area
        goalkeepers_restricted_area_params = {
            'class': hockey.GoalkeepersRestrictedArea,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_x': -(self.rink_length / 2.0) + self.goal_line_dist,
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.goal_frame_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': False,
            'edgecolor': self.feature_colors['goalkeepers_restricted_area'],
            'facecolor': self.feature_colors['goalkeepers_restricted_area'],
            'zorder': 10
        }
        goalkeepers_restricted_area_params = {
            **goalkeepers_restricted_area_params,
            **goalkeepers_restricted_area
        }
        self._initialize_feature(goalkeepers_restricted_area_params)

        # Initialize the center faceoff circle
        center_faceoff_circle_params = {
            'class': hockey.CenterFaceoffCircle,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.faceoff_circle_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['center_faceoff_circle'],
            'edgecolor': self.feature_colors['center_faceoff_circle'],
            'zorder': 20
        }
        center_faceoff_circle_params = {
            **center_faceoff_circle_params,
            **center_faceoff_circle
        }
        self._initialize_feature(center_faceoff_circle_params)

        # Initialize the offensive and defensive zone faceoff circles
        ozone_dzone_faceoff_circle_params = {
            'class': hockey.OzoneDzoneFaceoffCircle,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'hashmark_width': 2.0,
            'hashmark_ext_spacing': (71.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.faceoff_circle_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['ozone_dzone_faceoff_circle'],
            'edgecolor': self.feature_colors['ozone_dzone_faceoff_circle'],
            'zorder': 10
        }
        ozone_dzone_faceoff_circle_params = {
            **ozone_dzone_faceoff_circle_params,
            **ozone_dzone_faceoff_circle
        }
        self._initialize_feature(ozone_dzone_faceoff_circle_params)

        # Initialize the center faceoff spot
        center_faceoff_spot_params = {
            'class': hockey.CenterFaceoffSpot,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.center_faceoff_spot_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['center_faceoff_spot'],
            'edgecolor': self.feature_colors['center_faceoff_spot'],
            'zorder': 20
        }
        center_faceoff_spot_params = {
            **center_faceoff_spot_params,
            **center_faceoff_spot
        }
        self._initialize_feature(center_faceoff_spot_params)

        # Initialize the offensive and defensive zone faceoff spots
        ozone_dzone_faceoff_spot_params = {
            'class': hockey.NonCenterFaceoffSpot,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.noncenter_faceoff_spot_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_spot_outer_ring'],
            'edgecolor': self.feature_colors['faceoff_spot_outer_ring'],
            'zorder': 10
        }
        ozone_dzone_faceoff_spot_params = {
            **ozone_dzone_faceoff_spot_params,
            **ozone_dzone_faceoff_spot
        }
        self._initialize_feature(ozone_dzone_faceoff_spot_params)

        # Initialize the offensive and defensive zone faceoff spot stripes
        ozone_dzone_faceoff_spot_stripe_params = {
            'class': hockey.NonCenterFaceoffSpotStripe,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'gap_width': (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.noncenter_faceoff_spot_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_spot_stripe'],
            'edgecolor': self.feature_colors['faceoff_spot_stripe'],
            'zorder': 11
        }
        ozone_dzone_faceoff_spot_stripe_params = {
            **ozone_dzone_faceoff_spot_stripe_params,
            **ozone_dzone_faceoff_spot_stripe
        }
        self._initialize_feature(ozone_dzone_faceoff_spot_stripe_params)

        # Initialize the markings around the offensive and defensive zone
        # faceoff spots. This is for the upper-left L
        ozone_dzone_faceoff_line_ul_params = {
            'class': hockey.FaceoffLines,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'dist_from_spot_x': 2.0,
            'dist_from_spot_y': 9.0 / 12.0,
            'over_x': False,
            'over_y': False,
            'feature_length': 4.0,
            'feature_width': 3.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_line'],
            'edgecolor': self.feature_colors['faceoff_line'],
            'zorder': 10
        }
        ozone_dzone_faceoff_line_ul_params = {
            **ozone_dzone_faceoff_line_ul_params,
            **ozone_dzone_faceoff_line_ul
        }
        self._initialize_feature(ozone_dzone_faceoff_line_ul_params)

        # Initialize the markings around the offensive and defensive zone
        # faceoff spots. This is for the lower-left L
        ozone_dzone_faceoff_line_ll_params = {
            'class': hockey.FaceoffLines,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'dist_from_spot_x': 2.0,
            'dist_from_spot_y': 9.0 / 12.0,
            'over_x': True,
            'over_y': False,
            'feature_length': 4.0,
            'feature_width': 3.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_line'],
            'edgecolor': self.feature_colors['faceoff_line'],
            'zorder': 10
        }
        ozone_dzone_faceoff_line_ll_params = {
            **ozone_dzone_faceoff_line_ll_params,
            **ozone_dzone_faceoff_line_ll
        }
        self._initialize_feature(ozone_dzone_faceoff_line_ll_params)

        # Initialize the markings around the offensive and defensive zone
        # faceoff spots. This is for the lower-right L
        ozone_dzone_faceoff_line_lr_params = {
            'class': hockey.FaceoffLines,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'dist_from_spot_x': 2.0,
            'dist_from_spot_y': 9.0 / 12.0,
            'over_x': True,
            'over_y': True,
            'feature_length': 4.0,
            'feature_width': 3.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_line'],
            'edgecolor': self.feature_colors['faceoff_line'],
            'zorder': 10
        }
        ozone_dzone_faceoff_line_lr_params = {
            **ozone_dzone_faceoff_line_lr_params,
            **ozone_dzone_faceoff_line_lr
        }
        self._initialize_feature(ozone_dzone_faceoff_line_lr_params)

        # Initialize the markings around the offensive and defensive zone
        # faceoff spots. This is for the upper-right L
        ozone_dzone_faceoff_line_ur_params = {
            'class': hockey.FaceoffLines,
            'x_anchor': (self.rink_length / 2.0) -
            self.ozone_dzone_faceoff_circle_x,
            'y_anchor': (self.rink_width / 2.0) -
            self.ozone_dzone_faceoff_circle_y,
            'dist_from_spot_x': 2.0,
            'dist_from_spot_y': 9.0 / 12.0,
            'over_x': False,
            'over_y': True,
            'feature_length': 4.0,
            'feature_width': 3.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_line'],
            'edgecolor': self.feature_colors['faceoff_line'],
            'zorder': 10
        }
        ozone_dzone_faceoff_line_ur_params = {
            **ozone_dzone_faceoff_line_ur_params,
            **ozone_dzone_faceoff_line_ur
        }
        self._initialize_feature(ozone_dzone_faceoff_line_ur_params)

        # Initialize the neutral zone faceoff spots
        nzone_faceoff_spot_params = {
            'class': hockey.NonCenterFaceoffSpot,
            'x_anchor': self.nzone_faceoff_spot_x,
            'y_anchor': self.nzone_faceoff_spot_y,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.noncenter_faceoff_spot_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_spot_outer_ring'],
            'edgecolor': self.feature_colors['faceoff_spot_outer_ring'],
            'zorder': 10
        }
        nzone_faceoff_spot_params = {
            **nzone_faceoff_spot_params,
            **nzone_faceoff_spot
        }
        self._initialize_feature(nzone_faceoff_spot_params)

        # Initialize the neutral zone faceoff spot stripes
        nzone_faceoff_spot_stripe_params = {
            'class': hockey.NonCenterFaceoffSpotStripe,
            'x_anchor': self.nzone_faceoff_spot_x,
            'y_anchor': self.nzone_faceoff_spot_y,
            'gap_width': (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.noncenter_faceoff_spot_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['faceoff_spot_stripe'],
            'edgecolor': self.feature_colors['faceoff_spot_stripe'],
            'zorder': 11
        }
        nzone_faceoff_spot_stripe_params = {
            **nzone_faceoff_spot_stripe_params,
            **nzone_faceoff_spot_stripe
        }
        self._initialize_feature(nzone_faceoff_spot_stripe_params)

        # Initialize the referee's crease
        referee_crease_params = {
            'class': hockey.RefereeCrease,
            'x_anchor': 0.0,
            'y_anchor': -self.rink_width / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.referee_crease_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['referee_crease'],
            'edgecolor': self.feature_colors['referee_crease'],
            'zorder': 20
        }
        referee_crease_params = {
            **referee_crease_params,
            **referee_crease
        }
        self._initialize_feature(referee_crease_params)

        # Initialize the goal crease's outline
        goal_crease_outline_params = {
            'class': hockey.GoalCreaseOutline,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_x': -(self.rink_length / 2.0) + self.goal_line_dist,
            'goal_crease_length': 4.5,
            'goal_crease_width': 4.0,
            'crease_notch_dist': 4.0,
            'crease_notch_width': (5.0 / 12.0),
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.goal_crease_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['goal_crease_outline'],
            'edgecolor': self.feature_colors['goal_crease_outline'],
            'zorder': 10
        }
        goal_crease_outline_params = {
            **goal_crease_outline_params,
            **goal_crease_outline
        }
        self._initialize_feature(goal_crease_outline_params)

        # Initialize the goal crease's fill
        goal_crease_fill_params = {
            'class': hockey.GoalCreaseFill,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_x': -(self.rink_length / 2.0) + self.goal_line_dist,
            'goal_crease_length': 4.5,
            'goal_crease_width': 4.0,
            'crease_notch_dist': 4.0,
            'crease_notch_width': (5.0 / 12.0),
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.goal_crease_radius,
            'feature_thickness': self.minor_line_thickness,
            'visible': True,
            'facecolor': self.feature_colors['goal_crease_fill'],
            'edgecolor': self.feature_colors['goal_crease_fill'],
            'zorder': 9
        }
        goal_crease_fill_params = {
            **goal_crease_fill_params,
            **goal_crease_fill
        }
        self._initialize_feature(goal_crease_fill_params)

        # Initialize the goal frame outline
        goal_frame_outline_params = {
            'class': hockey.GoalFrame,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_x': -(self.rink_length / 2.0) + self.goal_line_dist,
            'goal_mouth_interior_width': 6.0,
            'goal_depth': 40.0 / 12.0,
            'goal_post_diameter': 2.375 / 12,
            'feature_unit': 'ft',
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.goal_frame_radius,
            'feature_thickness': 1.9 / 12.0,
            'visible': True,
            'edgecolor': self.feature_colors['goal_frame'],
            'facecolor': self.feature_colors['goal_frame'],
            'zorder': 10
        }
        goal_frame_outline_params = {
            **goal_frame_outline_params,
            **goal_frame_outline
        }
        self._initialize_feature(goal_frame_outline_params)

        # Initialize the goal fill
        goal_fill_params = {
            'class': hockey.GoalFill,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'goal_line_x': -(self.rink_length / 2.0) + self.goal_line_dist,
            'goal_mouth_interior_width': 6.0,
            'goal_depth': 40.0 / 12.0,
            'goal_post_diameter': 2.375 / 12,
            'feature_unit': 'ft',
            'reflect_x': True,
            'reflect_y': False,
            'rink_length': self.rink_length,
            'rink_width': self.rink_width,
            'feature_radius': self.goal_frame_radius,
            'feature_thickness': 1.9 / 12.0,
            'visible': True,
            'edgecolor': self.feature_colors['goal_fill'],
            'facecolor': self.feature_colors['goal_fill'],
            'zorder': 10
        }
        goal_fill_params = {
            **goal_fill_params,
            **goal_fill
        }
        self._initialize_feature(goal_fill_params)

    def draw(self, ax = None, display_range = 'full', xlim = None, ylim = None,
             rotation = None):
        """Draw the rink.

        Parameters
        ----------
        ax : matplotlib.Axes
            An axes object onto which the plot can be drawn. If None is
            supplied, then the currently-active Axes object will be used

        display_range : str; default "full"
            The portion of the surface to display. The entire surface
            will always be drawn under the hood, however this parameter
            limits what is shown in the final plot. The following explain what
            each display range corresponds to:

            'full' : the entire ice surface

            'offense' : the offensive (TV-right) half of the ice surface

            'offence' : the offensive (TV-right) half of the ice surface

            'defense' : the defensive (TV-left) half of the ice surface

            'defence' : the defensive (TV-left) half of the ice surface

            'nzone' : the neutral zone (the area between the zone lines)

            'neutral' : the neutral zone (the area between the zone lines)

            'neutral_zone' : the neutral zone (the area between the zone lines)

            'neutral zone' : the neutral zone (the area between the zone lines)

            'ozone' : the offensive zone. This is the area (TV-right) of the
                neutral zone

            'offensive_zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'offensive zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'attacking_zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'attacking zone' : the offensive zone. This is the area (TV-right)
                of the neutral zone

            'dzone' : the defensive zone. This is the area (TV-left) of the
                neutral zone

            'defensive_zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defensive zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defending_zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

            'defending zone' : the defensive zone. This is the area (TV-left)
                of the neutral zone

        xlim : float, tuple (float, float), or None (default: None)
            The display range in the x direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the x coordinates to display and the upper bound will be the
            +x end of the boards. If a tuple, the two values will be
            used to determine the bounds. If None, then the
            display_range will be used instead to set the bounds

        ylim : float, tuple (float, float), or None (default: None)
            The display range in the y direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the y coordinates to display and the upper bound will be the
            +y side of the rink. If a tuple, the two values will be used
            to determine the bounds. If None, then the display_range
            will be used instead to set the bounds

        rotation : float or None (default: None)
            Angle (in degrees) through which to rotate the rink when
            drawing. If used, this will set the class attribute of
            self._rotation. A value of 0.0 will correspond to a TV View
            of the rink, where +x is to the right and +y is on top. The
            rotation occurs counter clockwise
        """
        # If there is a rotation to be applied, apply it first and set it as
        # the class attribute self._rotation
        if rotation:
            self._rotation = Affine2D().rotate_deg(rotation)

        # If an Axes object is not provided, create one to use for plotting
        if ax is None:
            fig, ax = plt.subplots()
            fig.set_size_inches(50, 50)
            ax = plt.gca()

        # Set the aspect ratio to be equal and remove the axis to leave only
        # the plot
        ax.set_aspect('equal')
        ax.axis('off')

        # Get the transformation to apply
        transform = self._get_transform(ax)

        # Add each feature
        for feature in self._features:
            # Start by adding the feature to the current Axes object
            feature.draw(ax, transform)

            try:
                # Check the feature's visibility
                visible = feature.visible
            except AttributeError:
                # If the feature doesn't have a visible attribute, set its
                # visibility to be true by default
                visible = True

            # Assuming the feature is visible (and is not the boards), get
            # the feature's x and y limits to ensure it lies within the
            # bounds of the rink
            if visible and not isinstance(feature, hockey.Boards):
                try:
                    feature_df = feature._translate_feature()

                    # If the feature doesn't have a limitation on x, set its
                    # limits to be its minimum and maximum values of x
                    if self._feature_xlim is None:
                        self._feature_xlim = [
                            feature_df['x'].min(),
                            feature_df['x'].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest x value or the larger
                    # of its specified maximum and largest x value
                    else:
                        self._feature_xlim = [
                            min(self._feature_xlim[0], feature_df['x'].min()),
                            max(self._feature_xlim[0], feature_df['x'].max())
                        ]

                    # If the feature doesn't have a limitation on y, set its
                    # limits to be its minimum and maximum values of y
                    if self._feature_ylim is None:
                        self._feature_ylim = [
                            feature_df['y'].min(),
                            feature_df['y'].max()
                        ]

                    # Otherwise, set the limits to be the smaller of its
                    # specified minimum and smallest y value or the larger
                    # of its specified maximum and largest y value
                    else:
                        self._feature_ylim = [
                            min(self._feature_ylim[0], feature_df['y'].min()),
                            max(self._feature_ylim[0], feature_df['y'].max())
                        ]

                except TypeError:
                    # If there is an error with the above process, do not
                    # set the x and y limits
                    pass

        # Set the plot's display range
        ax = self.set_plot_display_range(ax, display_range, xlim, ylim)

        return ax

    def _get_plot_range_limits(self, display_range = 'full', xlim = None,
                               ylim = None):
        """Get the x and y limits for the displayed plot.

        Parameters
        ----------
            display_range : str (default: 'full')
                The range of which to display the plot. This is a key that will
                be searched for in the ranges_dict parameter

            xlim : float or None (default: None)
                A specific limit on x for the plot

            ylim : float or None (default: None)
                A specific limit on y for the plot

        Returns
        -------
            xlim : tuple
                The x-directional limits for displaying the plot
            ylim : tuple
                The y-directional limits for displaying the plot
        """
        # Copy the supplied xlim and ylim parameters so as not to overwrite
        # the initial memory
        xlim = self.copy_(xlim)
        ylim = self.copy_(ylim)

        # Determine the length of half of the rink (including the thickness of
        # the boards)
        half_rink_length = (self.rink_length / 2) + self.board_thickness + 1
        half_rink_width = (self.rink_width / 2) + self.board_thickness + 1
        half_nzone_length = (self.nzone_length / 2) + self.major_line_thickness
        half_nzone_length += 1

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                'full': (-half_rink_length, half_rink_length),

                # Half-rink plots
                'offense': (0, half_rink_length),
                'offence': (0, half_rink_length),
                'defense': (-half_rink_length, 0),
                'defence': (-half_rink_length, 0),

                # Neutral zone
                'nzone': (-half_nzone_length, half_nzone_length),
                'neutral': (-half_nzone_length, half_nzone_length),
                'neutral_zone': (-half_nzone_length, half_nzone_length),
                'neutral zone': (-half_nzone_length, half_nzone_length),

                # Offensive zone
                'ozone': (half_nzone_length - 1, half_rink_length),
                'offensive_zone': (half_nzone_length - 1, half_rink_length),
                'offensive zone': (half_nzone_length - 1, half_rink_length),
                'attacking_zone': (half_nzone_length - 1, half_rink_length),
                'attacking zone': (half_nzone_length - 1, half_rink_length),

                # Defensive zone
                'dzone': (-half_rink_length, -half_nzone_length + 1),
                'defensive_zone': (-half_rink_length, -half_nzone_length + 1),
                'defensive zone': (-half_rink_length, -half_nzone_length + 1),
                'defending_zone': (-half_rink_length, -half_nzone_length + 1),
                'defending zone': (-half_rink_length, -half_nzone_length + 1)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # rink
            xlim = xlims.get(
                display_range,
                (-half_rink_length, half_rink_length)
            )

        # If an x limit is provided, try to use it
        else:
            try:
                xlim = (xlim[0] - self.x_shift, xlim[1] - self.x_shift)

            # If the limit provided is not a tuple, use the provided value as
            # best as possible. This will set the provided value as the lower
            # limit of x, and display any x values greater than it
            except TypeError:
                # Apply the necessary shift to align the plot limit with the
                # data
                xlim = xlim - self.x_shift

                # If the provided value for the x limit is beyond the end of
                # the boards, display the entire rink
                if xlim >= half_rink_length:
                    xlim = -half_rink_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_rink_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the rink. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                'full': (-half_rink_width, half_rink_width),

                # Half-rink plots
                'offense': (-half_rink_width, half_rink_width),
                'offence': (-half_rink_width, half_rink_width),
                'defense': (-half_rink_width, half_rink_width),
                'defence': (-half_rink_width, half_rink_width),

                # Neutral zone
                'nzone': (-half_rink_width, half_rink_width),
                'neutral': (-half_rink_width, half_rink_width),
                'neutral_zone': (-half_rink_width, half_rink_width),
                'neutral zone': (-half_rink_width, half_rink_width),

                # Offensive zone
                'ozone': (-half_rink_width, half_rink_width),
                'offensive_zone': (-half_rink_width, half_rink_width),
                'offensive zone': (-half_rink_width, half_rink_width),
                'attacking_zone': (-half_rink_width, half_rink_width),
                'attacking zone': (-half_rink_width, half_rink_width),

                # Defensive zone
                'dzone': (-half_rink_width, half_rink_width),
                'defensive_zone': (-half_rink_width, half_rink_width),
                'defensive zone': (-half_rink_width, half_rink_width),
                'defending_zone': (-half_rink_width, half_rink_width),
                'defending zone': (-half_rink_width, half_rink_width)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # rink
            ylim = ylims.get(
                display_range,
                (-half_rink_length, half_rink_length)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_shift, ylim[1] - self.y_shift)

            except TypeError:
                ylim = ylim - self.y_shift

                if ylim >= half_rink_width:
                    ylim = -half_rink_width

                ylim = (ylim, half_rink_width)

        # Smaller coordinate should always go first
        if xlim[0] > xlim[1]:
            xlim = (xlim[1], xlim[0])
        if ylim[0] > ylim[1]:
            ylim = (ylim[1], ylim[0])

        # Constrain the limits from going beyond the end of the rink (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_rink_length),
            min(xlim[1], half_rink_length)
        )

        ylim = (
            max(ylim[0], -half_rink_width),
            min(ylim[1], half_rink_width)
        )

        return xlim, ylim


class IIHFRink(HockeyRink):
    """A regulation IIHF (International Ice Hockey Federation) rink.

    Please see the HockeyRink class definition for full details.
    """

    def __init__(self, rink_length = 60.0, rink_width = 30.0,
                 rink_units = 'm', nzone_length = 14.28, corner_radius = 8.5,
                 faceoff_circle_radius = 4.5,
                 center_faceoff_spot_radius = 0.15,
                 noncenter_faceoff_spot_radius = 0.3,
                 referee_crease_radius = 3.0, board_thickness = 0.05,
                 goal_line_dist = 4.0, goal_crease_radius = 1.83,
                 goal_frame_radius = 0.508,
                 ozone_dzone_faceoff_circle_x = 10.0,
                 ozone_dzone_faceoff_circle_y = 8.0,
                 zone_line_nzone_faceoff_dist_x = 1.5,
                 nzone_faceoff_spot_y = 7.0, major_line_thickness = 0.3,
                 minor_line_thickness = 0.05,
                 **kwargs):
        kwargs['rink_length'] = rink_length
        kwargs['rink_width'] = rink_width
        kwargs['rink_units'] = rink_units
        kwargs['nzone_length'] = nzone_length
        kwargs['corner_radius'] = corner_radius
        kwargs['faceoff_circle_radius'] = faceoff_circle_radius
        kwargs['center_faceoff_spot_radius'] = center_faceoff_spot_radius
        kwargs['noncenter_faceoff_spot_radius'] = noncenter_faceoff_spot_radius
        kwargs['referee_crease_radius'] = referee_crease_radius
        kwargs['board_thickness'] = board_thickness
        kwargs['goal_line_dist'] = goal_line_dist
        kwargs['goal_crease_radius'] = goal_crease_radius
        kwargs['goal_frame_radius'] = goal_frame_radius
        kwargs['ozone_dzone_faceoff_circle_x'] = ozone_dzone_faceoff_circle_x
        kwargs['ozone_dzone_faceoff_circle_y'] = ozone_dzone_faceoff_circle_y
        kwargs['zone_line_nzone_faceoff_dist_x'] =\
            zone_line_nzone_faceoff_dist_x
        kwargs['nzone_faceoff_spot_y'] = nzone_faceoff_spot_y
        kwargs['major_line_thickness'] = major_line_thickness
        kwargs['minor_line_thickness'] = minor_line_thickness

        kwargs['ozone_dzone_faceoff_spot_stripe'] = {
            'gap_width': 0.075
        }

        kwargs['nzone_faceoff_spot_stripe'] = {
            'gap_width': 0.075
        }

        kwargs['ozone_dzone_faceoff_line_ul'] = {
            'dist_from_spot_x': 0.6,
            'dist_from_spot_y': 0.225,
            'feature_length': 1.2,
            'feature_width': 0.9
        }

        kwargs['ozone_dzone_faceoff_line_ll'] = {
            'dist_from_spot_x': 0.6,
            'dist_from_spot_y': 0.225,
            'feature_length': 1.2,
            'feature_width': 0.9
        }

        kwargs['ozone_dzone_faceoff_line_lr'] = {
            'dist_from_spot_x': 0.6,
            'dist_from_spot_y': 0.225,
            'feature_length': 1.2,
            'feature_width': 0.9
        }

        kwargs['ozone_dzone_faceoff_line_ur'] = {
            'dist_from_spot_x': 0.6,
            'dist_from_spot_y': 0.225,
            'feature_length': 1.2,
            'feature_width': 0.9
        }

        kwargs['ozone_dzone_faceoff_circle'] = {
            'hashmark_width': 0.6,
            'hashmark_ext_spacing': 1.8,
        }

        kwargs['goal_crease_outline'] = {
            'goal_crease_length': 1.37,
            'goal_crease_width': 1.22,
            'crease_notch_dist': 1.32,
            'crease_notch_width': 0.13,
        }

        kwargs['goal_crease_fill'] = {
            'goal_crease_length': 1.37,
            'goal_crease_width': 1.22,
            'crease_notch_dist': 1.32,
            'crease_notch_width': 0.13,
        }

        kwargs['goal_frame_outline'] = {
            'goal_mouth_interior_width': 1.83,
            'goal_depth': 1.12,
            'goal_post_diameter': 0.05,
            'feature_thickness': 0.1,
            'feature_unit': 'm'
        }

        kwargs['goal_fill'] = {
            'goal_mouth_interior_width': 1.83,
            'goal_depth': 1.12,
            'goal_post_diameter': 0.05,
            'feature_thickness': 0.1,
            'feature_unit': 'm'
        }

        super().__init__(**kwargs)


class NCAARink(HockeyRink):
    """A regulation NCAA ice hockey rink.

    Please see the HockeyRink class definition for full details.
    """

    def __init__(self, **kwargs):
        kwargs['corner_radius'] = 20.0

        super().__init__(**kwargs)


class NHLRink(HockeyRink):
    """A regulation NHL ice hockey rink.

    Please see the HockeyRink class definition for full details.
    """

    def __init__(self, **kwargs):
        kwargs['goalkeepers_restricted_area'] = {'visible': True}

        super().__init__(**kwargs)


class NWHLRink(HockeyRink):
    """A regulation NWHL ice hockey rink.

    Please see the HockeyRink class definition for full details.
    """

    def __init__(self, **kwargs):
        kwargs['goalkeepers_restricted_area'] = {'visible': True}

        super().__init__(**kwargs)
