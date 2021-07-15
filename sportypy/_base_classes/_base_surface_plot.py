"""
@author: Ross Drucker
"""
import numpy as np
from functools import wraps
import matplotlib.pyplot as plt
from sportypy._base_classes._base_surface import BaseSurface

class BaseSurfacePlot(BaseSurface):
    """Class that extends a basic surface to include the necessary methods for
    plotting its features, user-supplied data, heatmaps, hexbin plots, etc.
    """
    def _validate_values(plot_function):
        """Ensure that values passed to the plotting function are within the
        boundaries of the final plot.

        A point is considered "valid" if the point lies within the boundaries of
        the surface or constraint. Those points that do not are not plotted and
        are instead converted to be np.nan

        This is a decorator which will be used with plotting methods of this
        class.

        This expects that x and y have already been converted to the right units
        and shifted appropriately to be plotted
        """
        @wraps(plot_function)
        def wrapper(self, x, y, *, values = None, plot_range = None,
                    plot_xlim = None, plot_ylim = None, **kwargs):
            # Get the values to use for a hexbin plot. This controls how the
            # hexagons are defined in a hexbin
            C = kwargs.pop('C', None)

            # If no values are supplied, use the binning parameter C described
            # above
            if not values:
                values = C
            
            # Make a copy of the values so as not to overwrite the original
            # values
            values = self.copy_(values)

            # If there are no values, make a series of 1s to serve as
            # placeholders that is the same shape as the x and y values
            if not values:
                values = np.ones(x.shape)
            
            # Otherwise, use the actual values and flatten them (if necessary)
            # to a one-dimensional array
            else:
                values = np.ravel(values)

                # Force the x and y values to be symmetric
                if kwargs.get('symmetrize', False):
                    values = np.concatenate((values, values))

            # If x, y, and values are not symmetric in length, raise an error
            if len(x) != len(y) or len(x) != len(values):
                raise Exception('x, y, and values must all be of same length')
            
            if plot_range is None and plot_xlim is None and plot_ylim is None:
                plot_xlim, plot_ylim = self._get_limits('full')

            # Initialize the mask to be be false. The mask will indicate whether
            # a point lies within the defined limits for the plot
            mask = False
            
            # If no plot_range is specified, and no x or y limitations are
            # imposed, set the plot limits to that of a full-surface plot
            if plot_range is None and plot_xlim is None and plot_ylim is None:
                plot_xlim, plot_ylim = self._get_limits('full')
            
            # Otherwise, get the limits of the plot based on the supplied values
            # and set the mask to identify points who are outside of its bounds
            else:
                plot_xlim, plot_ylim = self.get_limits(
                    plot_range,
                    self.copy_(plot_xlim),
                    self.copy_(plot_ylim)
                )

                # The mask finds points that are below the minimum allowable x
                # and y values or above the maximum allowable x and y values
                mask = (
                    (x < plot_xlim[0]) | (x > plot_xlim[1])
                    | (y < plot_ylim[0]) | (y > plot_ylim[1])
                )

            # If the plot is constrained to exclude values outside its bounds,
            # then values outside of the boundaries of the surface should be set
            # to be nan
            if kwargs.get('is_constrained', True):
                values = self._outside_boundaries_to_nan(x, y, values)
            
            # Create the final mask to exclude points that are outside the
            # boundary of the surface or are non-existent (nan)
            mask = mask | np.isnan(x) | np.isnan(y) | np.isnan(values)

            # Apply the mask to both the x and y coordinates as well as the
            # values
            x = x[~mask]
            y = y[~mask]
            values = values[~mask]

            return plot_function(
                self,
                x,
                y,
                values = values,
                plot_range = plot_range,
                plot_xlim = plot_xlim,
                plot_ylim = plot_ylim,
                **kwargs
            )
        
        return wrapper

    def _validate_plot(plot_function):
        """Ensure that all parameters necessary to draw the plot are in the
        correct form.

        This is a decorator which will be used with plotting methods of this
        class.
        """
        @wraps(plot_function)
        def wrapper(self, *args, **kwargs):
            # If no Axes object is passed as a keyword argument, create one to
            # use for the plot
            if 'ax' not in kwargs:
                kwargs['ax'] = plt.gca()

            # Convert the non-keyword arguments to a list
            args = list(args)

            # Check if any of the following are passed as keyword arguments to
            # the plot function
            for coord in ('x', 'y', 'x1', 'y1', 'x2', 'y2'):
                # If they are, then append it to the list of arguments
                if coord in kwargs:
                    args.append(kwargs.pop(coord))

            for i in range(len(args)):
                args[i] = self.copy_(args[i])
                args[i] = np.ravel(args[i])

                is_y = i % 2

                if kwargs.get('symmetrize', False):
                    args[i] = np.concatenate((
                        args[i],
                        args[i] * (-1 if is_y else 1)
                    ))

                args[i] = args[i] - (self.y_shift if is_y else self.x_shift)

            kwargs['transform'] = self._get_transform(kwargs['ax'])

            args = tuple(args)

            return plot_function(self, *args, **kwargs)

        return wrapper

    def _constrain_plot(self, plot_features, ax, transform):
        """Constrain the features"""
        pass