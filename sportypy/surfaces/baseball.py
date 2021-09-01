"""Extension of the BaseSurfacePlot class to create a baseball field.

This is a second-level child class of the BaseSurface class, and as such will
have access to its attributes and methods. The default field will be that of
the MLB, and main leagues will have their own subclass, but a user can manually
specify their own field parameters to create a totally-customized field. The
field's features are parameterized by the basic dimensions of the field, which
comprise the attributes of the class.

@author: Ross Drucker
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import sportypy.features.baseball_features as baseball
from sportypy._base_classes._base_surface_plot import BaseSurfacePlot


class BaseballField(BaseSurfacePlot):
    """A generic baseball field subclass of BaseSurfacePlot.

    This allows for the creation of the baseball field in a way that is
    entirely parameterized by the field's baseline characteristics. The default
    will be the dimensions of an MLB field. See the class definition for full
    details.

    Attributes
    ----------
    rotation : float (default: 0.0)
        The angle (in degrees) through which to rotate the final plot

    x_trans : float (default: 0.0)
        The amount that the x coordinates are to be shifted. By convention,
        the +x axis extends from the back tip of home plate out towards center
        field

    y_trans : float (default: 0.0)
        The amount that the y coordinates are to be shifted. By convention,
        the +y axis extends from the back tip of home plate out towards center
        field

    home_plate_side_length : float (default: 17.0 / 12.0; 17")
        The length of the front edge of home plate. This should be provided in
        the same units as the field

    base_side_length : float (default: 15.0 / 12.0; 15")
        The length of a side of a square base. This should be provided in the
        same units as the field

    home_to_2b_dist : float (default: 127.28125; 127' 3 3/8")
        The distance between the back tip of home plate and the center of the
        second base bag. This point is used to anchor the second base bag, as
        well as determine the anchor points of the corners of the first and
        third base bags
    """

    def __init__(self, rotation = 0.0, x_trans = 0.0, y_trans = 0.0,
                 home_plate_side_length = 17.0 / 12.0,
                 base_side_length = 15.0 / 12.0,
                 home_to_2b_dist = 127.0 + (3.0 / 12.0) + ((3.0 / 8.0) / 12.0),
                 baseline_length = 90.0,
                 home_plate = {}, first_base = {}, second_base = {},
                 third_base = {}, colors_dict = {},
                 **added_features):
        # Set the rotation of the plot to be the supplied rotation
        # value
        self._rotation = Affine2D().rotate_deg(rotation)

        # Set the court's necessary shifts. This will overwrite the
        # default values of x_trans and y_trans inherited from the
        # BaseSurfacePlot (which is in turn inherited from BaseSurface)
        self.x_trans = x_trans
        self.y_trans = y_trans

        # Initialize the values that are specific to features on the field
        self.home_plate_side_length = home_plate_side_length
        self.base_side_length = base_side_length
        self.home_to_2b_dist = home_to_2b_dist
        self.baseline_length = baseline_length

        # Initialize the standard colors of the court
        standard_colors = {
            'field_background': '#9b7653',
            'home_plate': '#ffffff',
            'first_base': '#ffffff',
            'second_base': '#ffffff',
            'third_base': '#ffffff',
        }

        # Combine the colors with a passed colors dictionary
        if not colors_dict:
            colors_dict = {}
        
        # Create the final color set for the features
        self.feature_colors = {**standard_colors, **colors_dict}

        # Initialize the constraint of the field although no constraint is
        # required for this surface
        field_constraint = {
            'class': baseball.FieldConstraint,
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
        self._initialize_feature(field_constraint)
        self._surface_constraint = self._features.pop(-1)

        # Initialize home plate
        home_plate_params = {
            'class': baseball.HomePlate,
            'x_anchor': 0.0,
            'y_anchor': 0.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'home_plate_side_length': home_plate_side_length,
            'facecolor': self.feature_colors['home_plate'],
            'edgecolor': self.feature_colors['home_plate'],
            'visible': True,
            'zorder': 10
        }
        home_plate_params = {**home_plate_params, **home_plate}
        self._initialize_feature(home_plate_params)

        # Initialize first base
        first_base_params = {
            'class': baseball.Base,
            'x_anchor': self.baseline_length * np.cos(np.pi / 4.0),
            'y_anchor': self.home_to_2b_dist / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'base_side_length': self.base_side_length,
            'facecolor': self.feature_colors['first_base'],
            'edgecolor': self.feature_colors['first_base'],
            'visible': True,
            'zorder': 10
        }
        first_base_params = {**first_base_params, **first_base}
        self._initialize_feature(first_base_params)

        # Initialize second base
        second_base_params = {
            'class': baseball.Base,
            'x_anchor': 0.0,
            'y_anchor': self.home_to_2b_dist,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'base_side_length': self.base_side_length,
            'facecolor': self.feature_colors['second_base'],
            'edgecolor': self.feature_colors['second_base'],
            'visible': True,
            'zorder': 10
        }
        second_base_params = {**second_base_params, **second_base}
        self._initialize_feature(second_base_params)

        third_base_params = {
            'class': baseball.Base,
            'x_anchor': self.baseline_length * np.cos(3.0 * np.pi / 4.0),
            'y_anchor': self.home_to_2b_dist / 2.0,
            'x_justify': 'center',
            'y_justify': 'center',
            'reflect_x': False,
            'reflect_y': False,
            'base_side_length': self.base_side_length,
            'facecolor': self.feature_colors['third_base'],
            'edgecolor': self.feature_colors['third_base'],
            'visible': True,
            'zorder': 10
        }
        third_base_params = {**third_base_params, **third_base}
        self._initialize_feature(third_base_params)

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
            +x end of the boards. If a tuple, the two values will be
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
            fig.patch.set_facecolor(self.feature_colors['field_background'])
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
            # bounds of the court
            if visible and not isinstance(feature, baseball.FieldConstraint):
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
        # the boards)
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
                'full': (-250, 250),

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
                # the boards, display the entire court
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

if __name__ == '__main__':
    BaseballField().draw()