"""
Tests for the shape-generating functions

@author: Ross Drucker
"""
import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal
from sportypy.helpers.coordinate_ops import create_shapes as create

def test_square():
    """
    Test that the create.square() function creates a square
    """
    unit_square = pd.DataFrame({
        'x': [
            -0.5,
             0.5,
             0.5,
            -0.5,
            -0.5
        ],
        
        'y': [
            -0.5,
            -0.5,
             0.5,
             0.5,
            -0.5
        ]
    })
    
    test_square = create.square(side_length = 1)
    
    assert_frame_equal(unit_square, test_square)
    
def test_circle():
    """
    Test that the create.circle() function creates a circle. Since points on
    a circle are all the same distance from the center, there should only be
    one unique distance. This distance is computed as sqrt(x^2 + y^2). Values
    within 99.9% of 1 will be considered to be equal
    """
    unit_circle = create.circle()
    unit_circle['distance'] = np.sqrt(
        np.square(unit_circle['x']) + np.square(unit_circle['y'])
    )
    
    unit_circle.loc[unit_circle['distance'] > .999, 'distance'] = 1
    
    assert len(unit_circle['distance'].unique()) == 1
    
def test_rectangle():
    """
    Test that the create.rectangle() function creates a rectangle. Since all
    squares are rectangles, a unit rectangle centered around (0, 0) should be
    the same as a unit square
    """
    unit_rectangle = create.rectangle(
        x_min = -0.5,
        x_max =  0.5,
        y_min = -0.5,
        y_max =  0.5
    )
    
    unit_square = create.square(side_length = 1)
    
    assert_frame_equal(unit_rectangle, unit_square)
    
def test_diamond():
    """
    Test that the create.diamond() creates a diamond
    """
    unit_diamond = pd.DataFrame({
        'x': [
            -0.5,
               0,
             0.5,
               0,
            -0.5
        ],
        
        'y': [
               0,
            -0.5,
               0,
             0.5,
               0
        ]
    })
    
    test_diamond = create.diamond(height = 1, width = 1)
    
    assert_frame_equal(unit_diamond, test_diamond)