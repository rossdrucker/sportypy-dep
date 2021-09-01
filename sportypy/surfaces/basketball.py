"""Extension of the BaseSurfacePlot class to create a basketball court.

This is a second-level child class of the BaseSurface class, and as such will
have access to its attributes and methods. The default court will be that of
the NBA, and main leagues will have their own subclass, but a user can manually
specify their own court parameters to create a totally-customized court. The
court's features are parameterized by the basic dimensions of the court, which
comprise the attributes of the class.

@author: Ross Drucker
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy.features.basketball_features as basketball
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class BasketballCourt(BaseSurfacePlot):
    """A generic basketball court subclass of BaseSurfacePlot.

    This allows for the creation of the basketball court in a way that is
    entirely parameterized by the court's baseline characteristics. The default
    will be the dimensions of an NBA court. See the class definition for full
    details.

    Attributes
    ----------
    rotation : float (default: 0.0)
            The angle (in degrees) through which to rotate the final plot

    x_trans : float (default: 0.0)
        The amount that the x coordinates are to be shifted. By convention,
        the +x axis extends from the center of the basketball court towards the
        right-hand goal when viewing the court in "TV View" (e.g. the court is
        longer than it is tall)

    y_trans : float (default: 0.0)
        The amount that the y coordinates are to be shifted. By convention,
        the +y axis extends from the center of the basketball court towards the
        top of the court when viewing the court in "TV View" (e.g. the court is
        longer than it is tall)

    court_length : float (default: 94.0; 94')
        The length of the court in the x direction when viewing the court in
        "TV View" (e.g. the court is longer than it is tall)

    court_width : float (default: 50.0; 50')
        The width of the court in the y direction when viewing the court in
        "TV View" (e.g. the court is longer than it is tall)

    court_units : str (default: 'ft')
        The units with which the court is to be drawn

    line_thickness : float (default: 2.0 / 12; 2")
        The thickness of the lines on the court

    basket_to_baseline_dist : float (default: 5.0 + (3.0 / 12.0); 5'3")
        The distance from the interior edge of the baseline to the center of
        the basket ring

    ring_center_to_backboard : float (default: 15.0 / 12.0; 15")
        The distance from the center of the basket ring to the face of the
        backboard

    backboard_face_size : float (default: 72.0 / 12.0; 72")
        The length of the backboard in the y direction when viewing the court
        in "TV View" (e.g. the court is longer than it is tall). This should
        be the full face size, not the half

    baseline_apron_extension_length : float (default: 8.0, 8')
        How far the court apron should extend beyond the baseline

    sideline_apron_extension_width : float (default: 5.0; 5')
        How far the court apron should extend beyond the sideline

    center_circle_radius : float (default: 6.0; 6')
        The outer radius of the center circle

    sideline_to_corner_three_point_dist : float (default: 3.0; 3')
        The distance between the sideline and the corner piece of the
        three-point line

    three_point_arc_distance : float (default: 23.0 + (9.0 / 12.0); 23'9")
        The radial distance from the center of the basket ring to the arc of
        the three-point line

    free_throw_dist : float (default: 15.0; 15')
        The distance from the edge of the free-throw line nearest center court
        to the front face of the backboard

    free_throw_lane_width : float (default: 16.0; 16')
        The width of the free-throw lane when viewing the court in "TV View"
        (e.g. the court is longer than it is tall)

    free_throw_circle_radius : float (default: 6.0; 6')
        The outer radius of the free-throw circle

    free_throw_circle_extended_arc : float (default: 0.0)
        In some leagues, the free-throw circle extends beyond the free-throw
        line. This is the arc length that it should extend in those leagues
        (e.g. in the NBA, this is 12.29", or 12.29 / 12.0)

    free_throw_dash_arc_length : float (default: 15.5 / 12.0; 15.5")
        The arc length of a dash of the free-throw circle. This is not required
        in all leagues

    n_free_throw_circle_dashes : float (default: 0.0)
        The number of dashes along the dashed portion of the free-throw circle
        (where applicable)

    restricted_arc_outer_radius : float (default: 4.0 + (2.0 / 12.0); 4'2")
        The outer radius of the restricted area

    backboard_thickness : float (default: 4.0 / 12.0; 4")
        The thickness by which to represent the backboard. In length/width
        terms when viewing in "TV View" (e.g. the court is longer than it is
        tall), this is considered the backboard's length, although that is not
        typically how this measurement is referred to

    basket_ring_radius : float (default: 9.0; 9")
        The radius of the basket ring

    ring_extension_width : float (default: 7.0 / 12.0; 7")
        The length of the extension between the backboard and edge of the
        basket ring nearest the backboard

    coaches_box_length : float (default: 28.0; 28')
        The length of the coaches box, when measured from the interior edge of
        the baseline to the edge of the coaches box nearest the baseline
    """

    def __init__(self, rotation = 0.0, x_trans = 0.0, y_trans = 0.0,
                 court_length = 94.0, court_width = 50.0, court_units = 'ft',
                 line_thickness = (2.0 / 12.0),
                 basket_to_baseline_dist = 5.0 + (3.0 / 12.0),
                 ring_center_to_backboard = (15.0 / 12.0),
                 backboard_face_size = (72.0 / 12.0),
                 baseline_apron_extension_length = 8.0,
                 sideline_apron_extension_width = 5.0,
                 center_circle_radius = 6.0,
                 sideline_to_corner_three_point_dist = 3.0,
                 three_point_arc_distance = 23.0 + (9.0 / 12.0),
                 free_throw_dist = 15.0,
                 free_throw_lane_width = 16.0,
                 free_throw_circle_radius = 6.0,
                 free_throw_circle_extended_arc = 0.0,
                 free_throw_dash_arc_length = 15.5 / 12.0,
                 n_free_throw_circle_dashes = 0.0,
                 restricted_arc_outer_radius = 4.0 + (2.0 / 12.0),
                 backboard_thickness = (4.0 / 12.0),
                 basket_ring_radius = (9.0 / 12.0),
                 ring_extension_width = (7.0 / 12.0),
                 coaches_box_x = 28.0,
                 coaches_box_width = 3.0,
                 substitution_area_length = 8.0 + (2.0 / 12.0),
                 center_circle_outline = {}, center_circle_fill = {},
                 division_line = {}, end_line = {}, side_line = {}, apron = {},
                 three_point_line = {}, two_point_range = {}, coaches_box = {},
                 substitution_area = {}, free_throw_lane_boundary = {},
                 free_throw_circle_outline = {}, paint = {},
                 restricted_arc = {}, colors_dict = {}, backboard = {},
                 basket_ring = {}, net = {}, **added_features):
        # Set the rotation of the plot to be the supplied rotation
        # value
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the court's necessary shifts. This will overwrite the
        # default values of x_trans and y_trans inherited from the
        # BaseSurfacePlot (which is in turn inherited from BaseSurface)
        self.x_trans = x_trans
        self.y_trans = y_trans

        # Set the full-sized dimensions of the court along with its
        # units of measure
        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness

        # Set the half-dimensions of the court, as these are often more useful
        # than the full-sized dimensions
        self.half_court_length = self.court_length / 2.0
        self.half_court_width = self.court_width / 2.0

        # Set the position of the center of the baskets
        self.basket_center_x = self.half_court_length - basket_to_baseline_dist
        self.basket_center_y = 0.0

        # Set the position of the backboards
        self.backboard_face_x = self.basket_center_x + ring_center_to_backboard
        self.backboard_face_size = backboard_face_size

        ##############################################################
        # Set the properties that are needed for particular features #
        ##############################################################
        # Court apron
        self.baseline_apron_extension_length = baseline_apron_extension_length
        self.sideline_apron_extension_width = sideline_apron_extension_width

        # Center circle
        self.center_circle_radius = center_circle_radius

        # Three-point range
        corner_three_dist = sideline_to_corner_three_point_dist
        three_point_half_width = self.half_court_width - corner_three_dist
        self.three_point_arc_width = 2.0 * three_point_half_width
        self.three_point_arc_distance = three_point_arc_distance

        # Free-throw lane
        self.free_throw_lane_length = self.half_court_length -\
            self.backboard_face_x + free_throw_dist
        self.free_throw_lane_width = free_throw_lane_width

        # Free-throw circle
        self.free_throw_circle_radius = free_throw_circle_radius
        self.n_free_throw_circle_dashes = n_free_throw_circle_dashes
        self.free_throw_dash_arc_length = free_throw_dash_arc_length

        # Restricted arc
        self.restricted_arc_radius = restricted_arc_outer_radius

        # Backboard
        self.backboard_width = backboard_face_size
        self.backboard_thickness = backboard_thickness

        # Basket ring
        self.basket_ring_radius = basket_ring_radius

        # Coaches Box
        self.coaches_box_x = coaches_box_x
        self.coaches_box_width = coaches_box_width

        # Substitution Area
        self.substitution_area_length = substitution_area_length

        # Create a container for the relevant features of a basketball court
        self._features = []

        # Initialize the x and y limits for the plot to be None. These
        # will get set when calling the draw() method below
        self._feature_xlim = None
        self._feature_ylim = None

        # Initialize the standard colors of the court
        standard_colors = {
            'court_background': '#d2ab6f',
            'offensive_halfcourt': '#d2ab6f',
            'defensive_halfcourt': '#d2ab6f',
            'center_circle_outline': '#000000',
            'center_circle_fill': '#d2ab6f',
            'division_line': '#000000',
            'end_line': '#000000',
            'side_line': '#000000',
            'coaches_box': '#000000',
            'substitution_area': '#000000',
            'court_apron': '#d2ab6f',
            'three_point_line': '#000000',
            'two_point_range': '#d2ab6f',
            'free_throw_lane_boundary': '#000000',
            'free_throw_circle_outline': '#000000',
            'paint': '#d2ab6f',
            'restricted_arc': '#000000',
            'backboard': '#000000',
            'basket_ring': '#000000',
            'net': '#ffffff'
        }

        # Combine the colors with a passed colors dictionary
        if not colors_dict:
            colors_dict = {}

        # Create the final color set for the features
        self.feature_colors = {**standard_colors, **colors_dict}

        # Initialize the constraint of the court to be inside of the playing
        # lines
        court_constraint = {
            'class': basketball.CourtConstraint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': 0.0,
            'visible': False
        }
        self._initialize_feature(court_constraint)
        self._surface_constraint = self._features.pop(-1)

        # Initialize the offensive half of the court
        offensive_halfcourt_params = {
            'class': basketball.HalfCourt,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'court_side': 'offense',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['offensive_halfcourt'],
            'edgecolor': self.feature_colors['offensive_halfcourt'],
            'zorder': 0
        }
        self._initialize_feature(offensive_halfcourt_params)

        defensive_halfcourt_params = {
            'class': basketball.HalfCourt,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'court_side': 'defense',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['defensive_halfcourt'],
            'edgecolor': self.feature_colors['defensive_halfcourt'],
            'zorder': 0
        }
        self._initialize_feature(defensive_halfcourt_params)

        # Initialize the center circle's outline
        center_circle_outline_params = {
            'class': basketball.CenterCircleOutline,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': self.center_circle_radius,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['center_circle_outline'],
            'edgecolor': self.feature_colors['center_circle_outline'],
            'zorder': 10
        }
        center_circle_outline_params = {
            **center_circle_outline_params,
            **center_circle_outline
        }
        self._initialize_feature(center_circle_outline_params)

        # Initialize the center circle's fill
        center_circle_fill_params = {
            'class': basketball.CenterCircleFill,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': self.center_circle_radius,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['center_circle_fill'],
            'edgecolor': self.feature_colors['center_circle_fill'],
            'zorder': 10
        }
        center_circle_fill_params = {
            **center_circle_fill_params,
            **center_circle_fill
        }
        self._initialize_feature(center_circle_fill_params)

        # Initialize the time line
        division_line_params = {
            'class': basketball.DivisionLine,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['division_line'],
            'edgecolor': self.feature_colors['division_line'],
            'zorder': 15
        }
        division_line_params = {**division_line_params, **division_line}
        self._initialize_feature(division_line_params)

        # Initialize the end line
        end_line_params = {
            'class': basketball.EndLine,
            'x_anchor': self.half_court_length,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['end_line'],
            'edgecolor': self.feature_colors['end_line'],
            'zorder': 15
        }
        end_line_params = {**end_line_params, **end_line}
        self._initialize_feature(end_line_params)

        # Initialize the side line
        side_line_params = {
            'class': basketball.SideLine,
            'x_anchor': 0.0,
            'y_anchor': self.court_width / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': True,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['side_line'],
            'edgecolor': self.feature_colors['side_line'],
            'zorder': 15
        }
        side_line_params = {**side_line_params, **side_line}
        self._initialize_feature(side_line_params)

        # Initialize the coaches box lines
        coaches_box_params = {
            'class': basketball.CoachesBox,
            'x_anchor': self.half_court_length - self.coaches_box_x -
            self.line_thickness,
            'y_anchor': self.half_court_width,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': self.coaches_box_width,
            'extension_direction': 'inward',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['coaches_box'],
            'edgecolor': self.feature_colors['coaches_box'],
            'zorder': 16
        }
        coaches_box_params = {**coaches_box_params, **coaches_box}
        self._initialize_feature(coaches_box_params)

        # Initialize the coaches box lines
        substitution_area_params = {
            'class': basketball.SubstitutionArea,
            'x_anchor': self.substitution_area_length / 2.0,
            'y_anchor': self.half_court_width + self.line_thickness,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['substitution_area'],
            'edgecolor': self.feature_colors['substitution_area'],
            'zorder': 16
        }
        substitution_area_params = {
            **substitution_area_params,
            **substitution_area
        }
        self._initialize_feature(substitution_area_params)

        # Initialize the court apron
        apron_params = {
            'class': basketball.CourtApron,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_thickness': self.baseline_apron_extension_length,
            'facecolor': self.feature_colors['court_apron'],
            'edgecolor': self.feature_colors['court_apron'],
            'zorder': 10
        }
        apron_params = {**apron_params, **apron}
        self._initialize_feature(apron_params)

        # Initialize the three-point line
        three_point_line_params = {
            'class': basketball.ThreePointLine,
            'x_anchor': -self.half_court_length,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': self.three_point_arc_width,
            'basket_to_baseline_dist': basket_to_baseline_dist,
            'feature_radius': self.three_point_arc_distance,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['three_point_line'],
            'edgecolor': self.feature_colors['three_point_line'],
            'zorder': 10
        }
        three_point_line_params = {
            **three_point_line_params,
            **three_point_line
        }
        self._initialize_feature(three_point_line_params)

        # Initialize the two-point range
        two_point_range_params = {
            'class': basketball.TwoPointRange,
            'x_anchor': -self.half_court_length,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': self.three_point_arc_width,
            'basket_to_baseline_dist': basket_to_baseline_dist,
            'feature_radius': self.three_point_arc_distance,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['two_point_range'],
            'edgecolor': self.feature_colors['two_point_range'],
            'zorder': 5
        }
        two_point_range_params = {
            **two_point_range_params,
            **two_point_range
        }
        self._initialize_feature(two_point_range_params)

        # Initialize the free-throw lane boundaries
        free_throw_lane_boundary_params = {
            'class': basketball.FreeThrowLaneBoundary,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.free_throw_lane_length,
            'lane_width': self.free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['free_throw_lane_boundary'],
            'edgecolor': self.feature_colors['free_throw_lane_boundary'],
            'zorder': 10
        }
        free_throw_lane_boundary_params = {
            **free_throw_lane_boundary_params,
            **free_throw_lane_boundary
        }
        self._initialize_feature(free_throw_lane_boundary_params)

        # Initialize the free-throw circle's outline
        free_throw_circle_outline_params = {
            'class': basketball.FreeThrowCircleOutline,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'arc_length_behind_ft_line': free_throw_circle_extended_arc,
            'free_throw_lane_length': self.free_throw_lane_length,
            'feature_radius': self.free_throw_circle_radius,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['free_throw_circle_outline'],
            'edgecolor': self.feature_colors['free_throw_circle_outline'],
            'zorder': 15
        }
        free_throw_circle_outline_params = {
            **free_throw_circle_outline_params,
            **free_throw_circle_outline
        }
        self._initialize_feature(free_throw_circle_outline_params)

        # Initialize the free-throw circle's dashed component (when necessary)
        if self.n_free_throw_circle_dashes > 0:
            # Compute the angle through which each dash will be traced
            free_throw_circle_s = self.free_throw_dash_arc_length
            free_throw_circle_r = self.free_throw_circle_radius
            theta_dashes = (free_throw_circle_s / free_throw_circle_r) / np.pi

            # Get the starting angle for the first dash. This will be updated
            # by the below loop
            start_s = free_throw_circle_extended_arc
            start_angle = 0.5 - ((start_s / free_throw_circle_r) / np.pi)

            start_angle -= theta_dashes

            # Create the dashes
            for dash in range(0, int(self.n_free_throw_circle_dashes)):
                free_throw_circle_dash_params = {
                    'class': basketball.FreeThrowCircleOutlineDash,
                    'x_anchor': 0.0,
                    'y_anchor': 0.0,
                    'x_justify': 'center',
                    'y_justify': 'center',
                    'reflect_x': True,
                    'reflect_y': False,
                    'visible': True,
                    'court_length': self.court_length,
                    'court_width': self.court_width,
                    'free_throw_lane_length': self.free_throw_lane_length,
                    'start_angle': start_angle,
                    'end_angle': start_angle - theta_dashes,
                    'feature_radius': self.free_throw_circle_radius,
                    'feature_thickness': self.line_thickness,
                    'facecolor': self.feature_colors['free_throw_circle_dash'],
                    'edgecolor': self.feature_colors['free_throw_circle_dash'],
                    'zorder': 15
                }
                self._initialize_feature(free_throw_circle_dash_params)

                start_angle -= (2.0 * theta_dashes)

        # Initialize the painted area
        paint_params = {
            'class': basketball.Paint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.free_throw_lane_length,
            'lane_width': self.free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['paint'],
            'edgecolor': self.feature_colors['paint'],
            'zorder': 10
        }
        paint_params = {**paint_params, **paint}
        self._initialize_feature(paint_params)

        # Initialize the restricted area arc
        restricted_arc_params = {
            'class': basketball.RestrictedArc,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'basket_center_x': self.basket_center_x,
            'backboard_face_x': self.backboard_face_x,
            'feature_radius': self.restricted_arc_radius,
            'feature_thickness': self.line_thickness,
            'facecolor': self.feature_colors['restricted_arc'],
            'edgecolor': self.feature_colors['restricted_arc'],
            'zorder': 10
        }
        restricted_arc_params = {**restricted_arc_params, **restricted_arc}
        self._initialize_feature(restricted_arc_params)

        # Initialize the backboard
        backboard_params = {
            'class': basketball.Backboard,
            'x_anchor': self.backboard_face_x,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 0.0,
            'feature_width': self.backboard_width,
            'feature_thickness': self.backboard_thickness,
            'facecolor': self.feature_colors['backboard'],
            'edgecolor': self.feature_colors['backboard'],
            'zorder': 15
        }
        backboard_params = {**backboard_params, **backboard}
        self._initialize_feature(backboard_params)

        # Initialize the basket ring
        basket_ring_params = {
            'class': basketball.BasketRing,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': self.basket_ring_radius,
            'feature_thickness': self.line_thickness,
            'basket_center_x': self.basket_center_x,
            'backboard_face_x': self.backboard_face_x,
            'ring_extension_width': ring_extension_width,
            'facecolor': self.feature_colors['basket_ring'],
            'edgecolor': self.feature_colors['basket_ring'],
            'zorder': 15
        }
        basket_ring_params = {**basket_ring_params, **basket_ring}
        self._initialize_feature(basket_ring_params)

        # Initialize the basket ring
        net_params = {
            'class': basketball.Net,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': self.basket_ring_radius,
            'basket_center_x': self.basket_center_x,
            'facecolor': self.feature_colors['net'],
            'edgecolor': self.feature_colors['net'],
            'zorder': 16
        }
        net_params = {**net_params, **net}
        self._initialize_feature(net_params)

        for added_feature in added_features.values():
            self._initialize_feature(added_feature)

    def draw(self, ax = None, display_range = 'full', xlim = None, ylim = None,
             rotation = None):
        """Draw the court.

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



        xlim : float, tuple (float, float), or None (default: None)
            The display range in the x direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the x coordinates to display and the upper bound will be the
            +x end of the court. If a tuple, the two values will be
            used to determine the bounds. If None, then the
            display_range will be used instead to set the bounds

        ylim : float, tuple (float, float), or None (default: None)
            The display range in the y direction to be used. If a single
            float is provided, this will be used as the lower bound of
            the y coordinates to display and the upper bound will be the
            +y side of the court. If a tuple, the two values will be used
            to determine the bounds. If None, then the display_range
            will be used instead to set the bounds

        rotation : float or None (default: None)
            Angle (in degrees) through which to rotate the court when
            drawing. If used, this will set the class attribute of
            self._rotation. A value of 0.0 will correspond to a TV View
            of the court, where +x is to the right and +y is on top. The
            rotation occurs counter clockwise
        """
        # If there is a rotation to be applied, apply it first and set it as
        # the class attribute self._rotation
        if rotation:
            self._rotation = Affine2D().rotate_deg(rotation)

        # If an Axes object is not provided, create one to use for plotting
        if ax is None:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor(self.feature_colors['court_background'])
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

            # Assuming the feature is visible (and is not the sideline or
            # endline), get the feature's x and y limits to ensure it lies
            # within the bounds of the court
            if visible and not isinstance(feature, basketball.CourtConstraint):
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

        # Determine the length of half of the court (including the thickness of
        # the court boundary)
        half_court_length = self.half_court_length +\
            self.baseline_apron_extension_length + 1.0
        half_court_width = self.half_court_width +\
            self.sideline_apron_extension_width + 1.0

        # Set the x limits of the plot if they are not provided
        if not xlim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            xlims = {
                # Full surface (default)
                'full': (-half_court_length, half_court_length),

                # Half-court plots
                'offense': (0.0, half_court_length),
                'offence': (0.0, half_court_length),
                'defense': (-half_court_length, 0.0),
                'defence': (-half_court_length, 0.0)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # court
            xlim = xlims.get(
                display_range,
                (-half_court_length, half_court_length)
            )

        # If an x limit is provided, try to use it
        else:
            try:
                xlim = (xlim[0] - self.x_trans, xlim[1] - self.x_trans)

            # If the limit provided is not a tuple, use the provided value as
            # best as possible. This will set the provided value as the lower
            # limit of x, and display any x values greater than it
            except TypeError:
                # Apply the necessary shift to align the plot limit with the
                # data
                xlim = xlim - self.x_trans

                # If the provided value for the x limit is beyond the end of
                # the court boundaries, display the entire court
                if xlim >= half_court_length:
                    xlim = -half_court_length

                # Set the x limit to be a tuple as described above
                xlim = (xlim, half_court_length)

        # Set the y limits of the plot if they are not provided. The default
        # will be the entire width of the court. Additional view regions may be
        # added here
        if not ylim:
            # Convert the search key to lower case
            display_range = display_range.lower().replace(' ', '')

            # Get the limits from the viable display ranges
            ylims = {
                # Full surface (default)
                'full': (-half_court_width, half_court_width),

                # Half-court plots
                'offense': (-half_court_width, half_court_width),
                'offence': (-half_court_width, half_court_width),
                'defense': (-half_court_width, half_court_width),
                'defence': (-half_court_width, half_court_width),

                # Offensive zone
                'ozone': (-half_court_width, half_court_width),
                'offensive_zone': (-half_court_width, half_court_width),
                'offensive zone': (-half_court_width, half_court_width),
                'attacking_zone': (-half_court_width, half_court_width),
                'attacking zone': (-half_court_width, half_court_width),

                # Defensive zone
                'dzone': (-half_court_width, half_court_width),
                'defensive_zone': (-half_court_width, half_court_width),
                'defensive zone': (-half_court_width, half_court_width),
                'defending_zone': (-half_court_width, half_court_width),
                'defending zone': (-half_court_width, half_court_width)
            }

            # Extract the x limit from the dictionary, defaulting to the full
            # court
            ylim = ylims.get(
                display_range,
                (-half_court_length, half_court_length)
            )

        # Otherwise, repeat the process above but for y
        else:
            try:
                ylim = (ylim[0] - self.y_trans, ylim[1] - self.y_trans)

            except TypeError:
                ylim = ylim - self.y_trans

                if ylim >= half_court_width:
                    ylim = -half_court_width

                ylim = (ylim, half_court_width)

        # Smaller coordinate should always go first
        if xlim[0] > xlim[1]:
            xlim = (xlim[1], xlim[0])
        if ylim[0] > ylim[1]:
            ylim = (ylim[1], ylim[0])

        # Constrain the limits from going beyond the end of the court (plus one
        # additional unit of buffer)
        xlim = (
            max(xlim[0], -half_court_length),
            min(xlim[1], half_court_length)
        )

        ylim = (
            max(ylim[0], -half_court_width),
            min(ylim[1], half_court_width)
        )

        return xlim, ylim


class NBACourt(BasketballCourt):
    """A regulation NBA basketball court.

    Please see the BasketballCourt documentation for full details.
    """

    def __init__(self, court_length = 94.0, court_width = 50.0,
                 court_units = 'ft', line_thickness = (2.0 / 12.0),
                 include_amateur_lane = False,
                 include_amateur_paint = False,
                 amateur_free_throw_lane_length = 19.0,
                 amateur_free_throw_lane_width = 12.0,
                 include_amateur_blocks = False, colors_dict = {}, **kwargs):

        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness
        self.amateur_free_throw_lane_length = amateur_free_throw_lane_length
        self.amateur_free_throw_lane_width = amateur_free_throw_lane_width

        nba_colors = {
            'inner_center_circle_outline': '#000000',
            'inner_center_circle_fill': '#d2ab6f',
            'pro_blocks': '#000000',
            'amateur_free_throw_lane_boundary': '#000000',
            'amateur_blocks': '#000000',
            'amateur_paint': '#1d428a',
            'free_throw_circle_dash': '#000000',
            'defensive_box': '#000000'
        }

        self.nba_colors = {**nba_colors, **colors_dict}

        # The inner center circle that appears on a (W)NBA basketball court
        kwargs['center_circle_outline_params'] = {
            'class': basketball.CenterCircleOutline,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 2.0 - (2.0 / 12.0),
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['inner_center_circle_outline'],
            'edgecolor': self.nba_colors['inner_center_circle_outline'],
            'zorder': 10
        }

        kwargs['center_circle_fill_params'] = {
            'class': basketball.CenterCircleFill,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 2.0 - (2.0 / 12.0),
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['inner_center_circle_fill'],
            'edgecolor': self.nba_colors['inner_center_circle_fill'],
            'zorder': 10
        }

        kwargs['amateur_free_throw_lane_boundary_params'] = {
            'class': basketball.FreeThrowLaneBoundary,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_amateur_lane,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.amateur_free_throw_lane_length,
            'lane_width': self.amateur_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_free_throw_lane_boundary'],
            'edgecolor': self.nba_colors['amateur_free_throw_lane_boundary'],
            'zorder': 10
        }

        # Initialize the blocks
        kwargs['pro_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['pro_blocks'],
            'edgecolor': self.nba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 8.0 - (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['pro_blocks'],
            'edgecolor': self.nba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['pro_blocks'],
            'edgecolor': self.nba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 + (3.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['pro_blocks'],
            'edgecolor': self.nba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.5,
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 1.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_blocks'],
            'edgecolor': self.nba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 - (1.0 / 12.9),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_blocks'],
            'edgecolor': self.nba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 - (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_blocks'],
            'edgecolor': self.nba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 17.0 + (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_blocks'],
            'edgecolor': self.nba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_paint_params'] = {
            'class': basketball.Paint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_amateur_paint,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.amateur_free_throw_lane_length,
            'lane_width': self.amateur_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['amateur_paint'],
            'edgecolor': self.nba_colors['amateur_paint'],
            'zorder': 10
        }

        kwargs['defensive_box_endline_mark_baseline'] = {
            'class': basketball.DefensiveBoxMark,
            'x_anchor': self.court_length / 2.0,
            'y_anchor': 11.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'mark_length': 0.5,
            'mark_width': self.line_thickness,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['defensive_box'],
            'edgecolor': self.nba_colors['defensive_box'],
            'zorder': 10
        }

        kwargs['defensive_box_endline_mark_painted_area'] = {
            'class': basketball.DefensiveBoxMark,
            'x_anchor': (self.court_length / 2.0) - 13.0,
            'y_anchor': 4.5,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'mark_length': self.line_thickness,
            'mark_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nba_colors['defensive_box'],
            'edgecolor': self.nba_colors['defensive_box'],
            'zorder': 10
        }

        super().__init__(free_throw_circle_extended_arc = 12.29 / 12.0,
                         n_free_throw_circle_dashes = 6.0,
                         colors_dict = self.nba_colors, **kwargs)


class WNBACourt(BasketballCourt):
    """A regulation WNBA basketball court.

    Please see the BasketballCourt documentation for full details.
    """

    def __init__(self, court_length = 94.0, court_width = 50.0,
                 court_units = 'ft', line_thickness = (2.0 / 12.0),
                 include_amateur_lane = False,
                 include_amateur_paint = False,
                 amateur_free_throw_lane_length = 19.0,
                 amateur_free_throw_lane_width = 12.0,
                 include_amateur_blocks = False, colors_dict = {}, **kwargs):

        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness
        self.amateur_free_throw_lane_length = amateur_free_throw_lane_length
        self.amateur_free_throw_lane_width = amateur_free_throw_lane_width

        wnba_colors = {
            'inner_center_circle_outline': '#000000',
            'inner_center_circle_fill': '#d2ab6f',
            'pro_blocks': '#000000',
            'amateur_free_throw_lane_boundary': '#000000',
            'amateur_blocks': '#000000',
            'amateur_paint': '#1d428a',
            'free_throw_circle_dash': '#000000',
            'defensive_box': '#000000'
        }

        self.wnba_colors = {**wnba_colors, **colors_dict}

        # The inner center circle that appears on a (W)NBA basketball court
        kwargs['center_circle_outline_params'] = {
            'class': basketball.CenterCircleOutline,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 2.0 - (2.0 / 12.0),
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['inner_center_circle_outline'],
            'edgecolor': self.wnba_colors['inner_center_circle_outline'],
            'zorder': 10
        }

        kwargs['center_circle_fill_params'] = {
            'class': basketball.CenterCircleFill,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_radius': 2.0 - (2.0 / 12.0),
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['inner_center_circle_fill'],
            'edgecolor': self.wnba_colors['inner_center_circle_fill'],
            'zorder': 10
        }

        kwargs['amateur_free_throw_lane_boundary_params'] = {
            'class': basketball.FreeThrowLaneBoundary,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_amateur_lane,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.amateur_free_throw_lane_length,
            'lane_width': self.amateur_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_free_throw_lane_boundary'],
            'edgecolor': self.wnba_colors['amateur_free_throw_lane_boundary'],
            'zorder': 10
        }

        # Initialize the blocks
        kwargs['pro_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['pro_blocks'],
            'edgecolor': self.wnba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 8.0 - (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['pro_blocks'],
            'edgecolor': self.wnba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['pro_blocks'],
            'edgecolor': self.wnba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 + (3.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['pro_blocks'],
            'edgecolor': self.wnba_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.5,
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 1.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_blocks'],
            'edgecolor': self.wnba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 - (1.0 / 12.9),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_blocks'],
            'edgecolor': self.wnba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 - (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_blocks'],
            'edgecolor': self.wnba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 17.0 + (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_amateur_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_blocks'],
            'edgecolor': self.wnba_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_paint_params'] = {
            'class': basketball.Paint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_amateur_paint,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.amateur_free_throw_lane_length,
            'lane_width': self.amateur_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['amateur_paint'],
            'edgecolor': self.wnba_colors['amateur_paint'],
            'zorder': 10
        }

        kwargs['defensive_box_endline_mark_baseline'] = {
            'class': basketball.DefensiveBoxMark,
            'x_anchor': self.court_length / 2.0,
            'y_anchor': 11.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'mark_length': 0.5,
            'mark_width': self.line_thickness,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['defensive_box'],
            'edgecolor': self.wnba_colors['defensive_box'],
            'zorder': 10
        }

        kwargs['defensive_box_endline_mark_painted_area'] = {
            'class': basketball.DefensiveBoxMark,
            'x_anchor': (self.court_length / 2.0) - 13.0,
            'y_anchor': 4.5,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'mark_length': self.line_thickness,
            'mark_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.wnba_colors['defensive_box'],
            'edgecolor': self.wnba_colors['defensive_box'],
            'zorder': 10
        }

        super().__init__(three_point_arc_distance = 22.0 + (1.75 / 12.0),
                         free_throw_circle_extended_arc = 12.29 / 12.0,
                         n_free_throw_circle_dashes = 6.0,
                         colors_dict = self.wnba_colors, **kwargs)


class NCAACourt(BasketballCourt):
    """A regulation NCAA basketball court.

    Please see the BasketballCourt documentation for full details.
    """

    def __init__(self, court_length = 94.0, court_width = 50.0,
                 court_units = 'ft', line_thickness = (2.0 / 12.0),
                 team_bench_area_x = 28.0,
                 team_bench_area_width = 6.0 + (2.0 / 12.0),
                 include_pro_lane = False,
                 include_pro_paint = False,
                 pro_free_throw_lane_length = 19.0,
                 pro_free_throw_lane_width = 16.0,
                 include_pro_blocks = False, colors_dict = {}, **kwargs):

        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness
        self.pro_free_throw_lane_length = pro_free_throw_lane_length
        self.pro_free_throw_lane_width = pro_free_throw_lane_width
        self.team_bench_area_x = team_bench_area_x
        self.team_bench_area_width = team_bench_area_width

        ncaa_colors = {
            'amateur_blocks': '#000000',
            'pro_free_throw_lane_boundary': '#000000',
            'pro_blocks': '#000000',
            'pro_paint': '#1d428a',
            'free_throw_circle_dash': '#000000',
            'defensive_box': '#000000',
            'team_bench_area': '#000000',
            'throw_in_line': '#000000'
        }

        self.ncaa_colors = {**ncaa_colors, **colors_dict}

        kwargs['amateur_free_throw_lane_boundary_params'] = {
            'class': basketball.FreeThrowLaneBoundary,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_pro_lane,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.pro_free_throw_lane_length,
            'lane_width': self.pro_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_free_throw_lane_boundary'],
            'edgecolor': self.ncaa_colors['pro_free_throw_lane_boundary'],
            'zorder': 10
        }

        # Initialize the blocks
        kwargs['pro_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_pro_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_blocks'],
            'edgecolor': self.ncaa_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 8.0 - (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_pro_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_blocks'],
            'edgecolor': self.ncaa_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 + (1.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_pro_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_blocks'],
            'edgecolor': self.ncaa_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['pro_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 + (3.0 / 12.0),
            'y_anchor': 8.0 + (3.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': include_pro_blocks,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 0.5,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_blocks'],
            'edgecolor': self.ncaa_colors['pro_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.5,
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 1.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['amateur_blocks'],
            'edgecolor': self.ncaa_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 - (1.0 / 12.9),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['amateur_blocks'],
            'edgecolor': self.ncaa_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.0 - (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['amateur_blocks'],
            'edgecolor': self.ncaa_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['amateur_block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 17.0 + (3.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['amateur_blocks'],
            'edgecolor': self.ncaa_colors['amateur_blocks'],
            'zorder': 10
        }

        kwargs['pro_paint_params'] = {
            'class': basketball.Paint,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': True,
            'visible': include_pro_paint,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'lane_length': self.pro_free_throw_lane_length,
            'lane_width': self.pro_free_throw_lane_width,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['pro_paint'],
            'edgecolor': self.ncaa_colors['pro_paint'],
            'zorder': 10
        }

        kwargs['defensive_box_endline_mark_baseline'] = {
            'class': basketball.DefensiveBoxMark,
            'x_anchor': self.court_length / 2.0,
            'y_anchor': 9.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'mark_length': 0.5,
            'mark_width': self.line_thickness,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['defensive_box'],
            'edgecolor': self.ncaa_colors['defensive_box'],
            'zorder': 10
        }

        kwargs['team_bench_area'] = {
            'class': basketball.TeamBenchArea,
            'x_anchor': (self.court_length / 2.0) - self.team_bench_area_x -
            self.line_thickness,
            'y_anchor': self.court_width / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': self.team_bench_area_width,
            'extension_direction': 'both',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['team_bench_area'],
            'edgecolor': self.ncaa_colors['team_bench_area'],
            'zorder': 16
        }

        kwargs['throw_in_line'] = {
            'class': basketball.ThrowInLine,
            'x_anchor': (self.court_length / 2.0) - 28.0 - self.line_thickness,
            'y_anchor': -(self.court_width / 2.0) - self.line_thickness,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': 2.0 / 12.0,
            'extension_direction': 'outward',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.ncaa_colors['throw_in_line'],
            'edgecolor': self.ncaa_colors['throw_in_line'],
            'zorder': 16
        }

        super().__init__(free_throw_lane_width = 12.0,
                         three_point_arc_distance = 22.0 + (1.75 / 12.0),
                         coaches_box_x = 38.0,
                         coaches_box = {
                             'feature_width': 2.0,
                             'reflect_y': False,
                             'extension_direction': 'outward'
                         },
                         substitution_area = {'visible': False},
                         colors_dict = self.ncaa_colors, **kwargs)


class FIBACourt(BasketballCourt):
    """A regulation FIBA basketball court.

    Please see the BasketballCourt documentation for full details.
    """

    def __init__(self, court_length = 28.0, court_width = 15.0,
                 court_units = 'm', line_thickness = 0.05,
                 team_bench_area_x = 9.0, team_bench_area_width = 2.0,
                 colors_dict = {}, **kwargs):

        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness
        self.team_bench_area_x = team_bench_area_x
        self.team_bench_area_width = team_bench_area_width

        fiba_colors = {
            'inner_center_circle_outline': '#000000',
            'inner_center_circle_fill': '#d2ab6f',
            'amateur_blocks': '#000000',
            'pro_free_throw_lane_boundary': '#000000',
            'blocks': '#000000',
            'pro_paint': '#1d428a',
            'free_throw_circle_dash': '#000000',
            'defensive_box': '#000000',
            'team_bench_area': '#000000',
            'throw_in_line': '#000000'
        }

        self.fiba_colors = {**fiba_colors, **colors_dict}

        # Initialize the blocks
        kwargs['block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 1.775,
            'y_anchor': 2.45 + .05,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 0.05,
            'block_width': 0.1,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['blocks'],
            'edgecolor': self.fiba_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 2.85,
            'y_anchor': 2.45 + .05,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 0.4,
            'block_width': 0.1,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['blocks'],
            'edgecolor': self.fiba_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 3.925,
            'y_anchor': 2.45 + .05,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 0.05,
            'block_width': 0.1,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['blocks'],
            'edgecolor': self.fiba_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 4.825,
            'y_anchor': 2.45 + .05,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 0.05,
            'block_width': 0.1,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['blocks'],
            'edgecolor': self.fiba_colors['blocks'],
            'zorder': 10
        }

        kwargs['team_bench_area'] = {
            'class': basketball.TeamBenchArea,
            'x_anchor': (self.court_length / 2.0) - self.team_bench_area_x -
            self.line_thickness,
            'y_anchor': self.court_width / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': self.team_bench_area_width,
            'extension_direction': 'outward',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['team_bench_area'],
            'edgecolor': self.fiba_colors['team_bench_area'],
            'zorder': 16
        }

        kwargs['throw_in_line'] = {
            'class': basketball.ThrowInLine,
            'x_anchor': (self.court_length / 2.0) - 8.325 -
            self.line_thickness,
            'y_anchor': -(self.court_width / 2.0) - self.line_thickness,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': False,
            'is_constrained': False,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'feature_width': 0.15,
            'extension_direction': 'outward',
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.fiba_colors['throw_in_line'],
            'edgecolor': self.fiba_colors['throw_in_line'],
            'zorder': 16
        }

        super().__init__(court_length = 28.0, court_width = 15.0,
                         court_units = 'm', line_thickness = 0.05,
                         basket_to_baseline_dist = 1.575,
                         ring_center_to_backboard = 0.375,
                         backboard_face_size = 1.80,
                         baseline_apron_extension_length = 6.0,
                         sideline_apron_extension_width = 5.0,
                         center_circle_radius = 1.80,
                         sideline_to_corner_three_point_dist = 0.90,
                         three_point_arc_distance = 6.75,
                         free_throw_dist = 4.225,
                         free_throw_lane_width = 4.90,
                         free_throw_circle_radius = 1.8,
                         free_throw_circle_extended_arc = 0.0,
                         restricted_arc_outer_radius = 1.30,
                         backboard_thickness = 0.05,
                         basket_ring_radius = 0.225,
                         ring_extension_width = 0.126,
                         coaches_box = {'visible': False},
                         substitution_area = {'visible': False},
                         substitution_area_length = 10.0,
                         colors_dict = self.fiba_colors, **kwargs)


class NFHSCourt(BasketballCourt):
    """A regulation high school basketball court.

    These are the dimensions specified by the National Federation of State High
    School Associations.

    Please see the BasketballCourt documentation for full details.
    """

    def __init__(self, court_length = 84.0, court_width = 50.0,
                 court_units = 'ft', line_thickness = 2.0 / 12.0,
                 colors_dict = {}, **kwargs):

        self.court_length = court_length
        self.court_width = court_width
        self.court_units = court_units
        self.line_thickness = line_thickness

        nfhs_colors = {
            'inner_center_circle_outline': '#000000',
            'inner_center_circle_fill': '#d2ab6f',
            'blocks': '#000000',
        }

        self.nfhs_colors = {**nfhs_colors, **colors_dict}

        # Initialize the blocks
        kwargs['block_1_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 7.0 - (11.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nfhs_colors['blocks'],
            'edgecolor': self.nfhs_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_2_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 11.0 + (1.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nfhs_colors['blocks'],
            'edgecolor': self.nfhs_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_3_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 14.25,
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nfhs_colors['blocks'],
            'edgecolor': self.nfhs_colors['blocks'],
            'zorder': 10
        }

        kwargs['block_4_params'] = {
            'class': basketball.Block,
            'x_anchor': (self.court_length / 2.0) - 17 - (5.0 / 12.0),
            'y_anchor': 6.0 + (4.0 / 12.0),
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': True,
            'reflect_y': True,
            'is_constrained': True,
            'visible': True,
            'court_length': self.court_length,
            'court_width': self.court_width,
            'block_length': 2.0 / 12.0,
            'block_width': 8.0 / 12.0,
            'feature_radius': 0.0,
            'feature_thickness': self.line_thickness,
            'facecolor': self.nfhs_colors['blocks'],
            'edgecolor': self.nfhs_colors['blocks'],
            'zorder': 10
        }

        super().__init__(court_length = self.court_length,
                         court_width = self.court_width,
                         court_units = self.court_units,
                         line_thickness = self.line_thickness,
                         basket_to_baseline_dist = 5.0 + (3.0 / 12.0),
                         ring_center_to_backboard = (15.0 / 12.0),
                         backboard_face_size = (72.0 / 12.0),
                         baseline_apron_extension_length = 3.0,
                         sideline_apron_extension_width = 3.0,
                         center_circle_radius = 6.0,
                         sideline_to_corner_three_point_dist = 5.25,
                         three_point_arc_distance = 19.0 + (9.0 / 12.0),
                         free_throw_dist = 15.0,
                         free_throw_lane_width = 12.0,
                         free_throw_circle_radius = 6.0,
                         free_throw_circle_extended_arc = 0.0,
                         restricted_arc_outer_radius = 0.0,
                         backboard_thickness = (4.0 / 12.0),
                         basket_ring_radius = (9.0 / 12.0),
                         ring_extension_width = (7.0 / 12.0),
                         coaches_box = {'visible': False},
                         restricted_arc = {'visible': False},
                         substitution_area = {'visible': False},
                         colors_dict = self.nfhs_colors, **kwargs)
