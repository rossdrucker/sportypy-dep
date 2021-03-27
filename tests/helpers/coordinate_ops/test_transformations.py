"""
Tests for coordinate-transforming functions

@author: Ross Drucker
"""
import numpy as np
import pandas as pd
from pandas._testing import assert_frame_equal
from sportypy.helpers.coordinate_ops import create_shapes as create
from sportypy.helpers.coordinate_ops import transformations as transform

def test_reflect():
    """
    Test that transform.reflect() accurately reflects a dataframe's points 
    over the correct axes using a unit square centered at 1, 1
    """
    test_dataframe = create.square(side_length = 1, center = (1, 1))
    
    expected_y_only = pd.DataFrame({
        'x': -1 * test_dataframe['x'],
        'y':      test_dataframe['y']
    })
    
    expected_x_only = pd.DataFrame({
        'x':      test_dataframe['x'],
        'y': -1 * test_dataframe['y']
    })
    
    expected_x_and_y = pd.DataFrame({
        'x': -1 * test_dataframe['x'],
        'y': -1 * test_dataframe['y']
    })
    
    test_x_only = transform.reflect(
        test_dataframe,
        over_x = True,
        over_y = False
    )
    
    test_y_only = transform.reflect(
        test_dataframe,
        over_x = False,
        over_y = True
    )
    
    test_x_and_y = transform.reflect(
        test_dataframe,
        over_x = True,
        over_y = True
    )
    
    assert_frame_equal(expected_x_only, test_x_only)
    assert_frame_equal(expected_y_only, test_y_only)
    assert_frame_equal(expected_x_and_y, test_x_and_y)
    
def test_rotate():
    """
    Test that transform.rotate() accurately rotates a dataframe's points about
    the origin
    """
    sample_point = pd.DataFrame({
        'x': [0.0],
        'y': [1.0]
    })
    
    expected_ccw = pd.DataFrame({
        'x': [-1.0],
        'y': [ 0.0]
    })
    
    expected_cw = pd.DataFrame({
        'x': [1.0],
        'y': [0.0]
    })
    
    test_ccw = transform.rotate(
        sample_point,
        rotation_dir = 'ccw',
        angle = 0.5
    )
    
    test_cw = transform.rotate(
        sample_point,
        rotation_dir = 'cw',
        angle = 0.5
    )
    
    assert_frame_equal(expected_ccw, test_ccw)
    assert_frame_equal(expected_cw, test_cw)
    
def test_translate():
    """
    Test that transform.translate() accurately translates a dataframe's points
    in both the x and y directions
    """
    sample_point = pd.DataFrame({
        'x': [0.0],
        'y': [0.0]
    })
    
    expected_x_only = pd.DataFrame({
        'x': [1.0],
        'y': [0.0]
    })
    
    expected_y_only = pd.DataFrame({
        'x': [0.0],
        'y': [1.0]
    })
    
    expected_x_and_y = pd.DataFrame({
        'x': [1.0],
        'y': [1.0]
    })
    
    test_x_only = transform.translate(
        sample_point,
        translate_x = 1,
        translate_y = 0
    )
    
    test_y_only = transform.translate(
        sample_point,
        translate_x = 0,
        translate_y = 1
    )
    
    test_x_and_y = transform.translate(
        sample_point,
        translate_x = 1,
        translate_y = 1
    )
    
    assert_frame_equal(expected_x_only, test_x_only)
    assert_frame_equal(expected_y_only, test_y_only)
    assert_frame_equal(expected_x_and_y, test_x_and_y)
    
def test_scale():
    """
    Test that transform.scale() accurately scales a dataframe's points
    """
    sample_points = create.square(side_length = 1)
    
    expected_points = pd.DataFrame({
        'x': [
            -1.0,
             1.0,
             1.0,
            -1.0,
            -1.0
        ],
        
        'y': [
            -1.0,
            -1.0,
             1.0,
             1.0,
            -1.0
        ]
    })
    
    test_points = transform.scale(sample_points, scale_factor = 2)
    
    assert_frame_equal(expected_points, test_points)