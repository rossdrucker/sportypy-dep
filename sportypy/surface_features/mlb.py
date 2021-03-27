"""
Functions needed to draw a regulation MLB field. The origin of the coordinate
system, (0, 0), will be the back tip of home base, with the +y axis extending
out to the pitcher's base and the x axis parallel to the lines between first
and third base (with first base being in the +x direction)

@author: Ross Drucker
"""
import math
import pandas as pd


def home_base():
    """
    Generate the coordinates needed to draw home base as described in Rule
    2.02 of the MLB rule book. The tip of home base will be (0, 0) in the
    coordinate system
    
    Parameters
    ----------
    None
    
    Returns
    -------
    home_base: a pandas dataframe containing the points necessary to draw home
        base
    """
    # Home base is a 17" square, with two corners removed such that one edge is
    # 17", the two adjacent sides are 8.5", and the remaining sides are 12"
    # angled to make a point. Since the tip of home plate is at (0, 0), and 
    # home base is a 17" square, the nearest vertices to the tip of home base
    # are +/-8.5" along the x axis, and 8.5" in front of the tip of home base
    home_base = pd.DataFrame({
        'x': [
            0,
            -8.5/12,
            -8.5/12,
            8.5/12,
            8.5/12,
            0
        ],
        
        'y': [
            0,
            8.5/12,
            17/12,
            17/12,
            8.5/12,
            0
        ]
    })
    
    return home_base