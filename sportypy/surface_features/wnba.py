"""
@author: Ross Drucker
"""
"""
Functions needed to draw a regulation WNBA basketball court

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd

from helpers.coordinate_ops import create_shapes as create
from helpers.coordinate_ops import transformations as transform

def inner_center_circle(full_surf = True, rotate = False,
                        rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the inner center circle
    as in the court diagram on page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    inner_center_circle: A pandas dataframe containing the points that comprise
        the center circle of the court
    """
    # Draw the inner semicircle at half court. It has an inner radius of 2'
    # and thickness of 2"
    inner_center_circle = create.circle(
        d = 4 + (4/12),
        start = 1/2,
        end = 3/2
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [-4]
        })
    ).append(
        create.circle(
            d = 4,
            start = 3/2,
            end = 1/2
        )
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [4]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        inner_center_circle = inner_center_circle.append(
            transform.reflect(inner_center_circle, over_y = True)
        )
        
    # Rotate the coordinates if necessary
    if rotate:
        inner_center_circle = transform.rotate(
            inner_center_circle,
            rotation_dir
        )
    
    return inner_center_circle

def outer_center_circle(full_surf = True, rotate = False,
                        rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the outer center circle
    as in the court diagram on page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    outer_center_circle: A pandas dataframe containing the points that comprise
        the center circle of the court
    """
    # Draw the outer semicircle at half court. It has an outer radius of 6'
    # and thickness of 2"
    outer_center_circle = create.circle(
        d = 12 - (4/12),
        start = 1/2,
        end = 3/2
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [-12]
        })
    ).append(
        create.circle(
            d = 12,
            start = 3/2,
            end = 1/2
        )
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [12]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        outer_center_circle = outer_center_circle.append(
            transform.reflect(outer_center_circle, over_y = True)
        )
        
    # Rotate the coordinates if necessary
    if rotate:
        outer_center_circle = transform.rotate(
            outer_center_circle,
            rotation_dir
        )
    
    return outer_center_circle

def division_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of
    the division line as in the court diagram on page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    division_line: A pandas dataframe of the division line on the court
    """
    # The line's center should be 47' from the interior side of the baselines,
    # and must be 2" thick
    division_line = create.rectangle(
        x_min = -1/12, x_max = 0,
        y_min = -25, y_max = 25
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        division_line = division_line.append(
            transform.reflect(division_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        division_line = transform.rotate(
            division_line,
            rotation_dir
        )
    
    return division_line

def endlines_sideline(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    end lines, sidelines, hash marks, and substitution areas as in the court
    diagram on page 8 of the WNBA rule book, as well as the hash marks on the
    sides of the court
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    endline_sideline: a pandas dataframe of the end lines, side lines, hash
        marks, and substitution area markers
    """
    # The endlines, sideline, hash marks, and substitution area form the
    # boundary of the court
    endline_sideline = pd.DataFrame({
        'x': [
            0,
            -19 + (2/12),
            -19 + (2/12),
            -19,
            -19,
            -47,
            -47,
            -47 + (6/12),
            -47 + (6/12),
            -47,
            -47,
            -47 + (6/12),
            -47 + (6/12),
            -47,
            -47,
            -19,
            -19,
            -19 + (2/12),
            -19 + (2/12),
            0,
            0,
            -4,
            -4,
            -4 - (2/12),
            -4 - (2/12),
            -47 - (2/12),
            -47 - (2/12),
            0,
            0
        ],
        
        'y': [
            -25,
            -25,
            -22,
            -22,
            -25,
            -25,
            -11 - (2/12),
            -11 - (2/12),
            -11,
            -11,
            11,
            11,
            11 + (2/12),
            11 + (2/12),
            25,
            25,
            22,
            22,
            25,
            25,
            25 + (2/12),
            25 + (2/12),
            29,
            29,
            25 + (2/12),
            25 + (2/12),
            -25 - (2/12),
            -25 - (2/12),
            -25
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        endline_sideline = endline_sideline.append(
            transform.reflect(endline_sideline, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        endline_sideline = transform.rotate(
            endline_sideline,
            rotation_dir
        )
    
    return endline_sideline

def court_apron(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    court apron as in the court diagram on page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    court_apron: a pandas dataframe of the court border
    """
    # Courts have borders around the outside of the court that are different
    # in color than the end lines and sidelines. They are usually about 5' on
    # the sidelines and 8' on the end lines
    court_apron = pd.DataFrame({
        'x': [
            0,
            -47 - (2/12),
            -47 - (2/12),
            0,
            0,
            -57 - (4/12),
            -57 - (4/12),
            0,
            0
        ],
        
        'y': [
            -25 - (2/12),
            -25 - (2/12),
            25 + (2/12),
            25 + (2/12),
            30 + (2/12),
            30 + (2/12),
            -30 - (2/12),
            -30 - (2/12),
            -25 - (2/12)
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        court_apron = court_apron.append(
            transform.reflect(court_apron, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        court_apron = transform.rotate(
            court_apron,
            rotation_dir
        )
    
    return court_apron

def free_throw_lane(full_surf = True, rotate = False, rotation_dir = 'ccw',
                    include_amateur = False):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    professional-sized free throw lane as in the court diagram on page 8 of
    the WNBA rule book. This free-throw lane is required for all teams. This
    will also generate the free-throw lane for amateur (college) basketball if
    desired
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    free_throw_lane_dict: a dictionary containing up to two pandas dataframes:
        one for professional-sized free-throw lanes, and one for amateur
        (college)
    """
    # The free throw lane goes from the endline inwards a distance of 18' 10"
    # (interior) and 19' (exterior) with a width of 6'
    pro_free_throw_lane = pd.DataFrame({
        'x': [
            -47,
            -28,
            -28,
            -47,
            -47,
            -28 - (2/12),
            -28 - (2/12),
            -47,
            -47
        ],
        
        'y': [
            -8,
            -8,
            8,
            8,
            8 - (2/12),
            8 - (2/12),
            -8 + (2/12),
            -8 + (2/12),
            -8
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        pro_free_throw_lane = pro_free_throw_lane.append(
            transform.reflect(pro_free_throw_lane, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        pro_free_throw_lane = transform.rotate(
            pro_free_throw_lane,
            rotation_dir
        )
    
    free_throw_lane_dict = {
        'professional': pro_free_throw_lane
    }
    
    if include_amateur:
        am_free_throw_lane = pd.DataFrame({
            'x': [
                -47,
                -28,
                -28,
                -47,
                
                -47,
                -28 - (2/12),
                -28 - (2/12),
                -47,
                
                -47
            ],
            
            'y': [
                -6,
                -6,
                6,
                6,
                
                6 - (2/12),
                6 - (2/12), 
                -6 + (2/12),
                -6 + (2/12),
                
                -6
            ]
        })
        
        # Reflect the x coordinates over the y axis
        if full_surf:
            am_free_throw_lane = am_free_throw_lane.append(
                transform.reflect(am_free_throw_lane, over_y = True)
            )
        
        # Rotate the coordinates if necessary
        if rotate:
            am_free_throw_lane = transform.rotate(
                am_free_throw_lane,
                rotation_dir
            )
            
        free_throw_lane_dict['amateur'] = am_free_throw_lane
    
    return free_throw_lane_dict

def free_throw_circle(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframes for the points that comprise the free-throw circles
    as specified in page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    free_throw_circles_dict: a dictionary with keys 'solid' and 'dash_x', where
        x is a number that corresponds to a dashed section of the free throw
        circle
    """
    # The free-throw circle is 6' in diameter from the center of the free-throw
    # line (exterior)
    free_throw_circle_solid = create.circle(
        center = (-28 - (1/12), 0),
        start = -1/2,
        end = 1/2,
        d = 12
    ).append(
        pd.DataFrame({
            'x':[-28 - (1/12)],
            'y':[6]
        })
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = 1/2,
            end = -1/2,
            d = 12 - (4/12)
        )
    ).append(
        pd.DataFrame({
            'x':[-28 - (1/12)],
            'y':[-6]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        free_throw_circle_solid = free_throw_circle_solid.append(
            transform.reflect(free_throw_circle_solid, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        free_throw_circle_solid = transform.rotate(
            free_throw_circle_solid,
            rotation_dir
        )
    
    # The dashed sections of the free-throw circle
    free_throw_circle_dash_1 = create.circle(
        center = (-28 - (1/12), 0),
        start = (1/2) + (((12.29/72) + (15.5/72)) / np.pi),
        end = (1/2) + (((12.29/72) + (31/72)) / np.pi),
        d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.29/72) + (31/72)) / np.pi),
            end = (1/2) + (((12.29/72) + (15.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.29/72) + (15.5/72)) / np.pi),
            end = (1/2) + (((12.29/72) + (31/72)) / np.pi),
            d = 12
        ).iloc[0]
    )
    
    free_throw_circle_dash_2 = create.circle(
        center = (-28 - (1/12), 0),
        start = (1/2) + (((12.29/72) + (46.5/72)) / np.pi),
        end = (1/2) + (((12.20/72) + (62/72)) / np.pi),
        d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.20/72) + (62/72)) / np.pi),
            end = (1/2) + (((12.29/72) + (46.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.29/72) + (46.5/72)) / np.pi),
            end = (1/2) + (((12.20/72) + (62/72)) / np.pi),
            d = 12
        ).iloc[0]
    )
        
    free_throw_circle_dash_3 = create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.29/72) + (77.5/72)) / np.pi),
            end = (1/2) + (((12.20/72) + (93/72)) / np.pi),
            d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (1/2) + (((12.20/72) + (93/72)) / np.pi),
            end = (1/2) + (((12.29/72) + (77.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
                center = (-28 - (1/12), 0),
                start = (1/2) + (((12.29/72) + (77.5/72)) / np.pi),
                end = (1/2) + (((12.20/72) + (93/72)) / np.pi),
                d = 12
        ).iloc[0]
    )
        
    free_throw_circle_dash_4 = create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.29/72) + (77.5/72)) / np.pi),
            end = (-1/2) - (((12.20/72) + (93/72)) / np.pi),
            d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.20/72) + (93/72)) / np.pi),
            end = (-1/2) - (((12.29/72) + (77.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.29/72) + (77.5/72)) / np.pi),
            end = (-1/2) - (((12.20/72) + (93/72)) / np.pi),
            d = 12
        ).iloc[0]
    )
        
    free_throw_circle_dash_5 = create.circle(
        center = (-28 - (1/12), 0),
        start = (-1/2) - (((12.29/72) + (46.5/72)) / np.pi),
        end = (-1/2) - (((12.20/72) + (62/72)) / np.pi),
        d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.20/72) + (62/72)) / np.pi),
            end = (-1/2) - (((12.29/72) + (46.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.29/72) + (46.5/72)) / np.pi),
            end = (-1/2) - (((12.20/72) + (62/72)) / np.pi),
            d = 12
        ).iloc[0]
    )
    
    free_throw_circle_dash_6 = create.circle(
        center = (-28 - (1/12), 0),
        start = (-1/2) - (((12.29/72) + (15.5/72)) / np.pi),
        end = (-1/2) - (((12.29/72) + (31/72)) / np.pi),
        d = 12
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.29/72) + (31/72)) / np.pi),
            end = (-1/2) - (((12.29/72) + (15.5/72)) / np.pi),
            d = 12 - (4/12)
        )
    ).append(
        create.circle(
            center = (-28 - (1/12), 0),
            start = (-1/2) - (((12.29/72) + (15.5/72)) / np.pi),
            end = (-1/2) - (((12.29/72) + (31/72)) / np.pi),
            d = 12
        ).iloc[0]
    )
        
    # Reflect the x coordinates over the y axis
    if full_surf:
        free_throw_circle_dash_1 = free_throw_circle_dash_1.append(
            transform.reflect(free_throw_circle_dash_1, over_y = True)
        )
        
        free_throw_circle_dash_2 = free_throw_circle_dash_2.append(
            transform.reflect(free_throw_circle_dash_2, over_y = True)
        )
        
        free_throw_circle_dash_3 = free_throw_circle_dash_3.append(
            transform.reflect(free_throw_circle_dash_3, over_y = True)
        )
        
        free_throw_circle_dash_4 = free_throw_circle_dash_4.append(
            transform.reflect(free_throw_circle_dash_4, over_y = True)
        )
        
        free_throw_circle_dash_5 = free_throw_circle_dash_5.append(
            transform.reflect(free_throw_circle_dash_5, over_y = True)
        )
        
        free_throw_circle_dash_6 = free_throw_circle_dash_6.append(
            transform.reflect(free_throw_circle_dash_6, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        free_throw_circle_dash_1 = transform.rotate(
            free_throw_circle_dash_1,
            rotation_dir
        )
        
        free_throw_circle_dash_2 = transform.rotate(
            free_throw_circle_dash_2,
            rotation_dir
        )
        
        free_throw_circle_dash_3 = transform.rotate(
            free_throw_circle_dash_3,
            rotation_dir
        )
        
        free_throw_circle_dash_4 = transform.rotate(
            free_throw_circle_dash_4,
            rotation_dir
        )
        
        free_throw_circle_dash_5 = transform.rotate(
            free_throw_circle_dash_5,
            rotation_dir
        )
        
        free_throw_circle_dash_6 = transform.rotate(
            free_throw_circle_dash_6,
            rotation_dir
        )
    
    free_throw_circle_dict = {
        'solid': free_throw_circle_solid,
        'dash_1': free_throw_circle_dash_1,
        'dash_2': free_throw_circle_dash_2,
        'dash_3': free_throw_circle_dash_3,
        'dash_4': free_throw_circle_dash_4,
        'dash_5': free_throw_circle_dash_5,
        'dash_6': free_throw_circle_dash_6
    }
    
    return free_throw_circle_dict

def blocks(full_surf = True, rotate = False, rotation_dir = 'ccw',
           include_amateur = False):
    """
    Generate the dataframes for the points that comprise the blocks as
    specified in page 8 of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    blocks_dict: a dictionary with the block numbers as keys and the dataframes
        to use for plotting as values
    """
    # The first block is 7' (interior) from the endline, and is 2" thick
    professional_block_1 = create.rectangle(
        x_min = -40, x_max = -40 + (2/12),
        y_min = -8.5, y_max = -8
    )
    
    # The second block is 8" (interior) from the first block, and is 2" thick
    professional_block_2 = create.rectangle(
        x_min = -40 + (10/12), x_max = -39,
        y_min = -8.5, y_max = -8
    )
    
    # The third block is 3' (interior) from the second block, and is 2" thick
    professional_block_3 = create.rectangle(
        x_min = -36, x_max = -36 + (2/12),
        y_min = -8.5, y_max = -8
    )
    
    # The fourth block is 3' (interior) from the third block, and is 2" thick
    professional_block_4 = create.rectangle(
        x_min = -33 + (2/12), x_max = -33 + (4/12),
        y_min = -8.5, y_max = -8
    )
    
    # Block 1 but on the other side of the free-throw lane
    professional_block_5 = create.rectangle(
        x_min = -40, x_max = -40 + (2/12),
        y_min = 8.5, y_max = 8
    )
    
    # Block 2 but on the other side of the free-throw lane
    professional_block_6 = create.rectangle(
        x_min = -40 + (10/12), x_max = -39,
        y_min = 8.5, y_max = 8
    )
    
    # Block 3 but on the other side of the free-throw lane
    professional_block_7 = create.rectangle(
        x_min = -36, x_max = -36 + (2/12),
        y_min = 8.5, y_max = 8
    )
    
    # Block 4 but on the other side of the free-throw lane
    professional_block_8 = create.rectangle(
        x_min = -33 + (2/12), x_max = -33 + (4/12),
        y_min = 8.5, y_max = 8
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        professional_block_1 = professional_block_1.append(
            transform.reflect(professional_block_1, over_y = True)
        )
        
        professional_block_2 = professional_block_2.append(
            transform.reflect(professional_block_2, over_y = True)
        )
        
        professional_block_3 = professional_block_3.append(
            transform.reflect(professional_block_3, over_y = True)
        )
        
        professional_block_4 = professional_block_4.append(
            transform.reflect(professional_block_4, over_y = True)
        )
        
        professional_block_5 = professional_block_5.append(
            transform.reflect(professional_block_5, over_y = True)
        )
        
        professional_block_6 = professional_block_6.append(
            transform.reflect(professional_block_6, over_y = True)
        )
        
        professional_block_7 = professional_block_7.append(
            transform.reflect(professional_block_7, over_y = True)
        )
        
        professional_block_8 = professional_block_8.append(
            transform.reflect(professional_block_8, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        professional_block_1 = transform.rotate(
            professional_block_1,
            rotation_dir
        )
        
        professional_block_2 = transform.rotate(
            professional_block_2,
            rotation_dir
        )
        
        professional_block_3 = transform.rotate(
            professional_block_3,
            rotation_dir
        )
        
        professional_block_4 = transform.rotate(
            professional_block_4,
            rotation_dir
        )
        
        professional_block_5 = transform.rotate(
            professional_block_5,
            rotation_dir
        )
        
        professional_block_6 = transform.rotate(
            professional_block_6,
            rotation_dir
        )
        
        professional_block_7 = transform.rotate(
            professional_block_7,
            rotation_dir
        )
        
        professional_block_8 = transform.rotate(
            professional_block_8,
            rotation_dir
        )
        
    blocks_dict = {
        'professional_block_1': professional_block_1,
        'professional_block_2': professional_block_2,
        'professional_block_3': professional_block_3,
        'professional_block_4': professional_block_4,
        'professional_block_5': professional_block_5,
        'professional_block_6': professional_block_6,
        'professional_block_7': professional_block_7,
        'professional_block_8': professional_block_8,
    }
    
    if include_amateur:
        # The first set of blocks are 7' from the interior of the baseline, and
        # measure 1' in width
        amateur_block_1 = create.rectangle(
            x_min = -40, x_max = -39,
            y_min = -6 - (8/12), y_max = -6
        )
        
        # The second set of blocks are 3' from the first block, and measure 2"
        # in width
        amateur_block_2 = create.rectangle(
            x_min = -36, x_max = -36 + (2/12),
            y_min = -6 - (8/12), y_max = -6
        )
        
        # The third set of blocks are 3' from the second block, and measure 2"
        # in width
        amateur_block_3 = create.rectangle(
            x_min = -33 + (2/12), x_max = -33 + (4/12),
            y_min = -6 - (8/12), y_max = -6
        )
        
        # The fourth set of blocks are 3' from the third block, and measure 2"
        # in width
        amateur_block_4 = create.rectangle(
            x_min = -30 + (4/12), x_max = -30 + (6/12),
            y_min = -6 - (8/12), y_max = -6
        )
        
        # Block 1 but on the other side of the free-throw lane
        amateur_block_5 = create.rectangle(
            x_min = -40, x_max = -39,
            y_min = 6, y_max = 6 + (8/12)
        )
        
        # Block 2 but on the other side of the free-throw lane
        amateur_block_6 = create.rectangle(
            x_min = -36, x_max = -36 + (2/12),
            y_min = 6, y_max = 6 + (8/12)
        )
        
        # Block 3 but on the other side of the free-throw lane
        amateur_block_7 = create.rectangle(
            x_min = -33 + (2/12), x_max = -33 + (4/12),
            y_min = 6, y_max = 6 + (8/12)
        )
        
        # Block 4 but on the other side of the free-throw lane
        amateur_block_8 = create.rectangle(
            x_min = -30 + (4/12), x_max = -30 + (6/12),
            y_min = 6, y_max = 6 + (8/12)
        )
        
        # Reflect the x coordinates over the y axis
        if full_surf:
            amateur_block_1 = amateur_block_1.append(
                transform.reflect(amateur_block_1, over_y = True)
            )
            
            amateur_block_2 = amateur_block_2.append(
                transform.reflect(amateur_block_2, over_y = True)
            )
            
            amateur_block_3 = amateur_block_3.append(
                transform.reflect(amateur_block_3, over_y = True)
            )
            
            amateur_block_4 = amateur_block_4.append(
                transform.reflect(amateur_block_4, over_y = True)
            )
            
            amateur_block_5 = amateur_block_5.append(
                transform.reflect(amateur_block_5, over_y = True)
            )
            
            amateur_block_6 = amateur_block_6.append(
                transform.reflect(amateur_block_6, over_y = True)
            )
            
            amateur_block_7 = amateur_block_7.append(
                transform.reflect(amateur_block_7, over_y = True)
            )
            
            amateur_block_8 = amateur_block_8.append(
                transform.reflect(amateur_block_8, over_y = True)
            )
        
        # Rotate the coordinates if necessary
        if rotate:
            amateur_block_1 = transform.rotate(
                amateur_block_1,
                rotation_dir
            )
            
            amateur_block_2 = transform.rotate(
                amateur_block_2,
                rotation_dir
            )
            
            amateur_block_3 = transform.rotate(
                amateur_block_3,
                rotation_dir
            )
            
            amateur_block_4 = transform.rotate(
                amateur_block_4,
                rotation_dir
            )
            
            amateur_block_5 = transform.rotate(
                amateur_block_5,
                rotation_dir
            )
            
            amateur_block_6 = transform.rotate(
                amateur_block_6,
                rotation_dir
            )
            
            amateur_block_7 = transform.rotate(
                amateur_block_7,
                rotation_dir
            )
            
            amateur_block_8 = transform.rotate(
                amateur_block_8,
                rotation_dir
            )
            
        blocks_dict['amateur_block_1'] = amateur_block_1
        blocks_dict['amateur_block_2'] = amateur_block_2
        blocks_dict['amateur_block_3'] = amateur_block_3
        blocks_dict['amateur_block_4'] = amateur_block_4
        blocks_dict['amateur_block_5'] = amateur_block_5
        blocks_dict['amateur_block_6'] = amateur_block_6
        blocks_dict['amateur_block_7'] = amateur_block_7
        blocks_dict['amateur_block_8'] = amateur_block_8
        
    return blocks_dict

def lower_defensive_box_mark(full_surf = True, rotate = False,
                             rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    lower defensive box tick marks as in the court diagram on page 8 of the
    WNBA Rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    lower_defensive_box_mark_dict: a dictionary with the two hash marks that
        comprise the lower defensive box hash marks
    """
    
    # The defensive hash marks are 13' (interior) from the end line, is 2"
    # wide, and 6" long
    lower_defensive_box_mark_1 = create.rectangle(
        x_min = -34, x_max = -34 + (2/12),
        y_min = -5, y_max = -4.5
    )
    
    lower_defensive_box_mark_2 = create.rectangle(
        x_min = -34, x_max = -34 + (2/12),
        y_min = 4.5, y_max = 5
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        lower_defensive_box_mark_1 = lower_defensive_box_mark_1.append(
            transform.reflect(lower_defensive_box_mark_1, over_y = True)
        )
        
        lower_defensive_box_mark_2 = lower_defensive_box_mark_2.append(
            transform.reflect(lower_defensive_box_mark_2, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        lower_defensive_box_mark_1 = transform.rotate(
            lower_defensive_box_mark_1,
            rotation_dir
        )
        
        lower_defensive_box_mark_2 = transform.rotate(
            lower_defensive_box_mark_2,
            rotation_dir
        )
        
    lower_defensive_box_mark_dict = {
        'lower_defensive_box_mark_1': lower_defensive_box_mark_1,
        'lower_defensive_box_mark_2': lower_defensive_box_mark_2
    }
    
    return lower_defensive_box_mark_dict

def three_point_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the three-point line
    as specified in the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    three_point_lines: a pandas dataframe of the three-point line
    """
    # First, a bit of math is needed to determine the starting and ending
    # angles of the three-point arc, relative to 0 radians. Since in the end,
    # the angle is what matters, the units of measure do not. Inches are easier
    # to use for this calculation. The angle begins 3' from the interior edge
    # of the sideline
    start_y = (22 * 12)
    
    # The rule book describes the arc as having a radius of 23' 9"
    radius_outer = (22 * 12) + 1.75
    
    # From here, the calculation is relatively straightforward. To determine
    # the angle, the inverse sine is needed. It will be multiplied by pi
    # so that it can be passed to the create_circle() function
    start_angle_outer = math.asin(start_y / radius_outer) / np.pi
    end_angle_outer = -start_angle_outer
    
    # The same method can be used for the inner angles, however, since the
    # inner radius will be traced from bottom to top, the angle must be
    # negative to start
    radius_inner = (22 * 12) + 1.75 - 2
    start_angle_inner = -math.asin((start_y - 2) / radius_inner) / np.pi
    end_angle_inner = -start_angle_inner
    
    # According to the rulebook, the three-point line is 21' 7 7/8" in the
    # corners
    three_point_line = pd.DataFrame({
        'x': [-47],
        'y': [22]
    }).append(
        create.circle(
            center = (-41.75, 0),
            d = 2 * (radius_outer / 12),
            start = start_angle_outer,
            end = end_angle_outer
        )
    ).append(
        pd.DataFrame({
            'x': [
                -47,
                -47
            ],
            
            'y': [
                -22,
                -22 + (2/12)
            ]
        })
    ).append(
        create.circle(
            center = (-41.75, 0),
            d = 2 * (radius_inner / 12),
            start = start_angle_inner,
            end = end_angle_inner
        )
    ).append(
        pd.DataFrame({
            'x': [
                -47,
                -47
            ],
            
            'y': [
                22 - (2/12),
                22
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        three_point_line = three_point_line.append(
            transform.reflect(three_point_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        three_point_line = transform.rotate(
            rotation_dir,
            three_point_line
        )
    
    return three_point_line

def restricted_area_arc(full_surf = True, rotate = False,
                        rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the restricted-area
    arcs as specified in the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    restricted_area_arcs: a pandas dataframe of the restricted-area arcs
    """
    # Following the same process as for the three-point line, the restricted
    # area arc's starting and ending angle can be computed
    start_y = -4 - (2/12)
    
    # The rule book describes the arc as having a radius of 4'
    radius_outer = 4 + (2/12)
    
    # From here, the calculation is relatively straightforward. To determine
    # the angle, the inverse sine is needed. It will be multiplied by pi
    # so that it can be passed to the create_circle() function
    start_angle_outer = math.asin(start_y / radius_outer) / np.pi
    end_angle_outer = -start_angle_outer
    
    # The same method can be used for the inner angles, however, since the
    # inner radius will be traced from bottom to top, the angle must be
    # negative to start
    radius_inner = 4
    start_angle_inner = -math.asin((start_y + (2/12)) / radius_inner) / np.pi
    end_angle_inner = -start_angle_inner
    
    # The restricted area arc is an arc of radius 4' from the center of the
    # basket, and extending in a straight line to the front face of the
    # backboard, and having thickness of 2"
    restricted_area_arc = pd.DataFrame({
        'x': [-43],
        'y': [-4 - (2/12)]
    }).append(
        create.circle(
            center = (-41.75, 0),
            d = 8 + (4/12),
            start = start_angle_outer,
            end = end_angle_outer
        )
    ).append(
        pd.DataFrame({
            'x': [-43, -43],
            'y': [4 + (2/12), 4]
        })
    ).append(
        create.circle(
            center = (-41.75, 0),
            d = 8,
            start = start_angle_inner,
            end = end_angle_inner
        )
    ).append(
        pd.DataFrame({
            'x': [-43, -43],
            'y': [-4, -4 - (2/12)]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        restricted_area_arc = restricted_area_arc.append(
            transform.reflect(restricted_area_arc, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        restricted_area_arc = transform.rotate(
            rotation_dir,
            restricted_area_arc
        )
        
    return restricted_area_arc

def backboard(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the backboard as
    specified in the court diagram of the WNBA rule book

    Returns
    -------
    backboard: a pandas dataframe of the backboard
    """
    # Per the rule book, the backboard must by 6' wide. The height of the
    # backboard is irrelevant in this graphic, as this is a bird's eye view
    # over the court
    backboard = create.rectangle(
        x_min = -43 - (4/12), x_max = -43,
        y_min = -3, y_max = 3
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        backboard = backboard.append(
            transform.reflect(backboard, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        backboard = transform.rotate(
            backboard,
            rotation_dir
        )
        
    return backboard

def goal(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the goals as specified
    in the court diagram of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    goals: a pandas dataframe of the goals
    """
    # Get the starting angle of the ring. The connector has a width of 5", so
    # 2.5" are on either side. The ring has a radius of 9", so the arcsine of
    # these measurements should give the angle at which point they connect
    start_angle = np.pi - math.asin(2.5/9)
    
    # The ending angle of the ring would be the negative of the starting angle
    end_angle = -start_angle
    
    # Define the coordinates for the goal
    goal = pd.DataFrame({
        'x': [
            -43,
            -41.75 - ((9/12) * math.cos(start_angle))
        ],
        
        'y': [
            2.5/12,
            2.5/12
        ]
    }).append(
        create.circle(
            center = (-41.75, 0),
            start = start_angle,
            end = end_angle,
            d = 1.5 + (4/12)
        )
    ).append(
        pd.DataFrame({
            'x': [
                -41.75 - ((9/12) * math.cos(start_angle)),
                -43,
                -43
            ],
            
            'y': [
                -2.5/12,
                -2.5/12,
                2.5/12
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        goal = goal.append(
            transform.reflect(goal, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        goal = transform.rotate(
            goal,
            rotation_dir
        )
        
    return goal

def net(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the rings as specified
    in the court diagram of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    nets: a pandas dataframe of the nets
    """
    # The ring's center is 15" from the backboard, and 63" from the baseline,
    # which means it is centered at (+/-41.75, 0). The ring has an interior
    # diameter of 18", which is where the net is visible from above
    net = create.circle(
        center = (-41.75, 0),
        d = 1.5
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        net = net.append(
            transform.reflect(net, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        net = transform.rotate(
            net,
            rotation_dir
        )
    
    return net

def painted_area(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    free throw lane as specified in the court diagram of the WNBA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    painted_areas: a pandas dataframe of the painted areas
    """
    # The interior of the free throw lane is known as the painted area, and
    # can be a different color than the markings and court. These coordinates
    # can be used to color them on the plot
    painted_area = create.rectangle(
        x_min = -47, x_max = -28 - (2/12),
        y_min = -8 + (2/12), y_max = 8 - (2/12)
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        painted_area = painted_area.append(
            transform.reflect(painted_area, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        painted_area = transform.rotate(
            painted_area,
            rotation_dir
        )
    
    return painted_area