"""
Module to perform basic coordinate transformations to aid in creating a
playing surface

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd

def reflect(df, over_x = False, over_y = True):
    """
    Performs a mathematical reflection over a specified axis

    Parameters
    ----------
    df: the input pandas dataframe. It must have an 'x' column and a 'y' column
    over_x: whether or not to reflect over the x axis
    over_y: whether or not to reflect over the y axis

    Returns
    -------
    out: the reflected pandas dataframe
    """
    # Make a copy of the original dataframe on which to operate
    reflected = df.copy()
    
    # If a reflection over the x axis is required, perform it
    if over_y:
        reflected = pd.DataFrame({
            'x': -1 * reflected['x'],
            'y': reflected['y']
        })
        
    # If a reflection over the y axis is required, perform it
    if over_x:
        reflected = pd.DataFrame({
            'x': reflected['x'],
            'y': -1 * reflected['y']
        })
        
    return reflected

def rotate(df, rotation_dir = 'ccw', angle = .5):
    """
    Performs a mathematical rotation about (0, 0). This rotation is given as:
        x' = x * cos(theta) - y * sin(theta) 
        y' = x * sin(theta) + y * cos(theta)

    Parameters
    ----------
    df: the input pandas dataframe. It must have an 'x' column and a 'y' column
    rotation_dir: the rotation direction. 'ccw' corresponds to counterclockwise
    angle: the angle (in radians) by which to rotate the coordinates, divided
        by pi

    Returns
    -------
    rotated: the rotated dataframe
    """
    # If the rotation direction is clockwise, take the negative of the angle
    if rotation_dir.lower() not in ['ccw', 'counter', 'counterclockwise']:
        angle *= -1
    
    # Set theta to be the angle of rotation
    theta = angle * np.pi
    
    # Make a copy of the original dataframe on which to operate
    rotated = df.copy()
    rotated['x'] = (df['x'] * math.cos(theta)) - (df['y'] * math.sin(theta))
    rotated['y'] = (df['x'] * math.sin(theta)) + (df['y'] * math.cos(theta))
    
    return rotated

def translate(df, translate_x = 0, translate_y = 0):
    """
    Performs a mathematical translation of coordinates

    Parameters
    ----------
    df: the input pandas dataframe. It must have an 'x' column and a 'y' column
    translate_x: how many units (in the input dataframe's units) to translate
        the points in the +x direction
    translate_y: how many units (in the input dataframe's units) to translate
        the points in the +y direction

    Returns
    -------
    translated: the translated dataframe
    """
    # Make a copy of the original dataframe on which to operate
    translated = df.copy()
    
    # Translate the x and y coordinates
    translated['x'] = translated['x'] + translate_x
    translated['y'] = translated['y'] + translate_y
    
    return translated

def scale(df, scale_factor = 1):
    # Make a copy of the original dataframe on which to operate
    scaled = df.copy()
    
    # Scale the x and y coordinates
    scaled['x'] = scale_factor * scaled['x']
    scaled['y'] = scale_factor * scaled['y']
    
    return scaled