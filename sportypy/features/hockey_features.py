"""Extensions of the BaseFeature class to be specific to hockey rinks.

The features are all parameterized by the basic characteristics of an ice rink,
with the default being an NHL ice rink. A user can manually specify their own
rink parameters in the HockeyRink() class that will adjust the placement of
these features, however the features themselves will be consistent across all
hockey surfaces.

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd
from sportypy._base_classes._base_feature import BaseFeature


class BaseHockeyFeature(BaseFeature):
    """An extension of the BaseFeature class specifically for hockey.

    The following attributes are specific to hockey features only. For more
    information on inherited attributes, please see the BaseFeature class
    definition. The default values are provided to ensure that the feature can
    at least be created, and will default to a regulation NHL ice rink.

    Attributes
    ----------
    rink_length : float (default: 200.0)
        The length of the rink in TV view

    rink_width : float (default: 85.0)
        The width of the rink in TV view

    feature_radius : float (default: 0.0)
        The radius needed to draw the feature. This may not be needed for all
        features

    feature_thickness : float (default: 0.0)
        The thickness with which to draw the feature. This is normally given
        as the horizontal width of the feature in TV view, however it may be
        used to specify other thicknesses as needed
    """

    def __init__(self, rink_length = 200.0, rink_width = 85.0,
                 feature_radius = 0.0, feature_thickness = 0.0,
                 feature_units = 'ft', *args, **kwargs):

        # Set the full-sized dimensions of the rink
        self.rink_length = rink_length
        self.rink_width = rink_width
        self.feature_units = feature_units

        # Set the characteristics of the feature
        self.feature_radius = feature_radius
        self.feature_thickness = feature_thickness
        super().__init__(*args, **kwargs)

    def _reflect(self, df, over_x = False, over_y = True):
        """Reflect a data frame's coordinates over the desired axes.

        Parameters
        ----------
        df : pandas.DataFrame
            A data frame with points to reflect

        over_x : bool (default: False)
            Whether or not to reflect the points over the x axis

        over_y : bool (default: False)
            Whether or not to reflect the points over the y axis

        Returns
        -------
        out_df : pandas.DataFrame
            The data frame with the appropriate reflections
        """
        out_df = df.copy()
        if over_x:
            out_df['y'] = -1 * df['y']
        if over_y:
            out_df['x'] = -1 * df['x']

        return out_df


class Boards(BaseHockeyFeature):
    """Get the boards.

    One half of the rink's boards.

    The rink's boards are rounded in the arc of a circle of a given radius, so
    the x and y coordinates of its center must be taken and shifted to the
    correct place.
    """

    def _get_centered_feature(self):
        """Generate the coordinates needed to form the boards.

        The boards are comprised of a closed polygon of defined thickness via
        the board_thickness attribute.
        """
        # Specify the half-dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Calculate the corner arc's inner radius
        arc_inner_upper = self.create_circle(
            center = (center_x, center_y),
            r = self.feature_radius,
            start = 0.5,
            end = 0.0
        )

        arc_inner_lower = self.create_circle(
            center = (center_x, -center_y),
            r = self.feature_radius,
            start = 0.0,
            end = -0.5
        )

        # Calculate the corner arc's outer radius
        arc_outer_upper = self.create_circle(
            center = (center_x, center_y),
            r = self.feature_radius + self.feature_thickness,
            start = 0.0,
            end = 0.5
        )

        arc_outer_lower = self.create_circle(
            center = (center_x, -center_y),
            r = self.feature_radius + self.feature_thickness,
            start = -0.5,
            end = 0.0
        )

        # Combine the boards' inner and outer arcs with its guaranteed
        # coordinates
        boards_df = pd.concat([
            # Start at the top of the rink in TV view with the boards' inner
            # boundary
            pd.DataFrame({
                'x': [0],
                'y': [half_width]
            }),

            # Then add in its upper innner arc
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                'x': [half_length],
                'y': [0]
            }),

            # Then its lower inner arc
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before flipping to the outer boundary
            pd.DataFrame({
                'x': [0, 0],
                'y': [-half_width, -half_width - self.feature_thickness]
            }),

            # Back to the lower arc on the outer boundary
            arc_outer_lower,

            # Then back to the middle
            pd.DataFrame({
                'x': [half_length + self.feature_thickness],
                'y': [0]
            }),

            # Then back to the upper arc
            arc_outer_upper,

            # Finally back to the top and original starting point
            pd.DataFrame({
                'x': [0, 0],
                'y': [half_width + self.feature_thickness, half_width]
            })
        ])

        return boards_df


class BoardsConstraint(BaseHockeyFeature):
    """Get the constraint of the boards.

    This corresponds to the inner edge of the boards and is used to
    constrain other features from extending beyond the inner boundary of the
    ice rink.

    Unlike the Boards class above, this feature is designed to function over
    the entire surface of an ice rink

    feature_radius is the radius of the circle that forms the arc-like
    corners of the boards
    """

    def _get_centered_feature(self):
        """Generate the coordinates of the inner edge of the boards.

        The boards are comprised of a closed polygon of defined thickness via
        the feature_thickness attribute.
        """
        # Specify the half-dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Calculate the corner arcs
        arc_upper_right = self.create_circle(
            center = (center_x, center_y),
            r = self.feature_radius,
            start = 0.5,
            end = 0.0
        )

        arc_lower_right = self.create_circle(
            center = (center_x, -center_y),
            r = self.feature_radius,
            start = 0.0,
            end = -0.5
        )

        arc_lower_left = self.create_circle(
            center = (-center_x, -center_y),
            r = self.feature_radius,
            start = -0.5,
            end = -1.0
        )

        arc_upper_left = self.create_circle(
            center = (-center_x, center_y),
            r = self.feature_radius,
            start = 1.0,
            end = 0.5
        )

        # Combine the boards' inner and outer arcs with its guaranteed
        # coordinates
        boards_constraint_df = pd.concat([
            # Start at the top of the rink in TV view with the boards' inner
            # boundary
            pd.DataFrame({
                'x': [0],
                'y': [half_width]
            }),

            # Then add in its upper right corner
            arc_upper_right,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                'x': [half_length],
                'y': [0]
            }),

            # Then its lower right corner
            arc_lower_right,

            # Then go to the bottom of the rink in TV view
            pd.DataFrame({
                'x': [0],
                'y': [-half_width]
            }),

            # Now continue to the lower left corner
            arc_lower_left,

            # Then back to the middle
            pd.DataFrame({
                'x': [-half_length],
                'y': [0]
            }),

            # Then the upper left corner
            arc_upper_left,

            # Finally back to the top and original starting point
            pd.DataFrame({
                'x': [0],
                'y': [half_width]
            })
        ])

        return boards_constraint_df


class NeutralZone(BaseHockeyFeature):
    """Get the neutral zone.

    The area of the ice between the two zone lines.

    This is the middle "third" of the rink. Its center should lie along the
    line x = 0.
    """

    def _get_centered_feature(self):
        """Create the neutral zone.

        The zone is rectangular in shape, and usually is white in color.
        """
        nzone_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.rink_width / 2.0,
            y_max = self.rink_width / 2.0
        )

        return nzone_df


class OffensiveZone(BaseHockeyFeature):
    """Get the offensive zone.

    The attacking area of the ice.

    This is the right "third" of the rink in TV view.
    """

    def __init__(self, nzone_length = 0.0, *args, **kwargs):
        self.nzone_length = nzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Create the offensive zone.

        The zone is rectangular in shape with rounded corners (that will be
        constrained by the boards), and usually is white in color.
        """
        # Specify the dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find where the point to use as the center of the circle with the
        # given radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Calculate the corner arc's inner radius
        arc_inner_upper = self.create_circle(
            center = (center_x, center_y),
            r = self.feature_radius,
            start = 0.5,
            end = 0.0
        )

        arc_inner_lower = self.create_circle(
            center = (center_x, -center_y),
            r = self.feature_radius,
            start = 0.0,
            end = -0.5
        )

        ozone_df = pd.concat([
            # Start at the upper left corner of the zone line that is closest
            # to center ice
            pd.DataFrame({
                'x': [self.nzone_length / 2.0],
                'y': [half_width]
            }),

            # Then draw the upper right corner of the boards
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                'x': [half_length],
                'y': [0.0]
            }),

            # Then the lower right corner
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before closing the path by returning to the
            # starting point
            pd.DataFrame({
                'x': [self.nzone_length / 2.0, self.nzone_length / 2.0],
                'y': [-half_width, half_width]
            })
        ])

        return ozone_df


class DefensiveZone(BaseHockeyFeature):
    """Get the defensive zone.

    The defending area of the ice.

    This is the left "third" of the rink in TV view.
    """

    def __init__(self, nzone_length = 0.0, *args, **kwargs):
        self.nzone_length = nzone_length
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        """Create the offensive zone.

        The zone is rectangular in shape with rounded corners (that will be
        constrained by the boards), and usually is white in color.
        """
        # Specify the dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find where the point to use as the center of the circle with the
        # given radius for the boards' corners' arc
        center_x = half_length - self.feature_radius
        center_y = half_width - self.feature_radius

        # Calculate the corner arc's inner radius
        arc_inner_upper = self.create_circle(
            center = (-center_x, center_y),
            r = self.feature_radius,
            start = 0.5,
            end = 1.0
        )

        arc_inner_lower = self.create_circle(
            center = (-center_x, -center_y),
            r = self.feature_radius,
            start = 1.0,
            end = 1.5
        )

        dzone_df = pd.concat([
            # Start at the upper right corner of the zone line that is closest
            # to center ice
            pd.DataFrame({
                'x': [-self.nzone_length / 2.0],
                'y': [half_width]
            }),

            # Then draw the upper left arc of the boards
            arc_inner_upper,

            # Then its guaranteed point at half the length of the rink
            pd.DataFrame({
                'x': [-half_length],
                'y': [0.0]
            }),

            # Then the lower left arc
            arc_inner_lower,

            # Then go to the bottom of the rink in TV view with the boards'
            # inner boundary before closing the path by returning to the
            # starting point
            pd.DataFrame({
                'x': [-self.nzone_length / 2.0, -self.nzone_length / 2.0],
                'y': [-half_width, half_width]
            })
        ])

        return dzone_df


class CenterLine(BaseHockeyFeature):
    """Get the center line.

    The center line is the line that divides the ice surface in half.

    This line spans the entire width of the ice rink. The center of this line
    runs through the line x = 0.
    """

    def _get_centered_feature(self):
        """Create the center line.

        The line is rectangular in shape, and usually red in color.
        """
        # Create the center line
        center_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.rink_width / 2.0,
            y_max = self.rink_width / 2.0
        )

        return center_line_df


class ZoneLine(BaseHockeyFeature):
    """Get the zone lines.

    The zone lines are the lines that separate the neutral zone from the
    offensive and defensive zones of the ice.

    By convention, the offensive zone is defined to be on the +x side of the
    ice (where the center of the ice corresponds to the coordinate system's
    origin) and the defensive zone corresponds to the -x side of the ice
    """

    def _get_centered_feature(self):
        """Create the zone line.

        This line spans the entire width of the ice rink. The distance between
        the inner edges of these lines are what comprise the neutral zone
        """
        # Create the neutral zone line
        zone_line_df = self.create_rectangle(
            x_min = -self.feature_thickness / 2.0,
            x_max = self.feature_thickness / 2.0,
            y_min = -self.rink_width / 2.0,
            y_max = self.rink_width / 2.0
        )

        return zone_line_df


class GoalLine(BaseHockeyFeature):
    """Get the goal lines.

    The goal lines are the lines that a puck must cross in order to score a
    goal.

    This line stretches the width of the ice surface, but may be constrained by
    the curvature of the boards.
    """

    def __init__(self, goal_line_anchor = 11.0, *args, **kwargs):
        # Set the goal line's anchor property
        self.goal_line_anchor = goal_line_anchor
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # Specify the half-dimensions of the rink
        half_length = self.rink_length / 2.0
        half_width = self.rink_width / 2.0

        # Find the point to use as the center of the circle with the given
        # radius for the boards' corners' arc
        corner_arc_center_x = half_length - self.feature_radius
        corner_arc_center_y = half_width - self.feature_radius

        # First, check to see if the goal line will intersect the corner of the
        # rink. Usually, it will, but in case a user supplies a value where
        # this is not the case, this check will accomodate
        if self.x_justify == 'right':
            min_x = self.goal_line_anchor - self.feature_thickness
        elif self.x_justify == 'left':
            min_x = self.goal_line_anchor
        else:
            min_x = self.goal_line_anchor - (self.feature_thickness / 2.0)

        # If the minimum value of x is going to be less than the x coordinate
        # of the center of the corner's arc, then the feature should be a
        # rectangle
        if min_x <= corner_arc_center_x:
            goal_line_df = self.create_rectangle(
                x_min = -self.feature_thickness / 2.0,
                x_max = self.feature_thickness / 2.0,
                y_min = -half_width,
                y_max = half_width
            )

            return goal_line_df

        # Otherwise, more calculation is necessary
        else:
            # Start the calculation by getting the distance from the boards to
            # the anchored point of the goal line. Position this point relative
            # to the center of the circle
            anchor_to_arc_center = self.goal_line_anchor - corner_arc_center_x

            # Finally, go through the cases in the following way:
            if self.x_justify == 'right':
                # If the feature is right-justified, the starting x is the
                # provided x anchor less the given thickness of the goal line,
                # and the ending x is the half rink length less the provided x
                # anchor
                start_x = anchor_to_arc_center - self.feature_thickness
                end_x = anchor_to_arc_center

            elif self.x_justify == 'left':
                # If the feature is left-justified, the starting x is the
                # provided x anchor, and the ending x is the half rink length
                # less the provided x anchor plus the given thickness of the
                # goal line
                start_x = anchor_to_arc_center
                end_x = anchor_to_arc_center + self.feature_thickness

            else:
                # Otherwise, the feature is center-justified. This means that
                # half of the feature's thickness should be on either side of
                # the anchored x coordinate
                start_x = anchor_to_arc_center - (self.feature_thickness / 2.0)
                end_x = anchor_to_arc_center + (self.feature_thickness / 2.0)

            # Finally, compute the starting and ending angles by taking the
            # inverse sine of the starting and ending x positions, then
            # dividing by the corner's radius. Divide by pi to ensure that the
            # angles are correctly passed to the self.create_circle() method
            theta_start = math.asin(start_x / self.feature_radius) / np.pi
            theta_end = math.asin(end_x / self.feature_radius) / np.pi

            # Now create the feature's data frame
            goal_line_df = pd.concat([
                self.create_circle(
                    center = (corner_arc_center_x, corner_arc_center_y),
                    start = 0.5 - theta_start,
                    end = 0.5 - theta_end,
                    r = self.feature_radius
                ),

                self.create_circle(
                    center = (corner_arc_center_x, -corner_arc_center_y),
                    start = -0.5 + theta_end,
                    end = -0.5 + theta_start,
                    r = self.feature_radius
                )
            ])

            return goal_line_df


class CenterFaceoffCircle(BaseHockeyFeature):
    """Get the faceoff circle at center ice.

    This circle is usually blue in color and lies on top of the center line.
    """

    def _get_centered_feature(self):
        # The center circle has no external hash marks, so this circle just
        # needs to be a circle
        faceoff_circle_df = pd.concat([
            self.create_circle(
                center = (0, 0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    0,
                    0
                ],

                'y': [
                    -self.feature_radius,
                    -self.feature_radius - self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            )
        ])

        return faceoff_circle_df


class CenterFaceoffSpot(BaseHockeyFeature):
    """The spot where a faceoff is taken at center ice.

    This spot is usually blue in color.
    """

    def _get_centered_feature(self):
        # The faceoff spot at center ice is a solid-colored dot, usually blue
        # in color
        faceoff_spot_df = self.create_circle(
            center = (0, 0),
            start = 0.0,
            end = 2.0,
            r = self.feature_radius
        )

        return faceoff_spot_df


class NonCenterFaceoffSpot(BaseHockeyFeature):
    """The spot where a faceoff is taken.

    This spot is usually either blue (center) or red (non-center) in color.
    """

    def _get_centered_feature(self):
        # The non-centered faceoff spots are comprised of an outer and inner
        # ring
        faceoff_spot_df = pd.concat([
            self.create_circle(
                center = (0, 0),
                start = 0.5,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    0
                ],

                'y': [
                    -self.feature_radius + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    0,
                    0
                ],

                'y': [
                    self.feature_radius - self.feature_thickness,
                    self.feature_radius
                ]
            })
        ])

        faceoff_spot_df = pd.concat([
            faceoff_spot_df,
            self._reflect(faceoff_spot_df, over_x = False, over_y = True)
        ])

        return faceoff_spot_df


class FaceoffLines(BaseHockeyFeature):
    """The L-shaped lines around offensive and defensive zone faceoff spots.

    These only exist in the offensive and defensive zones. They are usually
    red in color.
    """

    def __init__(self, dist_from_spot_x = 2.0, dist_from_spot_y = (9.0 / 12.0),
                 feature_length = 4.0, feature_width = 3.0, over_x = False,
                 over_y = False, *args, **kwargs):
        # Initialize the attributes unique to these L-shaped markings
        self.dist_from_spot_x = dist_from_spot_x
        self.dist_from_spot_y = dist_from_spot_y
        self.feature_length = feature_length
        self.feature_width = feature_width
        self.over_x = over_x
        self.over_y = over_y
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # The L-shaped lines are traced via the following path
        faceoff_line_df = pd.DataFrame({
            'x': [
                -self.dist_from_spot_x,
                -self.dist_from_spot_x - self.feature_length,
                -self.dist_from_spot_x - self.feature_length,
                -self.dist_from_spot_x - self.feature_thickness,
                -self.dist_from_spot_x - self.feature_thickness,
                -self.dist_from_spot_x,
                -self.dist_from_spot_x
            ],

            'y': [
                self.dist_from_spot_y,
                self.dist_from_spot_y,
                self.dist_from_spot_y + self.feature_thickness,
                self.dist_from_spot_y + self.feature_thickness,
                self.dist_from_spot_y + self.feature_width,
                self.dist_from_spot_y + self.feature_width,
                self.dist_from_spot_y
            ]
        })

        # Now, reflect the path over the x and y axes
        faceoff_line_df = self._reflect(
            faceoff_line_df,
            over_x = self.over_x,
            over_y = self.over_y
        )

        return faceoff_line_df


class OzoneDzoneFaceoffCircle(BaseHockeyFeature):
    """Get the offensive and defensive zone faceoff circles.

    These are the faceoff circles that are not at center ice.

    These faceoff circles are in the offensive and defensive zones.

    Attributes
    ----------
    hashmark_width : float (default: 2.0)
        The amount (in the units of the rink) that the hash marks on the
        exterior of a non-center faceoff circle extends towards the boards or
        the line y = 0

    hashmark_ext_spacing : float (default: 71/12)
        The spacing, from outer edge to outer edge, of the hash marks on the
        non-center faceoff circle. On an NHL rink, they are 5' 11" (71" total)
        apart
    """

    def __init__(self, hashmark_width = 2.0,
                 hashmark_ext_spacing = (71.0 / 12.0), *args, **kwargs):
        """Get the offensive and defensive zone faceoff circles.

        Initialize new features unique to faceoff circles, specifically the
        length of the hashmarks on the perimeter of the circle.

        This is only for non-center faceoff circles.
        """
        # Initialize the features specific to the non-center faceoff circle
        self.hashmark_width = hashmark_width
        self.hashmark_ext_spacing = hashmark_ext_spacing

        # Initialize the main component of the feature
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # To create a faceoff circle, start by finding the angle needed to draw
        # the outer ring of the faceoff circle. This can be computed using some
        # simple trigonometry. The NHL is used to illustrate the trigonometry,
        # however the code is abstracted to allow for variable parameters

        # NHL hash marks are 5' 11" (71") apart on the exterior, with one hash
        # mark on each side of the line that vertically bisects the circle
        # through its center. This means that 35.5" of this distance lies on
        # either side of this line, and thus the arcsine of this over the
        # radius of the circle will give the correct starting angle (after
        # adding pi/2)
        ext_spacing = self.hashmark_ext_spacing / 2.0
        int_spacing = ext_spacing - self.feature_thickness

        theta1 = math.asin(ext_spacing / self.feature_radius) / np.pi
        theta2 = math.asin(int_spacing / self.feature_radius) / np.pi

        faceoff_circle_df = pd.concat([
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
                end = 0.5 + theta2,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    -int_spacing,
                    -ext_spacing
                ],

                'y': [
                    self.feature_radius + self.hashmark_width,
                    self.feature_radius + self.hashmark_width
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 0.5 + theta1,
                end = 1.5 - theta1,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    -ext_spacing,
                    -int_spacing
                ],

                'y': [
                    -self.feature_radius - self.hashmark_width,
                    -self.feature_radius - self.hashmark_width,
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 1.5 - theta2,
                end = 1.5,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [0],
                'y': [-self.feature_radius + self.feature_thickness]
            }),

            self.create_circle(
                center = (0, 0),
                start = 1.5,
                end = 0.5,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [0],
                'y': [self.feature_radius]
            })
        ])

        # Reflect the half-circle just created over the y axis
        faceoff_circle_df = pd.concat([
            faceoff_circle_df,
            self._reflect(faceoff_circle_df, over_x = False, over_y = True)
        ])

        return faceoff_circle_df


class NonCenterFaceoffSpotStripe(BaseHockeyFeature):
    """The stripe in the offensive and defensive zone faceoff spots.

    These are the faceoff spots that are not at center ice.

    These faceoff circles are in the offensive and defensive zones.
    """

    def __init__(self, gap_width = (3.0 / 12.0), *args, **kwargs):
        """Get the non-center faceoff spots.

        Initialize new features unique to faceoff circles, specifically the
        size of the gap between the inner stripe and the outer ring.

        This is only for non-center faceoff circles.
        """
        # Initialize the features specific to the non-center faceoff spots
        self.gap_width = gap_width

        # Initialize the main component of the feature
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # The non-center face-off spots are wider in diameter, with a gap
        # between the top and bottom of the spot and the strip in the center.
        # First, find the angle at which to start the trace for the interior
        # of the spot. The following walkthrough uses NHL dimensions for the
        # explanation, but the process is equally applied through all leagues

        # The spot has a radius of 1', and a thickness of 2", so the inner
        # radius is 10". Since there is a 3" gap at theta = 180°, this
        # indicates that the stripe's curve starts at x = -7" from the center.
        # Using trigonometry, the angle can be computed

        # Start by getting the inner radius of the ring
        ring_inner_radius = self.feature_radius - self.feature_thickness

        # Then get the thickness of half of the stripe that runs through the
        # center of the spot
        stripe_thickness = ring_inner_radius - self.gap_width

        # Calculate the angle
        theta = math.asin(stripe_thickness / ring_inner_radius) / np.pi

        spot_stripe_df = pd.concat([
            self.create_circle(
                center = (0, 0),
                start = 0.5 - theta,
                end = 0.5 + theta,
                r = ring_inner_radius
            ),

            self.create_circle(
                center = (0, 0),
                start = 1.5 - theta,
                end = 1.5 + theta,
                r = ring_inner_radius
            )
        ])

        return spot_stripe_df


class RefereeCrease(BaseHockeyFeature):
    """The referee's crease.

    This is located on the bottom of the ice surface in TV view, and is usually
    red in color.
    """

    def _get_centered_feature(self):
        # The referee's crease is a semi-circle. In TV view, it is at the
        # bottom of the ice,
        referee_crease_df = pd.concat([
            pd.DataFrame({
                'x': [
                    self.feature_radius,
                ],

                'y': [
                    0
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 0.0,
                end = 1.0,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    -self.feature_radius,
                    -self.feature_radius + self.feature_thickness
                ],

                'y': [
                    0,
                    0
                ]
            }),

            self.create_circle(
                center = (0, 0),
                start = 1.0,
                end = 0.0,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    self.feature_radius,
                ],

                'y': [
                    0
                ]
            })
        ])

        return referee_crease_df


class GoalCreaseOutline(BaseHockeyFeature):
    """The area in front of the goal line where the goalie is positioned.

    The outline of this area is usually red, with the inner area being a light
    blue.
    """

    def __init__(self, goal_line_x = 89.0, goal_crease_width = 4.0,
                 goal_crease_length = 4.0, crease_notch_dist = 4.0,
                 crease_notch_width = (5.0 / 12.0), *args, **kwargs):
        # Set the goal line's anchor property
        self.goal_line_x = goal_line_x
        self.goal_crease_length = goal_crease_length
        self.goal_crease_width = goal_crease_width
        self.crease_notch_dist = crease_notch_dist
        self.crease_notch_width = crease_notch_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # First, determine where to start x based on the x_justify parameter.
        # The following are all with reference to the TV-left goal line and
        # goal crease
        if self.x_justify == 'left':
            # If the goal crease is left-justified, then the left-most edge of
            # the crease should be flush with the left-most edge of the goal
            # line.
            start_x = 0

        elif self.x_justify == 'right':
            # If the goal crease is right-justified, then the left-most edge of
            # the crease should be flush with x = self.feature_thickness
            start_x = self.feature_thickness

        else:
            # Otherwise, the goal crease is center-justified. It should begin
            # half of its line's thickness from the goal line
            start_x = self.feature_thickness / 2.0

        # Next, calculate the starting angle of the goal crease's rounded front
        # by taking the inverse sine of its half-width and dividing it by the
        # radius of the arc
        theta = math.asin(self.goal_crease_width / self.feature_radius)
        theta /= np.pi

        goal_crease_outline_df = pd.concat([
            pd.DataFrame({
                'x': [
                    start_x,
                    start_x + self.goal_crease_length
                ],

                'y': [
                    self.goal_crease_width,
                    self.goal_crease_width
                ]
            }),

            self.create_circle(
                center = (start_x, 0),
                start = theta,
                end = -theta,
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    start_x + self.goal_crease_length,
                    start_x,
                    start_x,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist + self.feature_thickness
                ],

                'y': [
                    -self.goal_crease_width,
                    -self.goal_crease_width,
                    -self.goal_crease_width + self.feature_thickness,
                    -self.goal_crease_width + self.feature_thickness,
                    -self.goal_crease_width + self.feature_thickness +
                    self.crease_notch_width,
                    -self.goal_crease_width + self.feature_thickness +
                    self.crease_notch_width,
                    -self.goal_crease_width + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (start_x, 0),
                start = -theta,
                end = theta,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist,
                    start_x,
                    start_x
                ],

                'y': [
                    self.goal_crease_width - self.feature_thickness,
                    self.goal_crease_width - self.feature_thickness -
                    self.crease_notch_width,
                    self.goal_crease_width - self.feature_thickness -
                    self.crease_notch_width,
                    self.goal_crease_width - self.feature_thickness,
                    self.goal_crease_width - self.feature_thickness,
                    self.goal_crease_width
                ]
            }),
        ])

        goal_crease_outline_df['x'] = goal_crease_outline_df['x'] +\
            self.goal_line_x

        return goal_crease_outline_df


class GoalCreaseFill(BaseHockeyFeature):
    """The area in front of the goal line where the goalie is positioned.

    The outline of this area is usually red, with the inner area being a light
    blue.
    """

    def __init__(self, goal_line_x = 89.0, goal_crease_width = 4.0,
                 goal_crease_length = 4.0, crease_notch_dist = 4.0,
                 crease_notch_width = (5.0 / 12.0), *args, **kwargs):
        # Set the goal line's anchor property
        self.goal_line_x = goal_line_x
        self.goal_crease_length = goal_crease_length
        self.goal_crease_width = goal_crease_width
        self.crease_notch_dist = crease_notch_dist
        self.crease_notch_width = crease_notch_width
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # First, determine where to start x based on the x_justify parameter.
        # The following are all with reference to the TV-left goal line and
        # goal crease
        if self.x_justify == 'left':
            # If the goal crease is left-justified, then the left-most edge of
            # the crease should be flush with the left-most edge of the goal
            # line.
            start_x = 0

        elif self.x_justify == 'right':
            # If the goal crease is right-justified, then the left-most edge of
            # the crease should be flush with x = self.feature_thickness
            start_x = self.feature_thickness

        else:
            # Otherwise, the goal crease is center-justified. It should begin
            # half of its line's thickness from the goal line
            start_x = self.feature_thickness / 2.0

        # Next, calculate the starting angle of the goal crease's rounded front
        # by taking the inverse sine of its width and dividing it by the radius
        # of the arc
        theta = math.asin(self.goal_crease_width / self.feature_radius)
        theta /= np.pi

        goal_crease_fill_df = pd.concat([
            pd.DataFrame({
                'x': [
                    start_x,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist + self.feature_thickness
                ],

                'y': [
                    -self.goal_crease_width + self.feature_thickness,
                    -self.goal_crease_width + self.feature_thickness,
                    -self.goal_crease_width + self.feature_thickness +
                    self.crease_notch_width,
                    -self.goal_crease_width + self.feature_thickness +
                    self.crease_notch_width,
                    -self.goal_crease_width + self.feature_thickness
                ]
            }),

            self.create_circle(
                center = (start_x, 0),
                start = -theta,
                end = theta,
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist + self.feature_thickness,
                    start_x + self.crease_notch_dist,
                    start_x + self.crease_notch_dist,
                    start_x
                ],

                'y': [
                    self.goal_crease_width - self.feature_thickness,
                    self.goal_crease_width - self.feature_thickness -
                    self.crease_notch_width,
                    self.goal_crease_width - self.feature_thickness -
                    self.crease_notch_width,
                    self.goal_crease_width - self.feature_thickness,
                    self.goal_crease_width - self.feature_thickness,
                ]
            }),
        ])

        goal_crease_fill_df['x'] = goal_crease_fill_df['x'] + self.goal_line_x

        return goal_crease_fill_df


class GoalFrame(BaseHockeyFeature):
    """The frame of the goal.

    This is usually red in color.
    """

    def __init__(self, goal_mouth_interior_width = 6.0, goal_line_x = -11.0,
                 goal_depth = 40.0 / 12.0, goal_post_diameter = 2.375 / 12.0,
                 feature_unit = 'ft', *args, **kwargs):
        # Initialize the attributes specific to the goal post
        self.goal_mouth_interior_width = goal_mouth_interior_width
        self.goal_line_x = goal_line_x
        self.goal_depth = goal_depth
        self.goal_post_diameter = goal_post_diameter

        if feature_unit == 'ft':
            self.goal_corner_center_movement = 1.0

        elif feature_unit == 'm':
            self.goal_corner_center_movement = 0.3048

        else:
            pass

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        half_goal_mouth = self.goal_mouth_interior_width / 2.0
        # First, determine where to start x based on the x_justify parameter.
        # The following are all with reference to the TV-left goal line and
        # goal frame
        if self.x_justify == 'left':
            # If the goal frame is left-justified, then the left-most edge of
            # the post should be flush with the left-most edge of the goal
            # line.
            start_x = self.goal_line_x

        elif self.x_justify == 'right':
            # If the goal crease is right-justified, then the left-most edge of
            # the goal frame should be flush with x = self.feature_thickness
            start_x = self.goal_line_x - self.feature_thickness

        else:
            # Otherwise, the goal crease is center-justified. It should begin
            # half of its line's thickness from the goal line
            start_x = self.goal_line_x - (self.feature_thickness / 2.0)

        goal_frame_df = pd.concat([
            pd.DataFrame({
                'x': [
                    start_x
                ],

                'y': [
                    half_goal_mouth + self.goal_post_diameter
                ]
            }),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    half_goal_mouth - self.goal_corner_center_movement
                ),
                start = (1.0 / 3.0) + (1.0 / 16.0),
                end = 1.0,
                r = self.feature_radius
            ),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    -half_goal_mouth + self.goal_corner_center_movement
                ),
                start = -1.0,
                end = -(1.0 / 3.0) - (1.0 / 16.0),
                r = self.feature_radius
            ),

            pd.DataFrame({
                'x': [
                    start_x,
                    start_x
                ],

                'y': [
                    -half_goal_mouth - self.goal_post_diameter,
                    -half_goal_mouth
                ]
            }),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    -half_goal_mouth + self.goal_corner_center_movement
                ),
                start = -(1.0 / 3.0) - (1.0 / 16.0),
                end = -1.0,
                r = self.feature_radius - self.feature_thickness
            ),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    half_goal_mouth - self.goal_corner_center_movement
                ),
                start = 1.0,
                end = (1.0 / 3.0) + (1.0 / 16.0),
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    start_x,
                    start_x
                ],

                'y': [
                    half_goal_mouth,
                    half_goal_mouth + self.goal_post_diameter
                ]
            })
        ])

        return goal_frame_df


class GoalFill(BaseHockeyFeature):
    """The fill of the goal.

    This is usually grey in color.
    """

    def __init__(self, goal_mouth_interior_width = 6.0, goal_line_x = -11.0,
                 goal_depth = 40.0 / 12.0, goal_post_diameter = 2.375 / 12.0,
                 feature_unit = 'ft', *args, **kwargs):
        # Initialize the attributes specific to the goal post
        self.goal_mouth_interior_width = goal_mouth_interior_width
        self.goal_line_x = goal_line_x
        self.goal_depth = goal_depth
        self.goal_post_diameter = goal_post_diameter

        if feature_unit == 'ft':
            self.goal_corner_center_movement = 1.0

        elif feature_unit == 'm':
            self.goal_corner_center_movement = 0.3048

        else:
            pass

        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        half_goal_mouth = self.goal_mouth_interior_width / 2.0
        # First, determine where to start x based on the x_justify parameter.
        # The following are all with reference to the TV-left goal line and
        # goal frame
        if self.x_justify == 'left':
            # If the goal frame is left-justified, then the left-most edge of
            # the post should be flush with the left-most edge of the goal
            # line.
            start_x = self.goal_line_x

        elif self.x_justify == 'right':
            # If the goal crease is right-justified, then the left-most edge of
            # the goal frame should be flush with x = self.feature_thickness
            start_x = self.goal_line_x - self.feature_thickness

        else:
            # Otherwise, the goal crease is center-justified. It should begin
            # half of its line's thickness from the goal line
            start_x = self.goal_line_x - (self.feature_thickness / 2.0)

        goal_fill_df = pd.concat([
            pd.DataFrame({
                'x': [
                    start_x
                ],

                'y': [
                    -half_goal_mouth
                ]
            }),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    -half_goal_mouth + self.goal_corner_center_movement
                ),
                start = -(1.0 / 3.0) - (1.0 / 16.0),
                end = -1.0,
                r = self.feature_radius - self.feature_thickness
            ),

            self.create_circle(
                center = (
                    self.goal_line_x - self.feature_radius,
                    half_goal_mouth - self.goal_corner_center_movement
                ),
                start = 1.0,
                end = (1.0 / 3.0) + (1.0 / 16.0),
                r = self.feature_radius - self.feature_thickness
            ),

            pd.DataFrame({
                'x': [
                    start_x,
                    start_x
                ],

                'y': [
                    half_goal_mouth,
                    -half_goal_mouth
                ]
            })
        ])

        return goal_fill_df


class GoalkeepersRestrictedArea(BaseHockeyFeature):
    """The restricted area behind the goal. This only appears on NHL rinks.

    This is usually red in color.
    """

    def __init__(self, long_base_width = 28.0, short_base_width = 22.0,
                 goal_line_x = -11.0, *args, **kwargs):
        # Initialize the attributes unique to the goalkeeper's restricted area
        self.long_base_width = long_base_width
        self.short_base_width = short_base_width
        self.goal_line_x = goal_line_x
        super().__init__(*args, **kwargs)

    def _get_centered_feature(self):
        # First, determine where to start x based on the x_justify parameter.
        # The following are all with reference to the TV-left goal line and
        # goal frame
        if self.x_justify == 'left':
            left_edge_x = self.goal_line_x
            right_edge_x = self.goal_line_x + self.feature_thickness

        elif self.x_justify == 'right':
            left_edge_x = self.goal_line_x - self.feature_thickness
            right_edge_x = self.goal_line_x

        else:
            # Otherwise, the goal crease is center-justified. It should begin
            # half of its line's thickness from the goal line
            left_edge_x = self.goal_line_x - (self.feature_thickness / 2.0)
            right_edge_x = self.goal_line_x + (self.feature_thickness / 2.0)

        goalkeepers_restricted_area_df = pd.DataFrame({
            'x': [
                -self.rink_length / 2.0,
                right_edge_x,
                right_edge_x,
                -self.rink_length / 2.0,
                -self.rink_length / 2.0,
                left_edge_x,
                left_edge_x,
                -self.rink_length / 2.0,
                -self.rink_length / 2.0
            ],

            'y': [
                self.long_base_width / 2.0,
                self.short_base_width / 2.0,
                -self.short_base_width / 2.0,
                -self.long_base_width / 2.0,
                (-self.long_base_width / 2.0) + self.feature_thickness,
                (-self.short_base_width / 2.0) + self.feature_thickness,
                (self.short_base_width / 2.0) - self.feature_thickness,
                (self.long_base_width / 2.0) - self.feature_thickness,
                self.long_base_width / 2.0
            ]
        })

        return goalkeepers_restricted_area_df
