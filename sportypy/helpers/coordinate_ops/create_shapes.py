"""
Functions to generate data frames of points that form geometric shapes

@author: Ross Drucker
"""
import numpy as np
import pandas as pd

def circle(center = (0, 0), npoints = 1000, d = 2, start = 0, end = 2):
    """
    Create a set of x and y coordinates that form a circle (or the arc of a
    circle)
    
    Parameters
    ----------
    center: The (x, y) coordinates of the center of the circle. Default: (0, 0)
    npoints: The number of points with which to create the circle. This will
        also be the length of the resulting data frame. Default: 500
    d: Diameter of the circle IN THE UNITS OF THE PLOT. This default unit will
        be feet. Default: 2 (unit circle)
    start: The angle (in radians) at which to start drawing the circle, where
        zero runs along the +x axis. Default: 0
    end: The angle (in radians) at which to stop drawing the circle, where zero
        runs along the +x axis. Default: 0

    Returns
    -------
    circle_df: A pandas dataframe that contains the circle's coordinate points
    """
    # Create a vector of numbers that are evenly spaced apart between the
    # starting and ending angles. They should be multiplied by pi to be in
    # radians. This vector represents the angle through which the circle is
    # traced
    pts = np.linspace(start * np.pi, end * np.pi, npoints)
    
    # Create the vectors x and y that represent the circle (or arc of a circle)
    # to be created. This is a translation away from the center across (d/2),
    # then rotated by cos(angle) and sin(angle) for x and y respectively. 
    x = center[0] + ((d / 2) * np.cos(pts))
    y = center[1] + ((d / 2) * np.sin(pts))
    
    # Combine points into data frame for output
    circle_df = pd.DataFrame({
        'x': x,
        'y': y
    })
    
    return circle_df

def rectangle(x_min, x_max, y_min, y_max):
    """
    Generate a bounding box for a rectangle

    Parameters
    ----------
    x_min: the lower of the two x coordinates
    x_max: the higher of the two x coordinates
    y_min: the lower of the two y coordinates
    y_max: the higher of the two y coordinates

    Returns
    -------
    rect_pts: A pandas dataframe that contains the rectangle's bounding box
        coordinates
    """
    # A rectangle's bounding box is described by going along the following path
    rect_pts = pd.DataFrame({
        'x': [
            x_min,
            x_max,
            x_max,
            x_min,
            x_min
        ],
        
        'y': [
            y_min,
            y_min,
            y_max,
            y_max,
            y_min
        ]  
    })
    
    return rect_pts

def square(side_length, center = (0, 0)):
    """
    Generate a bound box for a square
    
    Parameters
    ----------
    side_length: an integer length of the side of the square
    center: where to center the square
    
    Returns
    -------
    square_pts: A pandas dataframe that contains the square's bounding box
        coordinates
    """
    # A square's bounding box is described by going along the following path
    square_pts = pd.DataFrame({
        'x': [
            center[0] - side_length/2,
            center[0] + side_length/2,
            center[0] + side_length/2,
            center[0] - side_length/2,
            center[0] - side_length/2
        ],
        
        'y': [
            center[1] - side_length/2,
            center[1] - side_length/2,
            center[1] + side_length/2,
            center[1] + side_length/2,
            center[1] - side_length/2,
        ]
    })
    
    return square_pts

def diamond(height, width, center = (0, 0)):
    """
    Generate a bound box for a diamond
    
    Parameters
    ----------
    height: the vertical height of the diamond
    width: the horizontal width of the diamond
    center: where to center the diamond
    
    Returns
    -------
    diamond_pts: A pandas dataframe that contains the diamond's bounding box
        coordinates
    """
    # A square's bounding box is described by going along the following path
    diamond_pts = pd.DataFrame({
        'x': [
            center[0] - side_length/2,
            center[0] + side_length/2,
            center[0] + side_length/2,
            center[0] - side_length/2,
            center[0] - side_length/2
        ],
        
        'y': [
            center[0] - side_length/2,
            center[0] - side_length/2,
            center[0] + side_length/2,
            center[0] + side_length/2,
            center[0] - side_length/2,
        ]
    })
    
    return square_pts