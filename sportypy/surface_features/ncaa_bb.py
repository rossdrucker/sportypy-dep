"""
Functions needed to draw a regulation NCAA basketball court

@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd

from helper.coordinate_ops import create_shapes as create
from helper.coordinate_ops import transformations as transform

def center_circle(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the center circle as
    specified in Rule 1, Section 4, Article 1 of the NCAA rule book

    Returns
    -------
    center_circle: A pandas dataframe containing the points that comprise the
        center circle of the court
    """
    # Draw the right outer semicircle, then move in 2" per the NCAA's required
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
    if full_court:
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

def division_line(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of
    the division line as specified in Rule 1, Section 5, Article 1 of the NCAA
    rule book

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
    if full_court:
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

def endlines_sidelines(full_court = True, rotate = False,
                           rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    end lines and sidelines as specified in Rule 1, Section 3, Article 2 of
    the NCAA rule book

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
    if full_court:
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

def lower_defensive_box_ticks(full_court = True, rotate = False,
                              rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    lower defensive box tick marks as specified in Rule 1, Section 3, Article 7
    of the NCAA rule book (women's only). While it only pertains to women's
    basketball, universities typically only have one court for both teams, so
    this marking appears on the men's floor as well
    
    Returns
    -------
    endline_sideline: a pandas dataframe of the end lines and side lines
    """
    # The defensive box is marked by two 2"-thick tick marks, each being 3'
    # from the edge of the lane and extending 12" into the court
    lower_defensive_box_tick = create.rectangle(
        x_min = -47, x_max = -46,
        y_min = -9 - (2/12), y_max = -9
    )
    
    # Reflect the x coordinates over the y axis
    if full_court:
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

def court_border(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    court border as specified in the court diagram of the NCAA rule book

    Returns
    -------
    court_border: a pandas dataframe of the court border
    """
    # Courts have borders around the outside of the court that are different
    # in color than the end lines and sidelines. They are usually about 5' on
    # the sidelines and 8' on the end lines
    court_border = pd.DataFrame({
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
    if full_court:
        court_border = court_border.append(
            transform.reflect(court_border, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        court_border = transform.rotate(
            court_border,
            rotation_dir
        )
    
    return court_border

def coaching_boxes(full_court = True, rotate = False,
                       rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    coaching boxes as specified in Rule 1, Section 9, Articles 1 and 2 of the
    NCAA rule book

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
    if full_court:
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

def bench_areas(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the team bench areas
    as specified on the court diagram in the NCAA rule book

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
    if full_court:
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

def free_throw_lanes(full_court = True, rotate = False,
                         rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    free throw lane as specified in Rule 1, Section 6, Articles 1, 2, 3, and 4
    of the NCAA rule book

    Returns
    -------
    free_throw_lanes: a pandas dataframe of the free throw lanes
    painted_areas: a pandas dataframe of the painted areas
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
            # Start
            -47,
            
            # First block lower
            -40,
            -40,
            -39,
            -39,
            
            # Second block lower
            -36,
            -36,
            -36 + (2/12),
            -36 + (2/12),
            
            # Third block lower
            -33 + (2/12),
            -33 + (2/12),
            -33 + (4/12),
            -33 + (4/12),
            
            # Fourth block lower
            -30 + (4/12),
            -30 + (4/12),
            -30 + (6/12),
            -30 + (6/12),
            
            # End
            -28,
            
            # Cross
            -28,
            
            # Fourth block upper
            -30 + (6/12),
            -30 + (6/12),
            -30 + (4/12),
            -30 + (4/12),
            
            # Third block upper
            -33 + (2/12),
            -33 + (2/12),
            -33 + (4/12),
            -33 + (4/12),
            
            # Second block upper
            -36,
            -36,
            -36 + (2/12),
            -36 + (2/12),
            
            # First block upper
            -40,
            -40,
            -39,
            -39,
            
            # End of exterior
            -47,
            
            # Interior
            -47, -28 - (2/12), -28 - (2/12), -47, -47, -47
        ],
        
        'y': [
            -6,
            
            # First block lower
            -6,
            -6 - (8/12),
            -6 - (8/12),
            -6,
            
            # Second block lower
            -6,
            -6 - (8/12),
            -6 - (8/12),
            -6,
            
            # Third block lower
            -6,
            -6 - (8/12),
            -6 - (8/12),
            -6,
            
            # Fourth block lower
            -6,
            -6 - (8/12),
            -6 - (8/12),
            -6,
            
            # End
            -6,
            
            # Cross
            6,
            
            # Fourth block upper
            6,
            6 + (8/12),
            6 + (8/12),
            6,
            
            # Third block upper
            6,
            6 + (8/12),
            6 + (8/12),
            6,
            
            # Second block upper
            6,
            6 + (8/12),
            6 + (8/12),
            6,
            
             # First block upper
            6,
            6 + (8/12),
            6 + (8/12),
            6,
            
            # End of exterior
            6,
            
            # Interior
            6 - (2/12), 6 - (2/12), -6 + (2/12), -6 + (2/12), 6, -6
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_court:
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

def painted_areas(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    free throw lane as specified in Rule 1, Section 6, Articles 1, 2, 3, and 4
    of the NCAA rule book
    
    Returns
    -------
    painted_areas: a pandas dataframe of the painted areas
    """
    # The interior of the free throw lane is known as the painted area, and
    # can be a different color than the markings and court. These coordinates
    # can be used to color them on the plot
    painted_area = create.rectangle(
        x_min = -47, xmax = -28 - (2/12),
        y_min = -6 + (2/12), y_max = 6 - (2/12)
    )
    
    # Reflect the x coordinates over the y axis
    if full_court:
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
    
def restricted_area_arcs(full_court = True, rotate = False,
                             rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the restricted-area
    arcs as specified in Rule 1, Section 8 of the NCAA rule book

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
    if full_court:
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
    
def m_three_pt_lines(full_court = True, rotate = False,
                         rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the three-point line
    as specified in Rule 1, Section 7 of the NCAA rule book. These points are
    the men's three-point line after being moved back prior to the 2019-2020
    season

    Returns
    -------
    m_three_pt_lines: a pandas dataframe of the three-point line
    """
    # First, a bit of math is needed to determine the starting and ending
    # angles of the three-point arc, relative to 0 radians. Since in the end,
    # the angle is what matters, the units of measure do not. Inches are easier
    # to use for this calculation. The angle begins 9' 10 3/8" from the
    # interior edge of the endline
    start_x = (9 * 12) + 10 + (3/8)
    
    # However, the rule book describes the arc as having a radius of 22' 1.75"
    # from the center of the basket. The basket's center is 63" away from the
    # interior of the endline, so this must be subtracted from our starting x
    # position to get the starting x position *relative to the center of the
    # basket*
    start_x -= 63
    radius_outer = (22 * 12) + 1.75
    
    # From here, the calculation is relatively straightforward. To determine
    # the angle, the inverse cosine is needed. It will be multiplied by pi
    # so that it can be passed to the create_circle() function
    start_angle_outer = math.acos(start_x / radius_outer) / np.pi
    end_angle_outer = -start_angle_outer
    
    # The same method can be used for the inner angles, however, since the
    # inner radius will be traced from bottom to top, the angle must be
    # negative to start
    radius_inner = (22 * 12) + 1.75 - 2
    start_angle_inner = -math.acos(start_x / radius_inner) / np.pi
    end_angle_inner = -start_angle_inner
    
    # According to the rulebook, the three-point line is 21' 7 7/8" in the
    # corners
    m_three_pt_line = pd.DataFrame({
        'x': [-47],
        'y': [21 + ((7 + (7/8))/12)]
    }).append(
        create.circle(
            center = (-41.75, 0),
            d = 2 * (((22 * 12) + 1.75)/12),
            start = start_angle_outer,
            end = end_angle_outer
        )
    ).append(
        pd.DataFrame({
            'x': [
                -47,
                -47,
                -47 + (((9 * 12) + 10 + (3/8))/12)
            ],
            
            'y': [
                -21 - ((7 + (7/8))/12),
                -21 - ((7 + (7/8))/12) + (2/12),
                -21 - ((7 + (7/8))/12) + (2/12)
            ]
        })
    ).append(
        create.circle(
            center = (-41.75, 0),
            d = 2 * ((((22 * 12) + 1.75)/12) - (2/12)),
            start = start_angle_inner,
            end = end_angle_inner
        )
    ).append(
        pd.DataFrame({
            'x': [
                -47 + (((9 * 12) + 10 + (3/8))/12),
                -47,
                -47
            ],
            
            'y': [
                21 + ((7 + (7/8))/12) - (2/12),
                21 + ((7 + (7/8))/12) - (2/12),
                21 + ((7 + (7/8))/12)
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_court:
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

def w_three_pt_lines(full_court = True, rotate = False,
                         rotation_dir = 'ccw'):
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
            d = 41.5,
            start = -1/2,
            end = 1/2
        )
    ).append(
        pd.DataFrame({
            'x':[-47, -47],
            'y':[20.75, 20.75 - (2/12)]
        })
    ).append(
        create.circle(
            center = (-41.75, 0),
            d = 41.5 - (4/12),
            start = 1/2,
            end = -1/2
        )
    ).append(
        pd.DataFrame({
            'x':[-47, -47],
            'y':[-20.75 + (2/12), -20.75]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_court:
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

def free_throw_circles(full_court = True, rotate = False,
                           rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the free-throw circles
    as specified on the court diagram in the NCAA rule book

    Returns
    -------
    free_throw_circles: a pandas dataframe of the free-throw circle
    """
    # The free-throw circle is 6' in diameter from the center of the free-throw
    # line (exterior)
    free_throw_circle = create.circle(
        center = (-28, 0),
        start = -1/2,
        end = 1/2,
        d = 12
    ).append(
        pd.DataFrame({
            'x':[-28],
            'y':[6]
        })
    ).append(
        create.circle(
            center = (-28, 0),
            start = 1/2,
            end = -1/2,
            d = 12 - (4/12)
        )
    ).append(
        pd.DataFrame({
            'x':[-28],
            'y':[-6]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_court:
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

def backboards(full_court = True, rotate = False, rotation_dir = 'ccw'):
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
    if full_court:
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

def goals(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the goals as specified
    in Rule 1, Sections 14 and 15 of the NCAA rule book

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
    if full_court:
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

def nets(full_court = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the rings as specified
    in Rule 1, Section 14, Article 2 of the NCAA rule book

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
    if full_court:
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