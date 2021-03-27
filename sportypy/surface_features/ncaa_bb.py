"""
Functions needed to draw a regulation NCAA basketball court

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd

from sportypy.helpers.coordinate_ops import create_shapes as create
from sportypy.helpers.coordinate_ops import transformations as transform

def center_circle(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the center circle as
    specified in Rule 1, Section 4, Article 1 of the NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    center_circle: A pandas dataframe containing the points that comprise the
        center circle of the court
    """
    # Draw the left outer semicircle, then move in 2" per the NCAA's required
    # line thickness, and draw inner semicircle. Doing it this way alleviates
    # future fill issues.
    center_circle = create.circle(
        d = 12,
        start = 1/2,
        end = 3/2
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [6 - (2/12)]
        })
    ).append(
        create.circle(
            d = 12 - (4/12),
            start = 3/2,
            end = 1/2
        )
    ).append(
        pd.DataFrame({
            'x': [0],
            'y': [-6]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        center_circle = center_circle.append(
            transform.reflect(center_circle, over_y = True)
        )
        
    # Rotate the coordinates if necessary
    if rotate:
        center_circle = transform.rotate(
            center_circle,
            rotation_dir
        )
            
    return center_circle

def division_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of
    the division line as specified in Rule 1, Section 5, Article 1 of the NCAA
    rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    division_line: A pandas dataframe of the interior boundaries of the court
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

def endline_sideline(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    end lines and sidelines as specified in Rule 1, Section 3, Article 2 of
    the NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    endline_sideline: a pandas dataframe of the end lines and side lines
    """
    # The endline and sideline form the boundary of the court
    endline_sideline = pd.DataFrame({
        'x': [
            0,
            -47,
            -47,
            0,
            0,
            -47 - (2/12),
            -47 - (2/12),
            0,
            0
            
        ],
        
        'y': [
            -25,
            -25,
            25,
            25,
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

def lower_def_box_ticks(full_surf = True, rotate = False,
                        rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    lower defensive box tick marks as specified in Rule 1, Section 3, Article 7
    of the NCAA rule book (women's only). While it only pertains to women's
    basketball, universities typically only have one court for both teams, so
    this marking appears on the men's floor as well
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    lower_defensive_box_tick: a pandas dataframe of the lower defensive box
        tick marks
    """
    # The defensive box is marked by two 2"-thick tick marks, each being 3'
    # from the edge of the lane and extending 12" into the court
    lower_defensive_box_tick = create.rectangle(
        x_min = -47, x_max = -46,
        y_min = -9 - (2/12), y_max = -9
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        lower_defensive_box_tick = lower_defensive_box_tick.append(
            transform.reflect(lower_defensive_box_tick, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        lower_defensive_box_tick = transform.rotate(
            lower_defensive_box_tick,
            rotation_dir
        )
    
    return lower_defensive_box_tick

def court_apron(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    court apron as specified in the court diagram of the NCAA rule book
    
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
            -55 - (4/12),
            -55 - (4/12),
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

def coaching_box(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    coaching boxes as specified in Rule 1, Section 9, Articles 1 and 2 of the
    NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    coaching_boxes: a pandas dataframe of the sidelines
    """
    # The coaching boxes are 38' from the interior of the baseline on each
    # side of the court, and extend 2' out of bounds from the exterior of the
    # sideline
    coaching_box = create.rectangle(
        x_min = -9 - (2/12), x_max = -9,
        y_min = 25, y_max = 27
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        coaching_box = coaching_box.append(
            transform.reflect(coaching_box, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        coaching_box = transform.rotate(
            coaching_box,
            rotation_dir
        )
    
    return coaching_box

def bench_area(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the team bench areas
    as specified on the court diagram in the NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    bench_areas: a pandas dataframe of the team bench areas
    """
    # The bench area is 28 feet from the interior of the endline, is 2" wide,
    # and extends 3' on each side of the sideline
    bench_area = create.rectangle(
        x_min = -19 - (2/12), x_max = -19,
        y_min = 22, y_max = 28
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        bench_area = bench_area.append(
            transform.reflect(bench_area, over_y = True)
        )
    # Rotate the coordinates if necessary
    if rotate:
        bench_area = transform.rotate(
            bench_area,
            rotation_dir
        )
    
    return bench_area

def free_throw_lane(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    free throw lane as specified in Rule 1, Section 6, Articles 1, 2, 3, and 4
    of the NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    free_throw_lanes: a pandas dataframe of the free throw lanes
    """
    # The free throw lane goes from the endline inwards a distance of 18' 10"
    # (interior) and 19' (exterior) with a width of 6'
    
    # The first set of blocks are 7' from the interior of the baseline, and
    # measure 1' in width
    
    # The second set of blocks are 3' from the first block, and
    # measure 2" in width
    
    # The third set of blocks are 3' from the second block, and
    # measure 2" in width
    
    # The fourth set of blocks are 3' from the third block, and
    # measure 2" in width
    free_throw_lane = pd.DataFrame({
        'x': [
            -47, -28, -28, -47, -47, -28 - (2/12), -28 - (2/12), -47, -47, -47
        ],
        
        'y': [
            -6, -6, 6, 6, 6 - (2/12), 6 - (2/12), -6 + (2/12), -6 + (2/12),
            6, -6
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        free_throw_lane = free_throw_lane.append(
            transform.reflect(free_throw_lane, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        free_throw_lane = transform.rotate(
            free_throw_lane,
            rotation_dir
        )
    
    return free_throw_lane

def blocks(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframes for the points that comprise the blocks as
    specified in page 8 of the NBA rule book
    
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
    # The first set of blocks are 7' from the interior of the baseline, and
    # measure 1' in width
    block_1 = create.rectangle(
        x_min = -40, x_max = -39,
        y_min = -6, y_max = -6 - (8/12),
    )
    
    # The second set of blocks are 3' from the first block, and
    # measure 2" in width
    block_2 = create.rectangle(
        x_min = -36, x_max = -36 + (2/12),
        y_min = -6, y_max = -6 - (8/12)
    )
    
    # The third set of blocks are 3' from the second block, and
    # measure 2" in width
    block_3 = create.rectangle(
        x_min = -33 + (2/12), x_max = -33 + (4/12),
        y_min = -6, y_max = -6 - (8/12)
    )
    
    # The fourth set of blocks are 3' from the third block, and
    # measure 2" in width
    block_4 = create.rectangle(
        x_min = -30 + (4/12), x_max = -30 + (6/12),
        y_min = -6, y_max = -6 - (8/12)
    )
    
    # Block 1 but on the other side of the free-throw lane
    block_5 = create.rectangle(
        x_min = -40, x_max = -39,
        y_min = 6, y_max = 6 + (8/12)
    )
    
    # Block 2 but on the other side of the free-throw lane
    block_6 = create.rectangle(
        x_min = -36, x_max = -36 + (2/12),
        y_min = 6, y_max = 6 + (8/12)
    )
    
    # Block 3 but on the other side of the free-throw lane
    block_7 = create.rectangle(
        x_min = -33 + (2/12), x_max = -33 + (4/12),
        y_min = 6, y_max = 6 + (8/12)
    )
    
    # Block 4 but on the other side of the free-throw lane
    block_8 = create.rectangle(
        x_min = -30 + (4/12), x_max = -30 + (6/12),
        y_min = 6, y_max = 6 + (8/12)
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        block_1 = block_1.append(
            transform.reflect(block_1, over_y = True)
        )
        
        block_2 = block_2.append(
            transform.reflect(block_2, over_y = True)
        )
        
        block_3 = block_3.append(
            transform.reflect(block_3, over_y = True)
        )
        
        block_4 = block_4.append(
            transform.reflect(block_4, over_y = True)
        )
        
        block_5 = block_5.append(
            transform.reflect(block_5, over_y = True)
        )
        
        block_6 = block_6.append(
            transform.reflect(block_6, over_y = True)
        )
        
        block_7 = block_7.append(
            transform.reflect(block_7, over_y = True)
        )
        
        block_8 = block_8.append(
            transform.reflect(block_8, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        block_1 = transform.rotate(
            block_1,
            rotation_dir
        )
        
        block_2 = transform.rotate(
            block_2,
            rotation_dir
        )
        
        block_3 = transform.rotate(
            block_3,
            rotation_dir
        )
        
        block_4 = transform.rotate(
            block_4,
            rotation_dir
        )
        
        block_5 = transform.rotate(
            block_5,
            rotation_dir
        )
        
        block_6 = transform.rotate(
            block_6,
            rotation_dir
        )
        
        block_7 = transform.rotate(
            block_7,
            rotation_dir
        )
        
        block_8 = transform.rotate(
            block_8,
            rotation_dir
        )
        
    blocks_dict = {
        'block_1': block_1,
        'block_2': block_2,
        'block_3': block_3,
        'block_4': block_4,
        'block_5': block_5,
        'block_6': block_6,
        'block_7': block_7,
        'block_8': block_8,
    }
    
    return blocks_dict
    
def painted_area(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    free throw lane as specified in Rule 1, Section 6, Articles 1, 2, 3, and 4
    of the NCAA rule book
    
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
        y_min = -6 + (2/12), y_max = 6 - (2/12)
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
    
def restricted_area_arc(full_surf = True, rotate = False,
                        rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the restricted-area
    arcs as specified in Rule 1, Section 8 of the NCAA rule book
    
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
            start = -1/2,
            end = 1/2
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
            start = 1/2,
            end = -1/2
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
    
def m_three_pt_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the three-point line
    as specified in Rule 1, Section 7 of the NCAA rule book. These points are
    the men's three-point line after being moved back prior to the 2019-2020
    season
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    m_three_pt_lines: a pandas dataframe of the three-point line
    """
    # First, a bit of math is needed to determine the starting and ending
    # angles of the three-point arc, relative to 0 radians. Since in the end,
    # the angle is what matters, the units of measure do not. Inches are easier
    # to use for this calculation. The angle begins 40 1/8" from the
    # interior edge of the sideline
    start_y = (25 * 12) - (40 + (1/8))
    
    # The rule book describes the arc as having a radius of 22' 1 3/4" from the
    # center of the basket
    radius_outer = (22 * 12) + 1.75
    
    # From here, the calculation is relatively straightforward. To determine
    # the angle, the inverse sine is needed. It will be multiplied by pi
    # so that it can be passed to the create_circle() function
    start_angle_outer = -math.asin(start_y / radius_outer) / np.pi
    end_angle_outer = -start_angle_outer
    
    # The same method can be used for the inner angles, however, since the
    # inner radius will be traced from top to bottom, the angle must be
    # negative to start
    radius_inner = (22 * 12) + 1.75 - 2
    start_angle_inner = math.asin((start_y - 2) / radius_inner) / np.pi
    end_angle_inner = -start_angle_inner
    
    # According to the rulebook, the three-point line is 21' 7 7/8" in the
    # corners
    m_three_pt_line = pd.DataFrame({
        'x': [
            -47
        ],
        
        'y': [
            -25 + ((40 + (1/8)) / 12)
        ]
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
                25 - ((40 + (1/8)) / 12),
                25 - ((42 + (1/8)) / 12)
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
                -25 + ((42 + (1/8)) / 12),
                -25 + ((40 + (1/8)) / 12)
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        m_three_pt_line = m_three_pt_line.append(
            transform.reflect(m_three_pt_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        m_three_pt_line = transform.rotate(
            rotation_dir,
            m_three_pt_line
        )
    
    return m_three_pt_line

def w_three_pt_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the three-point line
    as specified in Rule 1, Section 7 of the NCAA rule book. These points are
    the women's three-point line, and also where the men's three-point line was
    prior to the 2019-2020 season. While this line only pertains to women's
    basketball, universities typically only have one court for both teams, so
    this marking appears on the men's floor as well

    Returns
    -------
    w_three_pt_lines: a pandas dataframe of the three-point line
    """
    # This can be computed similarly to how the men's line was computed
    w_three_pt_line = pd.DataFrame({
        'x':[-47],
        'y':[-20.75]
    }).append(
        create.circle(
            center = (-41.75, 0),
            start = -1/2,
            end = 1/2,
            d = 41.5
        )
    ).append(
        pd.DataFrame({
            'x':[-47, -47],
            'y':[20.75, 20.75 - (2/12)]
        })
    ).append(
        create.circle(
            center = (-41.75, 0),
            start = 1/2,
            end = -1/2,
            d = 41.5 - (4/12)
        )
    ).append(
        pd.DataFrame({
            'x':[-47, -47],
            'y':[-20.75 + (2/12), -20.75]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        w_three_pt_line = w_three_pt_line.append(
            transform.reflect(w_three_pt_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        w_three_pt_line = transform.rotate(
            w_three_pt_line,
            rotation_dir
        )
    
    return w_three_pt_line

def free_throw_circle(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the free-throw circles
    as specified on the court diagram in the NCAA rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    free_throw_circles: a pandas dataframe of the free-throw circle
    """
    # The free-throw circle is 6' in diameter from the center of the free-throw
    # line (exterior)
    free_throw_circle = create.circle(
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
        free_throw_circle = free_throw_circle.append(
            transform.reflect(free_throw_circle, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        free_throw_circle = transform.rotate(
            free_throw_circle,
            rotation_dir
        )
    
    return free_throw_circle

def backboard(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the backboard as
    specified in Rule 1, Section 10, Article 2 of the NCAA rule book

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
    in Rule 1, Sections 14 and 15 of the NCAA rule book
    
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
    in Rule 1, Section 14, Article 2 of the NCAA rule book
    
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