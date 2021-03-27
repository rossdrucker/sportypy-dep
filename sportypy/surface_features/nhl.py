"""
@author: Ross Drucker
"""
import math
import numpy as np
import pandas as pd

from sportypy.helpers.coordinate_ops import create_shapes as create
from sportypy.helpers.coordinate_ops import transformations as transform

def boards(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the boards as specified
    in Rule 1.3 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    boards: a pandas dataframe of coordinates needed to plot the boards
    """
    boards = pd.DataFrame({
        'x': [
            0
        ],
        
        'y': [
            42.5
        ]
    }).append(
        create.circle(
            center = (-72, 14.5),
            start = .5,
            end = 1,
            d = 56
        )
    ).append(
        pd.DataFrame({
            'x': [
                -100
            ],
            
            'y': [
                0
            ]
        })
    ).append(
        create.circle(
            center = (-72, -14.5),
            start = 1,
            end = 1.5,
            d = 56
        )
    ).append(
        pd.DataFrame({
            'x': [
                0,
                0
            ],
            
            'y': [
                -42.5,
                -42.5 - (2/12)
            ]
        })
    ).append(
        create.circle(
            center = (-72, -14.5),
            start = 1.5,
            end = 1,
            d = 56 + (4/12)
        )
    ).append(
        pd.DataFrame({
            'x': [
                -100 - (2/12)
            ],
            
            'y': [
                0
            ]
        })
    ).append(
        create.circle(
            center = (-72, 14.5),
            start = 1,
            end = .5,
            d = 56 + (4/12)
        )
    ).append(
        pd.DataFrame({
            'x': [
                0,
                0
            ],
            
            'y': [
                42.5 + (2/12),
                42.5
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        boards = boards.append(
            transform.reflect(
                boards,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        boards = transform.rotate(
            boards,
            rotation_dir
        )
        
    return boards

def faceoff_spot(center = (0, 0), full_surf = True, rotate = False,
                 rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the face-off spots as
    specified in Rule 1.9 of the NHL rule book
    
    Parameters
    ----------
    center: a tuple containing the center coordinates of the spot to be drawn
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    spot_dict: a dictionary with keys of 'center' and 'spot', where 'center'
        corresponds to the center coordinates of a face-off spot, and 'spot'
        is a pandas dataframe of coordinates to plot to make a face-off spot
    """
    # Center faceoff spot
    if center == (0, 0):
        # The center face-off spot is 12" in diameter
        spot = create.circle(
            center = (0, 0),
            start = 1/2,
            end = 3/2,
            d = 1
        )
        
        # Reflect the x coordinates over the y axis
        if full_surf:
            spot = create.circle(
                center = (0, 0),
                start = 1/2,
                end = 5/2,
                d = 1
            )
            
        # Rotate the coordinates if necessary
        if rotate:
            spot = transform.rotate(
                spot,
                rotation_dir
            )
        
        spot_dict = {
            'center': center,
            'spot_outer': spot,
            'spot_inner': pd.DataFrame({
                'x': [],
                'y': []
            })
        }
        
        return spot_dict
    
    else:
        # The non-center face-off spots are 2' in diameter, with a 3" gap
        # between the top and bottom of the spot and the strip in the center. 
        # First, find the angle at which to start the trace for the interior
        # of the spot.
        
        # The spot has a radius of 1', and a thickness of 2", so the inner
        # radius is 10". Since there is a 3" gap at theta = 180deg, this
        # indicates that the stripe's curve starts at x = -7" from the center.
        # Using trigonometry, the angle can be computed
        theta = math.asin(7/10) / np.pi
        
        
        # To draw this evenly, it's easiest to create two dataframes: one is
        # the underlying red spot of diameter 2', and the other being the
        # white inner portion described in the rule book. The starting point
        # is found using theta calculated above
        spot_outer = create.circle(
            center = (0, 0),
            start = 0,
            end = 2,
            d = 2
        )
        
        spot_inner = create.circle(
            center = (0, 0),
            start = .5 + theta,
            end = 1.5 - theta,
            d = 2 - (4/12)
        ).append(
            create.circle(
                center = (0, 0),
                start = .5 + theta,
                end = 1.5 - theta,
                d = 2 - (4/12)
            ).iloc[0]
        )
        
        spot_inner = spot_inner.append(
            transform.reflect(
                spot_inner,
                over_y = True
            )
        )
        
        # Rotate the coordinates if necessary
        if rotate:
            spot_outer = transform.rotate(
                spot_outer,
                rotation_dir
            )
            
            spot_inner = transform.rotate(
                spot_inner,
                rotation_dir
            )
        
        spot_outer = transform.translate(
            spot_outer,
            translate_x = center[0],
            translate_y = center[1]
        )
        
        spot_inner = transform.translate(
            spot_inner,
            translate_x = center[0],
            translate_y = center[1]
        )
        
        spot_dict = {
            'center': center,
            'spot_outer': spot_outer,
            'spot_inner': spot_inner
        }
        
        return spot_dict

def faceoff_circle(center = (0, 0), full_surf = True, rotate = False,
                   rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the face-off circles
    as specified in Rule 1.9 of the NHL rule book
    
    Parameters
    ----------
    center: a tuple containing the center coordinates of the spot to be drawn
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    faceoff_circle_dict: a dictionary with keys of 'center' and 'spot', where
        'center' corresponds to the center coordinates of the face-off spot,
        and 'spot' is a pandas dataframe of coordinates needed to plot a
        face-off circle
    """
    # The center circle has no external hash marks, so this circle just needs
    # to be a circle of 2" thickness
    if center == (0, 0):
        faceoff_circle = create.circle(
            center = (0, 0),
            start = .5,
            end = 1.5,
            d = 30
        ).append(
            pd.DataFrame({
                'x': [
                    0,
                    0
                ],
                
                'y': [
                    -15,
                    -15 + (2/12)
                ]
            })
        ).append(
            create.circle(
                center = (0, 0),
                start = 1.5,
                end = .5,
                d = 30 - (4/12)
            )
        ).append(
            pd.DataFrame({
                'x': [
                    0,
                    0
                ],
                
                'y': [
                    15 - (2/12),
                    15
                ]
            })
        )
            
    else:
        # Similar to the method described above, the starting angle to draw the
        # outer ring can be computed. The hash marks are 5' 11" (71") apart on
        # the exterior, so taking where this hash mark meets the circle to be
        # the center, the starting angle is computed as follows
        theta1 = math.asin((35.5/12)/15) / np.pi
        
        # The same process gives the angle to find the point on the interior
        # of the hash mark, which are 5' 7" (67") apart
        theta2 = math.asin((33.5/12)/15) / np.pi
        
        # Since the hash mark will be plotted on the top of the circle, the
        # starting angle will be theta + pi/2
        faceoff_circle = create.circle(
            center = (0, 0),
            start = .5 + theta1,
            end = 1.5 - theta1,
            d = 30
        ).append(
            pd.DataFrame({
                'x': [
                    -35.5/12,
                    -33.5/12,
                ],
                
                'y': [
                    -17,
                    -17
                ]
            })
        ).append(
            create.circle(
                center = (0, 0),
                start = 1.5 - theta2,
                end = 1.5,
                d = 30
            )
        ).append(
            pd.DataFrame({
                'x': [
                    0
                ],
                
                'y': [
                    -15 + (2/12)
                ]
            })
        ).append(
            create.circle(
                center = (0, 0),
                start = 1.5,
                end = .5,
                d = 30 - (4/12)
            )
        ).append(
            pd.DataFrame({
                'x': [
                    0
                ],
                
                'y': [
                    15
                ]
            })
        ).append(
            create.circle(
                center = (0, 0),
                start = .5,
                end = .5 + theta2,
                d = 30
            )
        ).append(
            pd.DataFrame({
                'x': [
                    -33.5/12,
                    -35.5/12,
                ],
                
                'y': [
                    17,
                    17
                ]
            })
        ).append(
            create.circle(
                center = (0, 0),
                start = .5 + theta1,
                end = 1.5 - theta1,
                d = 30
            ).iloc[0]
        )
        
    # If the faceoff circle being drawn is the center circle, and only half
    # the ice is desired, return the semi-circle that is present
    if center == (0, 0) and not full_surf:
        pass
    
    # If the spot is in the neutral zone, there should not be a circle around
    # it
    elif abs(center[0]) == 20:
        faceoff_circle = pd.DataFrame({
            'x': [],
            'y': []
        })
    
    else:
        # In all other cases, the entire circle should be generated, so the
        # current points set needs to be reflected over the y axis
        faceoff_circle = faceoff_circle.append(
            transform.reflect(faceoff_circle, over_y = True)
        )
        
        faceoff_circle = transform.translate(
            faceoff_circle,
            translate_x = center[0],
            translate_y = center[1]
        )
        
        # Rotate the coordinates if necessary. This is more for consistency
        # than necessity as a rotated circle is visually the same
        if rotate:
            faceoff_circle = transform.rotate(
                faceoff_circle,
                rotation_dir
            )
    
    faceoff_circle_dict = {
        'center': center,
        'faceoff_circle': faceoff_circle
    }
    
    return faceoff_circle_dict

def faceoff_lines(center = (0, 0), full_surf = True, rotate = False,
                  rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the face-off spot's
    hash marks as specified in Rule 1.9 of the NHL rule book
    
    Parameters
    ----------
    center: a tuple containing the center coordinates of the spot to be drawn
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    faceoff_line_dict: a dictionary with keys of 'center' and 'faceoff_lines',
        where 'center' corresponds to the center coordinates of the face-off
        spot, and 'faceoff_lines' is a pandas dataframe of coordinates needed
        to plot the hashmarks around a face-off spot
    """
    faceoff_line = pd.DataFrame({
        'x': [
            -2,
            -6,
            -6,
            -2 - (2/12),
            -2 - (2/12),
            -2,
            -2
            
        ],
        
        'y': [
            .75,
            .75,
            .75 + (2/12),
            .75 + (2/12),
            3.75,
            3.75,
            .75
        ]
    })
    
    # At each face-off spot, there are four of these lines. Now that one is
    # created, reflect over the x axis to get a second, then reflect both of
    # those sets of lines over the y axis to get the remaining two
    faceoff_line = faceoff_line.append(
        transform.reflect(faceoff_line, over_y = True)
    )
    faceoff_line = faceoff_line.append(
        transform.reflect(faceoff_line, over_x = True, over_y = True)
    )
    
    faceoff_line = faceoff_line.append(
        transform.reflect(faceoff_line, over_x = True, over_y = False)
    )
    
    # Move the lines to be in the correct positions around the face-off spot
    # centers
    faceoff_line = transform.translate(
        faceoff_line,
        translate_x = center[0],
        translate_y = center[1]
    )
    
    # If the spot is in the neutral zone, there should not be a circle around
    # it
    if abs(center[0]) == 20 or center == (0, 0):
        faceoff_line = pd.DataFrame({
            'x': [],
            'y': []
        })
        
    # Rotate the coordinates if necessary
    if rotate:
        faceoff_line = transform.rotate(
            faceoff_line,
            rotation_dir
        )
    
    faceoff_line_dict = {
        'center': center,
        'faceoff_lines': faceoff_line
    }
    
    return faceoff_line_dict

def referee_crease(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the referee's crease
    as specified in Rule 1.7 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    referee_crease: a pandas dataframe of coordinates needed to plot the
        referee's crease
    """
    # The referee's crease is located at center ice in front of the penalty
    # timekeeper's seat. It is a 2" thick, 10' radius semi-circle
    referee_crease = create.circle(
        center = (0, -42.5),
        start = .5,
        end = 1,
        d = 20
    ).append(
        pd.DataFrame({
            'x': [
                -10 + (2/12)
            ],
            
            'y': [
                -42.5
            ]
        })
    ).append(
        create.circle(
            center = (0, -42.5),
            start = 1,
            end = .5,
            d = 20 - (4/12)
        )
    ).append(
        pd.DataFrame({
            'x': [
                0
            ],
            
            'y': [
                10
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        referee_crease = referee_crease.append(
            transform.reflect(
                referee_crease,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        referee_crease = transform.rotate(
            referee_crease,
            rotation_dir
        )
    
    return referee_crease

def center_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the center line as
    specified in Rule 1.5 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    center_line: a pandas dataframe of coordinates needed to plot the
        center line
    """
    # The center line is a 12" wide line that's centered along y = 0. It spans
    # the width of the playing surface
    center_line = create.rectangle(
        x_min = -.5, x_max = 0,
        y_min = -42.5, y_max = 42.5
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        center_line = center_line.append(
            transform.reflect(
                center_line,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        center_line = transform.rotate(
            center_line,
            rotation_dir
        )
    
    return center_line

def blue_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the blue line as
    specified in Rule 1.7 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    blue_line: a pandas dataframe of coordinates needed to plot the blue line
    """
    # The blue line is a 12" wide line that's 25' (interior) from the center
    # line. It spans the width of the playing surface
    blue_line = create.rectangle(
        x_min = -26, x_max = -25,
        y_min = -42.5, y_max = 42.5
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        blue_line = blue_line.append(
            transform.reflect(
                blue_line,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        blue_line = transform.rotate(
            blue_line,
            rotation_dir
        )
    
    return blue_line
    
def goal_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the goal line as
    specified in Rule 1.7 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    goal_line: a pandas dataframe of coordinates needed to plot the goal line
    """
    # The goal line is a little tricky. It is 11' away from the boards (or 89'
    # from the center), but follows the curvature of the boards in the corner.
    # To get the curvature, a similar calculation to that of the face-off spot
    # interior can be performed
    theta1 = math.asin((17 - (1/12))/28) / np.pi
    theta2 = math.asin((17 + (1/12))/28) / np.pi
    
    goal_line = create.circle(
        center = (-72, 14.5),
        start = .5 + theta1,
        end = .5 + theta2,
        d = 56
    ).append(
        create.circle(
            center = (-72, -14.5),
            start = 1.5 - theta2,
            end = 1.5 - theta1,
            d = 56
        )
    ).append(
        create.circle(
            center = (-72, 14.5),
            start = .5 + theta1,
            end = .5 + theta2,
            d = 56
        ).iloc[0]
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        goal_line = goal_line.append(
            transform.reflect(
                goal_line,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        goal_line = transform.rotate(
            goal_line,
            rotation_dir
        )
    
    return goal_line

def goalkeeper_restricted_area(full_surf = True, rotate = False,
                               rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the goalkeeper's
    restricted area as specified in Rule 1.8 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    goalkeeper_restricted_area: a pandas dataframe of coordinates needed to
        plot the goalkeeper's restricted area
    """
    goalkeeper_restricted_area = pd.DataFrame({
        'x': [
            -100,
            -89 + 1/12,
            -89 + 1/12,
            -100,
            -100,
            -89 - (1/12),
            -89 - (1/12),
            -100,
            -100
        ],
        
        'y': [
            14,
            11,
            -11,
            -14,
            -14 + (2/12),
            -11 + (2/12),
            11 - (2/12),
            14 - (2/12),
            14
        ]
    })
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        goalkeeper_restricted_area = goalkeeper_restricted_area.append(
            transform.reflect(
                goalkeeper_restricted_area,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        goalkeeper_restricted_area = transform.rotate(
            goalkeeper_restricted_area,
            rotation_dir
        )
    
    return goalkeeper_restricted_area

def goal_crease(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the goal crease outline
    and blue inner area as specified in Rule 1.7 of the NHL rule book
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature
    
    Returns
    -------
    goal_crease_dict: a dictionary with keys of 'goal_crease_outline' and
        'goal_crease_inner', where 'goal_crease_outline' is a pandas dataframe
        that corresponds to the coordinates of the red outline of the goal
        crease, and 'goal_crease_inner' is a pandas dataframe of coordinates
        of the boundary of the blue interior of the goal crease
    """
    theta = math.asin(4/6) / np.pi
    
    goal_crease_outline = pd.DataFrame({
        'x': [
            -89 + (1/12),
            -89 + 4.5 + (1/12)
        ],
        
        'y': [
            4,
            4
        ]
    }).append(
        create.circle(
            center = (-89, 0),
            start = theta,
            end = -theta,
            d = 12
        )
    ).append(
        pd.DataFrame({
            'x': [
                -89 + (1/12),
                -89 + (1/12),
                -85 + (1/12),
                -85 + (1/12),
                -85 + (3/12),
                -85 + (3/12)
            ],
            
            'y': [
                -4,
                -4 + (2/12),
                -4 + (2/12),
                -4 + (7/12),
                -4 + (7/12),
                -4 + (2/12)
            ]
        })
    ).append(
        create.circle(
            center = (-89, 0),
            start = -theta,
            end = theta,
            d = 12 - (4/12)
        )
    ).append(
        pd.DataFrame({
            'x': [
                -85 + (3/12),
                -85 + (3/12),
                -85 + (1/12),
                -85 + (1/12),
                -89 + (1/12),
                -89 + (1/12)                
            ],
            
            'y': [
                4 - (2/12),
                4 - (7/12),
                4 - (7/12),
                4 - (2/12),
                4 - (2/12),
                4
            ]
        })
    )
        
    goal_crease_inner = pd.DataFrame({
        'x': [
            -89 + (1/12),
            -85 + (1/12),
            -85 + (1/12),
            -85 + (3/12),
            -85 + (3/12)
        ],
        
        'y': [
            -4 + (2/12),
            -4 + (2/12),
            -4 + (7/12),
            -4 + (7/12),
            -4 + (2/12)
        ]
        }).append(
            create.circle(
                center = (-89, 0),
                start = -theta,
                end = theta,
                d = 12 - (4/12)
            )
    ).append(
        pd.DataFrame({
            'x': [
                -85 + (3/12),
                -85 + (3/12),
                -85 + (1/12),
                -85 + (1/12),
                -89 + (1/12),
                -89 + (1/12)
            ],
            
            'y': [
                4 - (2/12),
                4 - (7/12),
                4 - (7/12),
                4 - (2/12),
                4 - (2/12),
                -4 + (2/12)
            ]
        })
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        goal_crease_outline = goal_crease_outline.append(
            transform.reflect(
                goal_crease_outline,
                over_y = True
            )
        )
        
        goal_crease_inner = goal_crease_inner.append(
            transform.reflect(
                goal_crease_inner,
                over_y = True
            )
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        goal_crease_outline = transform.rotate(
            goal_crease_outline,
            rotation_dir
        )
        
        goal_crease_inner = transform.rotate(
            goal_crease_inner,
            rotation_dir
        )
    
    goal_crease_dict = {
        'goal_crease_outline': goal_crease_outline,
        'goal_crease_inner': goal_crease_inner
    }
    
    return goal_crease_dict