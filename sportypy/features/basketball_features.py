"""Extensions of the BaseFeature class to be specific to basketball courts.

The features are all parameterized by the basic characteristics of an ice
court, with the default being an NBA basketball court. A user can manually
specify their own court parameters in the BasketballCourt() class that will
adjust the placement of these features, however the features themselves will be
consistent across all basketball surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseBasketballFeature(BaseFeature):
    """An extension of the BaseFeature class specifically for basketball.

    The following attributes are specific to basketball features only. For more
    information on inherited attributes, please see the BaseFeature class
    definition. The default values are provided to ensure that the feature can
    at least be created, and will default to a regulation NBA court.

    Attributes
    ----------
    court_length : float (default: 200.0)
        The length of the court in TV view

    court_width : float (default: 85.0)
        The width of the court in TV view

    feature_radius : float (default: 0.0)
        The radius needed to draw the feature. This may not be needed for all
        features

    feature_thickness : float (default: 0.0)
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed
    """

    def __init__(self, court_length = 94.0, court_width = 50.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = 'ft', *args, **kwargs):

        # Set the full-sized dimensions of the court
        self.court_length = court_length
        self.court_width = court_width

        # Set the half-court dimensions
        self.half_court_length = self.court_length / 2.0
        self.half_court_width = self.court_width / 2.0

        # Set the units for reference
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness

        super().__init__(*args, **kwargs)


class CourtConstraint(BaseBasketballFeature):
    """The constraint around the court.

    This confines all interior features to be constrained inside the court, as
    well as any interior plots.
    """

    def _get_centered_feature(self):
        court_constraint_df = self.create_rectangle(
            x_min = -self.half_court_length,
            x_max = self.half_court_length,
            y_min = -self.half_court_width,
            y_max = self.half_court_width
        )

        return court_constraint_df


class HalfCourt(BaseBasketballFeature):
    """Each half of the court.

    This allows greater control over each part of the court.
    """

    def __init__(self, court_side = 'offense', *args, **kwargs):
        # Determine the half of the court
        self.court_side = court_side

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        if self.court_side == 'defense':
            halfcourt_xmin = -self.half_court_length
            halfcourt_xmax = 0.0

        else:
            # Otherwise, it is the offensive half and the minimum and maximum
            # values should flip
            halfcourt_xmin = 0.0
            halfcourt_xmax = self.half_court_length

        half_court_df = self.create_rectangle(
            x_min = halfcourt_xmin,
            x_max = halfcourt_xmax,
            y_min = -self.half_court_width,
            y_max = self.half_court_width
        )

        return half_court_df


class CenterCircleOutline(BaseBasketballFeature):
    """The circle that surrounds mid-court.

    This may be part of a concentric set of circles, or may be a singular
    circle. If this is concentric, this class should be instantiated twice:
    once for each circle.
    """

    def _get_centered_feature(self):
        # The circle should be created as a half-ring with the appropriate
        # thickness
        center_circle_df = pd.concat([
            pd.DataFrame({
                'x': [
                    0
                ],

                'y': [
                    self.feature_radius
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 0.5,
                end = -0.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    0,
                    0
                ],

                'y': [
                    -self.feature_radius,
                    -self.feature_radius + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = -0.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    0
                ],

                'y': [
                    self.feature_radius
                ]
            })
        ])

        return center_circle_df


class CenterCircleFill(BaseBasketballFeature):
    """The circle that surrounds mid-court.

    This may be part of a concentric set of circles, or may be a singular
    circle. If this is concentric, this class should be instantiated twice:
    once for each circle.
    """

    def _get_centered_feature(self):
        # The circle should be created as a half-ring with the appropriate
        # thickness
        center_circle_df = self.create_circle(
            center = (0, 0),
            start = 0.5,
            end = -0.5,
            r = self.feature_radius - self.feature_thickness
        )

        return center_circle_df


class DivisionLine(BaseBasketballFeature):
    """The half-court line, also known as the division line.

    This is the line that divides the court evenly in half.
    """

    def _get_centered_feature(self):
        time_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.half_court_width,
            y_max = self.half_court_width
        )

        return time_line_df


class EndLine(BaseBasketballFeature):
    """The boundary line underneath the basket, also known as the end line.

    The boundary line is considered out of bounds, so its interior edge is used
    to create the constraint of the court. See the documentation for
    CourtConstraint for full details.
    """

    def _get_centered_feature(self):
        end_line_df = self.create_rectangle(
            x_min = 0,
            x_max = self.feature_thickness,
            y_min = -self.half_court_width - self.feature_thickness,
            y_max = self.half_court_width + self.feature_thickness
        )

        return end_line_df


class SideLine(BaseBasketballFeature):
    """The boundary line that runs the length of the court, aka the sideline.

    The boundary line is considered out of bounds, so its interior edge is used
    to create the constraint of the court. See the documentation for
    CourtConstraint for full details.
    """

    def _get_centered_feature(self):
        side_line_df = self.create_rectangle(
            x_min = -self.half_court_length - self.feature_thickness,
            x_max = self.half_court_length + self.feature_thickness,
            y_min = 0.0,
            y_max = self.feature_thickness
        )

        return side_line_df


class CourtApron(BaseBasketballFeature):
    """The court's apron is the coloring beyond the boundary of the court.

    The apron is usually a constrasting color from the court's surface, and may
    either be the same color or different from the lines on the court.
    """

    def __init__(self, baseline_extension = 8.0, sideline_extension = 4.0,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.baseline_extension = baseline_extension
        self.sideline_extension = sideline_extension

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # The court's apron extends beyond the boundaries of the court's
        # playing surface
        apron_df = pd.DataFrame({
            'x': [
                0,
                self.half_court_length + self.baseline_extension,
                self.half_court_length + self.baseline_extension,
                0,
                0,
                self.half_court_length,
                self.half_court_length,
                0,
                0
            ],

            'y': [
                self.half_court_width + self.sideline_extension,
                self.half_court_width + self.sideline_extension,
                -self.half_court_width - self.sideline_extension,
                -self.half_court_width - self.sideline_extension,
                -self.half_court_width,
                -self.half_court_width,
                self.half_court_width,
                self.half_court_width,
                self.half_court_width + self.sideline_extension
            ]
        })

        return apron_df


class ThreePointLine(BaseBasketballFeature):
    """The three-point line and arc.

    Attributes
    ----------
    feature_width : float (default: 44.0)
        The width of the extension, from outside edge to outside edge, along a
        line that runs through the center of the basket

    This is subject to vary based on the league.
    """

    def __init__(self, feature_width = 44.0, basket_to_baseline_dist = -5.25,
                 *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.feature_width = feature_width
        self.basket_to_baseline_dist = basket_to_baseline_dist

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # Start by calculating the angle through which the arc will trace. The
        # following explanation uses NBA dimensions, however the process is
        # the same no matter the governing body.

        # First, a bit of math is needed to determine the starting and ending
        # angles of the three-point arc, relative to 0 radians. Since in the
        # end, the angle is what matters, the units of measure do not. Inches
        # are easier to use for this calculation.
        start_y_outer = (self.feature_width / 2.0)

        # The rule book describes the arc as having a radius of 23' 9" to the
        # outside of the three-point arc from the center of the basket
        radius_outer = self.feature_radius

        # From here, the calculation is relatively straightforward. To
        # determine the angle, the inverse sine is needed. It will be
        # multiplied by pi so that it can be passed to the self.create_circle()
        # method
        start_angle_outer = math.asin(start_y_outer / radius_outer) / np.pi
        end_angle_outer = -start_angle_outer

        # The same technique can be used to find the inner angles, however,
        # since the inner radius will be traced from bottom to top, the angle
        # must be negative to start
        start_y_inner = start_y_outer - self.feature_thickness
        radius_inner = self.feature_radius - self.feature_thickness
        start_angle_inner = -math.asin(start_y_inner / radius_inner) / np.pi
        end_angle_inner = -start_angle_inner

        three_point_line_df = pd.concat([
            pd.DataFrame({
                'x': [
                    0.0
                ],

                'y': [
                    self.feature_width / 2.0
                ]
            }),

            self.create_circle(
                center = (self.basket_to_baseline_dist, 0.0),
                start = start_angle_outer,
                end = end_angle_outer,
                r = radius_outer
            ),

            pd.DataFrame({
                'x': [
                    0.0,
                    0.0
                ],

                'y': [
                    -self.feature_width / 2.0,
                    -(self.feature_width / 2.0) + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (self.basket_to_baseline_dist, 0.0),
                start = start_angle_inner,
                end = end_angle_inner,
                r = radius_inner
            ),

            pd.DataFrame({
                'x': [
                    0.0,
                    0.0
                ],

                'y': [
                    (self.feature_width / 2.0) - self.feature_thickness,
                    self.feature_width / 2.0
                ]
            })
        ])

        return three_point_line_df


class TwoPointRange(BaseBasketballFeature):
    """The area inside of the three-point arc where baskets are worth 2 points.

    Attributes
    ----------
    extension_length : float (default: 14.0)
        The length of the straight extension from the baseline to the beginning
        of the arc

    feature_width : float (default: 44.0)
        The width of the extension, from outside edge to outside edge, along a
        line that runs through the center of the basket

    This is subject to vary based on the league.
    """

    def __init__(self, extension_length = 14.0, feature_width = 44.0,
                 basket_to_baseline_dist = -41.75, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.extension_length = extension_length
        self.feature_width = feature_width
        self.basket_to_baseline_dist = basket_to_baseline_dist

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # Start by calculating the angle through which the arc will trace. The
        # following explanation uses NBA dimensions, however the process is
        # the same no matter the governing body.

        # First, a bit of math is needed to determine the starting and ending
        # angles of the three-point arc, relative to 0 radians. Since in the
        # end, the angle is what matters, the units of measure do not. Inches
        # are easier to use for this calculation.
        start_y_outer = (self.feature_width / 2.0)

        # The same technique can be used to find the inner angles, however,
        # since the inner radius will be traced from bottom to top, the angle
        # must be negative to start
        start_y_inner = start_y_outer - self.feature_thickness
        radius_inner = self.feature_radius - self.feature_thickness
        start_angle_inner = -math.asin(start_y_inner / radius_inner) / np.pi
        end_angle_inner = -start_angle_inner

        two_point_range_df = pd.concat([
            pd.DataFrame({
                'x': [
                    0.0
                ],

                'y': [
                    -(self.feature_width / 2.0) + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (self.basket_to_baseline_dist, 0.0),
                start = start_angle_inner,
                end = end_angle_inner,
                r = radius_inner
            ),

            pd.DataFrame({
                'x': [
                    0.0
                ],

                'y': [
                    (self.feature_width / 2.0) - self.feature_thickness
                ]
            })
        ])

        return two_point_range_df


class FreeThrowLaneBoundary(BaseBasketballFeature):
    """The boundary of the free throw lane on the court.

    This is only to describe its boundary, not its painted area or any features
    contained within. This also does not describe the free-throw circle.
    """

    def __init__(self, lane_length = 19.0, lane_width = 16.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.lane_length = lane_length
        self.lane_width = lane_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        free_throw_lane_boundary_df = pd.DataFrame({
            'x': [
                self.half_court_length,
                self.half_court_length - self.lane_length,
                self.half_court_length - self.lane_length,
                self.half_court_length,
                self.half_court_length,
                self.half_court_length - self.lane_length +
                self.feature_thickness,
                self.half_court_length - self.lane_length +
                self.feature_thickness,
                self.half_court_length,
                self.half_court_length
            ],

            'y': [
                self.lane_width / 2.0,
                self.lane_width / 2.0,
                -(self.lane_width / 2.0),
                -(self.lane_width / 2.0),
                -(self.lane_width / 2.0) + self.feature_thickness,
                -(self.lane_width / 2.0) + self.feature_thickness,
                (self.lane_width / 2.0) - self.feature_thickness,
                (self.lane_width / 2.0) - self.feature_thickness,
                self.lane_width / 2.0
            ]
        })

        return free_throw_lane_boundary_df


class FreeThrowCircleOutline(BaseBasketballFeature):
    """The semi-circle that encloses the area where a free-throw is taken.

    This the outline, not the legal free-throw shooting area.
    """

    def __init__(self, arc_length_behind_ft_line = 0.0,
                 free_throw_lane_length = 19.0, *args, **kwargs):
        # Initialize the attributes that are unique to this feature
        self.arc_length_behind_ft_line = arc_length_behind_ft_line
        self.free_throw_lane_length = free_throw_lane_length

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # The angle theta must be calculated to determine where to start
        # drawing the free-throw circle. It's possible that an arc length may
        # be needed to be added on the side of the free-throw line closest to
        # the basket. The starting angle can be determined via the relationship
        # s = r*theta, where s is the arc length, r is the radius, and theta is
        # the angle (in radians)

        # If there is an arc length to be added to the side of the free-throw
        # line closest to the basket, it should be included here. Setting this
        # to zero will result in the starting angle being 0.5 * pi
        s = self.arc_length_behind_ft_line

        # Get the (outer) radius of the circle being drawn
        r = self.feature_radius

        # Compute the starting angle to draw the free-throw circle. Since the
        # self.create_circle() method requires the starting angle to be passed
        # in radians / pi, this must be divided out
        theta = (s / r) / np.pi

        # The starting and ending angles are thus given as 0.5 +/- the theta
        # calculated above
        start_angle = 0.5 - theta
        end_angle = 1.5 + theta

        # Get the coordinates for the center of the free-throw line
        x_cent = self.half_court_length - self.free_throw_lane_length +\
            (self.feature_thickness / 2.0)
        y_cent = 0.0

        free_throw_circle_df = pd.concat([
            self.create_circle(
                center = (x_cent, y_cent),
                start = start_angle,
                end = end_angle,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (x_cent, y_cent),
                start = end_angle,
                end = start_angle,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return free_throw_circle_df


class FreeThrowCircleOutlineDash(BaseBasketballFeature):
    """The dashed portion of a free-throw circle.

    This is not required on all courts, but as it appears on an NBA and WNBA
    court, it should be included and distinguished from the rest of the
    free-throw circle's outline.
    """

    def __init__(self, start_angle = 0.0, end_angle = 2.0,
                 free_throw_lane_length = 19.0, *args, **kwargs):
        # Initialize the attributes that are unique to this feature
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.free_throw_lane_length = free_throw_lane_length

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # Get the coordinates for the center of the free-throw line
        x_cent = (self.half_court_length) - self.free_throw_lane_length +\
            (self.feature_thickness / 2.0)
        y_cent = 0

        free_throw_circle_df = pd.concat([
            self.create_circle(
                center = (x_cent, y_cent),
                start = self.start_angle,
                end = self.end_angle,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (x_cent, y_cent),
                start = self.end_angle,
                end = self.start_angle,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return free_throw_circle_df


class Paint(BaseBasketballFeature):
    """The painted area inside of the free-throw lane, also known as the paint.

    This is only to describe the paint, not its boundary or any features
    around it. This also does not describe the free-throw circle.
    """

    def __init__(self, lane_length = 19.0, lane_width = 16.0, *args, **kwargs):
        # Initialize the attributes unique to this feature
        self.lane_length = lane_length
        self.lane_width = lane_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        paint_df = self.create_rectangle(
            x_min = (self.half_court_length) - self.lane_length +
            self.feature_thickness,
            x_max = (self.half_court_length),
            y_min = -(self.lane_width / 2.0) + self.feature_thickness,
            y_max = (self.lane_width / 2.0) - self.feature_thickness
        )

        return paint_df


class Block(BaseBasketballFeature):
    """The blocks around the free-throw lane.

    The size of the blocks vary by league, but there are usually four blocks
    along the free-throw lane.
    """

    def __init__(self, block_length = 2.0 / 12.0, block_width = 0.5, *args,
                 **kwargs):
        # Initialize the attribute unique to the feature
        self.block_length = block_length
        self.block_width = block_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        block_df = self.create_rectangle(
            x_min = -self.block_length / 2.0,
            x_max = self.block_length / 2.0,
            y_min = -self.block_width / 2.0,
            y_max = self.block_width / 2.0
        )

        return block_df


class RestrictedArc(BaseBasketballFeature):
    """The restricted arc under the basket.

    The outer radius should be used when specifying the feature radius.
    """

    def __init__(self, basket_center_x = 41.75, backboard_face_x = 43.0, *args,
                 **kwargs):
        # Initialize the attribute unique to the feature
        self.basket_center_x = basket_center_x
        self.backboard_face_x = backboard_face_x

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        restricted_arc_df = pd.concat([
            pd.DataFrame({
                'x': [
                    self.backboard_face_x
                ],

                'y': [
                    self.feature_radius
                ]
            }),

            self.create_circle(
                center = (self.basket_center_x, 0.0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    self.backboard_face_x,
                    self.backboard_face_x
                ],

                'y': [
                    -self.feature_radius,
                    -self.feature_radius + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (self.basket_center_x, 0.0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    self.backboard_face_x,
                    self.backboard_face_x
                ],

                'y': [
                    self.feature_radius - self.feature_thickness,
                    self.feature_radius
                ]
            })
        ])

        return restricted_arc_df


class Backboard(BaseBasketballFeature):
    """The backboard of the goal.

    The thickness determines how far in the x direction the backboard should
    extend.
    """

    def __init__(self, feature_width = (72.0 / 12.0), *args, **kwargs):
        # Initialize the attribute unique to the feature
        self.feature_width = feature_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        backboard_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = -self.feature_width / 2.0,
            y_max = self.feature_width / 2.0
        )

        return backboard_df


class CoachesBox(BaseBasketballFeature):
    """The coaching box markings on the court.

    The positioning should be done using the interior edge markings with
    respect to the baseline.
    """

    def __init__(self, feature_width = 3.0, extension_direction = 'inward',
                 *args, **kwargs):
        # Initialize the attribute that is unique to this feature
        self.feature_width = feature_width
        self.extension_direction = extension_direction

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        if self.extension_direction == 'inward':
            coaches_box_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width,
                y_max = 0.0
            )

        elif self.extension_direction == 'outward':
            coaches_box_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = 0.0,
                y_max = self.feature_width
            )

        else:
            coaches_box_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width / 2.0,
                y_max = self.feature_width / 2.0
            )

        return coaches_box_df


class SubstitutionArea(BaseBasketballFeature):
    """The substitution area in front of the scorer's table.

    These lines extend outward from the sideline.
    """

    def __init__(self, feature_width = 4.0, *args,
                 **kwargs):
        # Initialize the attribute that is unique to this feature
        self.feature_width = feature_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        coaches_box_df = self.create_rectangle(
            x_min = 0.0,
            x_max = self.feature_thickness,
            y_min = 0.0,
            y_max = self.feature_width
        )

        return coaches_box_df


class BasketRing(BaseBasketballFeature):
    """The ring of the basket.

    The ring extension is the distance between the face of the backboard and
    the center of the ring. By default, this will have a thickness of 2 inches,
    although in practicality it is significantly less.
    """

    def __init__(self, ring_extension_width = (7.0 / 12.0),
                 basket_center_x = 41.75, backboard_face_x = 43.0, *args,
                 **kwargs):
        # Initialize the attributes unique to the feature
        self.ring_extension_width = ring_extension_width
        self.basket_center_x = basket_center_x
        self.backboard_face_x = backboard_face_x

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # The below mathematical description uses the dimensions for an NBA
        # basket ring, although the calculation is generalizable to any league

        # The connector has a width of 7", so 3.5" are on either side of the x
        # axis. The ring has a radius of 9", so the arcsine of these
        # measurements should give the angle at which point they connect
        half_extension_width = self.ring_extension_width / 2.0
        start_angle = math.asin(half_extension_width / self.feature_radius)
        start_angle = np.pi - start_angle
        end_angle = -start_angle

        basket_ring_df = pd.concat([
            pd.DataFrame({
                'x': [
                    self.backboard_face_x,
                    self.basket_center_x +
                    (self.feature_radius * math.cos(start_angle))
                ],

                'y': [
                    half_extension_width,
                    half_extension_width
                ]
            }),

            self.create_circle(
                center = (self.basket_center_x, 0.0),
                start = start_angle,
                end = end_angle,
                r = self.feature_radius + self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    self.basket_center_x +
                    (self.feature_radius * math.cos(start_angle)),
                    self.backboard_face_x,
                    self.backboard_face_x
                ],

                'y': [
                    -half_extension_width,
                    -half_extension_width,
                    half_extension_width
                ]
            }),
        ])

        return basket_ring_df


class Net(BaseBasketballFeature):
    """The netting of the basket.

    The netting will represent the interior of the basket ring.
    """

    def __init__(self, basket_center_x = 41.75, *args, **kwargs):
        # Initialize the attributes unique to the feature
        self.basket_center_x = basket_center_x

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        net_df = self.create_circle(
            center = (self.basket_center_x, 0.0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return net_df


class DefensiveBoxMark(BaseBasketballFeature):
    """The lower defensive box markings.

    Some courts have four hash marks in/around the lane that represent the
    lower defensive box. The positioning of these markings may vary by league.
    """

    def __init__(self, mark_length = 0.5, mark_width = 2.0 / 12.0, *args,
                 **kwargs):
        # Initialize the attributes unique to the feature
        self.mark_length = mark_length
        self.mark_width = mark_width

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        defensive_box_mark_df = self.create_rectangle(
            x_min = -self.mark_length,
            x_max = 0.0,
            y_min = 0.0,
            y_max = self.mark_width
        )

        return defensive_box_mark_df


class TeamBenchArea(BaseBasketballFeature):
    """The team bench area markings on the court.

    The positioning should be done using the interior edge markings with
    respect to the baseline.
    """

    def __init__(self, feature_width = 6.0 + (2.0 / 12.0),
                 extension_direction = 'both', *args, **kwargs):
        # Initialize the attribute that is unique to this feature
        self.feature_width = feature_width
        self.extension_direction = extension_direction

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        if self.extension_direction == 'inward':
            team_bench_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width,
                y_max = 0.0
            )

        elif self.extension_direction == 'outward':
            team_bench_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = 0.0,
                y_max = self.feature_width
            )

        else:
            team_bench_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width / 2.0,
                y_max = self.feature_width / 2.0
            )

        return team_bench_df


class ThrowInLine(BaseBasketballFeature):
    """The throw-in line markings on the court.

    The positioning should be done using the interior edge markings with
    respect to the baseline.
    """

    def __init__(self, feature_width = 3.0, extension_direction = 'inward',
                 *args, **kwargs):
        # Initialize the attribute that is unique to this feature
        self.feature_width = feature_width
        self.extension_direction = extension_direction

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        if self.extension_direction == 'outward':
            throw_in_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width,
                y_max = 0.0
            )

        elif self.extension_direction == 'inward':
            throw_in_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = 0.0,
                y_max = self.feature_width
            )

        else:
            throw_in_line_df = self.create_rectangle(
                x_min = 0.0,
                x_max = self.feature_thickness,
                y_min = -self.feature_width / 2.0,
                y_max = self.feature_width / 2.0
            )

        return throw_in_line_df
