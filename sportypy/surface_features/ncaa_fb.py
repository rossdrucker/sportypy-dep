"""
@author: Ross Drucker
"""
import os
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm

from helpers.coordinate_ops import create_shapes as create
from helpers.coordinate_ops import transformations as transform

def endline_sideline(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    end line and sideline as specified in the field diagram of the NCAA rule
    book (Appendix D)
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    endline_sideline: a pandas dataframe of the goal line
    """
    # The sidelines and end lines must be a solid white border, 6' wide along
    # the endlines, and 6' wide along the sidelines. The length of the field
    # is 100 yards, or 360' (interior on the inside of the goal lines), and
    # the sidelines connect with the end lines 10 yards (30') behind the
    # interior edge of the goal line. The field is 160' wide (interior)
    endline_sideline = pd.DataFrame({
        'x': [
            0,
            -180,
            -180,
            0,
            0,
            -186,
            -186,
            0,
            0
        ],
        
        'y': [
            -80,
            -80,
            80,
            80,
            86,
            86,
            -86,
            -86,
            -80
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
        
def goal_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    goal line as specified in the field diagram of the NCAA rule book(Appendix
    D)
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    goal_line: a pandas dataframe of the goal line
    """
    # The interior measurement between goal lines is 100 yards, or 300'. So,
    # taking the center of the field to be (0, 0), each goal line must be 150'
    # away from this point. Goal lines have thickness of 8", extending back
    # into the endzone, and extend across the width of the field (which totals
    # 160' across)
    goal_line = create.rectangle(
        x_min = -150 - (8/12), x_max = -150,
        y_min = -80, y_max = 80
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        goal_line = goal_line.append(
            transform.reflect(goal_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        goal_line = transform.rotate(
            goal_line,
            rotation_dir
        )
    
    return goal_line

def yard_markings(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    line markings at 5-yard intervals as specified in the field diagram of the
    NCAA rule book (Appendix D)
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    yard_line_dict: a dictionary of the lines of the field, and the coordinates
        required to plot them
    """
    # The lines are to be placed 8" from the interior of the sidelines, and be
    # 4" thick. At 5-yard intervals across the field, the lines should stretch
    # the width of the field, with a 2' long by 4" wide hash 60' from the 
    # interior of each boundary. At 1-yard intervals between these markings at
    # 5-yard intervals, a 2' tall by 4" wide marker should be placed 4" from
    # the interior of the sideline as well as 60' from the interior of the
    # sideline (and extending back towards the sideline). The field is being
    # constructed from left to right, and the right-side lines can be computed
    # via reflection, so only the left-side points and half the 50 yard line
    # are needed
    yardages = np.arange(-49, 1)
    
    yard_line_dict = dict()
    
    for yardage in yardages:
        if yardage == 0:
            # This is the 50 yard line. Only half the line is needed, since the
            # other half will be created via reflection
            yard_line = pd.DataFrame({
                'x': [
                    # Start 4" from the sideline
                    (3 * yardage) - (2/12),
                    
                    # Lower inbound line marker
                    (3 * yardage) - (2/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12),
                    
                    # Upper inbound line marker
                    (3 * yardage) - (2/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12),
                    
                    # Top
                    (3 * yardage) - (2/12),
                    
                    # Crossover
                    0,
                    
                    # Return to bottom
                    0,
                    
                    # Return to start
                    (3 * yardage) - (2/12)
                ],
                
                'y': [
                    # Start 4" from the sideline
                    -80 + (4/12),
                    
                    # Lower inbound line marker
                    -20,
                    -20,
                    -20 + (4/12),
                    -20 + (4/12),
                    
                    # Upper inbound line marker
                    20 - (4/12),
                    20 - (4/12),
                    20,
                    20,
                    
                    # Top
                    80 - (8/12),
                    
                    # Crossover
                    80 - (8/12),
                    
                    # Return to bottom
                    -80 + (4/12),
                    
                    # Return to start
                    -80 + (4/12),
                ]
            })
            
            yard_line_dict[f'yard_line_{50 + yardage}'] = yard_line
        
        elif yardage % 5 == 0:
            # At 5-yard intervals, the line should stretch the width of the
            # field, with the inbound line marker 60 from the interior of
            # the sideline boundary
            yard_line = pd.DataFrame({
                'x': [
                    # Start 4" from the sideline
                    (3 * yardage) - (2/12),
                    
                    # Lower inbound line marker
                    (3 * yardage) - (2/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12),
                    
                    # Upper inbound line marker
                    (3 * yardage) - (2/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12) - (10/12),
                    (3 * yardage) - (2/12),
                    
                    # Top
                    (3 * yardage) - (2/12),
                    
                    # Crossover
                    (3 * yardage) + (2/12),
                    
                    # Upper inbound line marker
                    (3 * yardage) + (2/12),
                    (3 * yardage) + (2/12) + (10/12),
                    (3 * yardage) + (2/12) + (10/12),
                    (3 * yardage) + (2/12),
                    
                    # Lower inbound line marker
                    (3 * yardage) + (2/12),
                    (3 * yardage) + (2/12) + (10/12),
                    (3 * yardage) + (2/12) + (10/12),
                    (3 * yardage) + (2/12),
                    
                    # Return to bottom
                    (3 * yardage) + (2/12),
                    
                    # Return to start
                    (3 * yardage) - (2/12)
                ],
                
                'y': [
                    # Start 4" from the sideline
                    -80 + (4/12),
                    
                    # Lower inbound line marker
                    -20,
                    -20,
                    -20 + (4/12),
                    -20 + (4/12),
                    
                    # Upper inbound line marker
                    20 - (4/12),
                    20 - (4/12),
                    20,
                    20,
                    
                    # Top
                    80 - (8/12),
                    
                    # Crossover
                    80 - (8/12),
                    
                    # Upper inbound line marker
                    20,
                    20,
                    20 - (4/12),
                    20 - (4/12),
                    
                    # Lower inbound line marker
                    -20 + (4/12),
                    -20 + (4/12),
                    -20,
                    -20,
                    
                    # Return to bottom
                    -80 + (8/12),
                    
                    # Return to start
                    -80 + (4/12),
                ]
            })
            
            yard_line_dict[f'yard_line_{50 + yardage}'] = yard_line
            
        else:
            # At 1-yard intervals, the line should be 2' long. The line should
            # appear at the bottom (b) and top (t) of the field inside the 6'
            # wide boundary, and also appear at 70'9" from the nearest boundary
            # and extending from this point towards that boundary (l and u)
            yard_line_b = create.rectangle(
                x_min = (3 * yardage) - (2/12), x_max = (3 * yardage) + (2/12),
                y_min = -80 + (4/12), y_max = -78 + (4/12)
            )
            
            yard_line_t = transform.reflect(
                yard_line_b,
                over_x = True,
                over_y = False
            )
            
            yard_line_l = create.rectangle(
                x_min = (3 * yardage) - (2/12), x_max = (3 * yardage) + (2/12),
                y_min = -22, y_max = -20
            )
            
            yard_line_u = transform.reflect(
                yard_line_l,
                over_x = True,
                over_y = False
            )
            
            yard_line_dict[f'yard_line_{50 + yardage}_b'] = yard_line_b
            yard_line_dict[f'yard_line_{50 + yardage}_t'] = yard_line_t
            yard_line_dict[f'yard_line_{50 + yardage}_l'] = yard_line_l
            yard_line_dict[f'yard_line_{50 + yardage}_u'] = yard_line_u
            
        
    # Reflect the x coordinates over the y axis
    if full_surf:
        for yard_line_no, yard_line_coords in yard_line_dict.items():
            yard_line_dict[yard_line_no] = pd.concat([
                yard_line_coords,
                pd.DataFrame({
                    'x': -1 * yard_line_coords['x'],
                    'y': yard_line_coords['y']
                })
            ])
    
    # Rotate the coordinates if necessary
    if rotate:
        for yard_line_no, yard_line_coords in yard_line_dict.items():
            yard_line_dict[yard_line_no] = transform.rotate(
                yard_line_coords,
                rotation_dir
            )
    
    return yard_line_dict

def try_line(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate the dataframe for the points that comprise the bounding box of the
    try line as specified in the field diagram of the NCAA rule book (Appendix
    D)
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    try_line: a pandas dataframe of the goal line
    """
    try_line = create.rectangle(
        x_min = -141 - (2/12), x_max = -141 + (2/12),
        y_min = -1, y_max = 1
    )
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        try_line = try_line.append(
            transform.reflect(try_line, over_y = True)
        )
    
    # Rotate the coordinates if necessary
    if rotate:
        try_line = transform.rotate(
            try_line,
            rotation_dir
        )
    
    return try_line

def directional_arrows(full_surf = True, rotate = False, rotation_dir = 'ccw'):
    """
    Generate a dictionary for the points that comprise the directional arrrows
    that are located at every 10-yard interval as described in the NCAA rule
    book (Appendix D)
    
    Parameters
    ----------
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    directional_arrows_dict: a dictionary of the directional arrows, and the
        coordinates required to plot them
    """
    # The arrow has two sides of 36", and one side of 18". The Pythagorean
    # Theorem can be used to determine the height (using half the length of
    # the base, which in this case is 18")
    arrow_width = np.sqrt(((36/12) ** 2) - ((9/12) ** 2))
    
    # The arrows only occur every 10 yards, but not at the 50 yard line
    arrow_yardages = np.arange(-40, 0, 10)
    
    # The output dictionary
    directional_arrows_dict = dict()
    
    # Create the arrows
    for yardage in arrow_yardages:
        arrow_lower = pd.DataFrame({
            'x': [
                # The numbers are 1' from the outer edge of the yard line,
                # which is 2" wide. The number itself is 4' wide, and the
                # number is 6" off the outside edge of the number
                (3 * yardage) - (2/12) - 5.5,
                (3 * yardage) - (2/12) - 5.5,
                (3 * yardage) - (2/12) - 5.5 - arrow_width,
                (3 * yardage) - (2/12) - 5.5
            ],
            
            'y': [
                # The bottom of the numbers must be 12 yards (36') off the
                # interior of the sideline. The number itself is then 6' tall,
                # and the top tip of the arrow is 15" below this line
                -53 - (15/12),
                -53 - (15/12) - (18/12),
                -53 - (15/12) - (9/12),
                -53 - (15/12)
            ]
        })
        
        arrow_upper = transform.reflect(
            arrow_lower,
            over_x = True,
            over_y = False
        )
        
        directional_arrows_dict[f'{50 + yardage}_arrow_l'] = arrow_lower
        directional_arrows_dict[f'{50 + yardage}_arrow_u'] = arrow_upper
    
    # Reflect the x coordinates over the y axis
    if full_surf:
        for directional_arrow, arrow_coords in directional_arrows_dict.items():
            directional_arrows_dict[directional_arrow] = pd.concat([
                arrow_coords,
                pd.DataFrame({
                    'x': -1 * arrow_coords['x'],
                    'y': arrow_coords['y']
                })
            ])
    
    # Rotate the coordinates if necessary
    if rotate:
        for directional_arrow, arrow_coords in directional_arrows_dict.items():
            directional_arrows_dict[directional_arrow] = transform.rotate(
                arrow_coords,
                rotation_dir
            )
    
    return directional_arrows_dict

def field_numbers(ax, full_surf = True, rotate = False):
    """
    Plot the yardage numbers every 10 yards on the field
    
    Parameters
    ----------
    ax: a matplotlib Axes object on which to add the field numbers
    full_surf: a bool indicating whether or not this feature is needed for a
        full-surface representation
    rotate: a bool indicating whether or not this feature needs to be rotated

    Returns
    -------
    ax: a matplotlib Axes object containing the field numbers
    """
    number_font_fpath = os.path.join('data', 'fonts', 'NCAA', 'clarenbd.ttf')
    number_font = fm.FontProperties(fname = number_font_fpath)
    
    # The numbers only occur every 10 yards
    marked_yardages = np.arange(-40, 1, 10)
    
    for yardage in marked_yardages:
        if not rotate:
            if not full_surf:
                if (3 * yardage) - 5 - (2/12) < 0:
                    ax.text(
                        (3 * yardage) - 5 - (2/12),
                        -53,
                        str(yardage + 50)[0],
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                    ax.text(
                        (3 * yardage) - 5 - (2/12),
                        59,
                        str(yardage + 50)[1],
                        rotation = 180,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                if (3 * yardage) + 1 + (2/12) < 0:
                    ax.text(
                        (3 * yardage) + 1 + (2/12),
                        -53,
                        str(yardage + 50)[1],
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                    ax.text(
                        (3 * yardage) + 1 + (2/12),
                        59,
                        str(yardage + 50)[0],
                        rotation = 180,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
            
            else:
                ax.text(
                    (3 * yardage) - 5 - (2/12),
                    -53,
                    str(yardage + 50)[0],
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (3 * yardage) - 5 - (2/12),
                    59,
                    str(yardage + 50)[1],
                    rotation = 180,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (3 * yardage) + 1 + (2/12),
                    -53,
                    str(yardage + 50)[1],
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                    
                ax.text(
                    (3 * yardage) + 1 + (2/12),
                    59,
                    str(yardage + 50)[0],
                    rotation = 180,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (-3 * yardage) - 5 - (2/12),
                    -53,
                    str(yardage + 50)[0],
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (-3 * yardage) + 1 + (2/12),
                    -53,
                    str(yardage + 50)[1],
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (-3 * yardage) - 5 - (2/12),
                    59,
                    str(yardage + 50)[1],
                    rotation = 180,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    (-3 * yardage) + 1 + (2/12),
                    59,
                    str(yardage + 50)[0],
                    rotation = 180,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
            
        else:
            if not full_surf:
                if (3 * yardage) + 5 - (2/12) < 0:
                    ax.text(
                        -53,
                        (3 * yardage) + 5 - (2/12),
                        str(yardage + 50)[0],
                        rotation = -90,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                    ax.text(
                        59,
                        (3 * yardage) + 5 - (2/12),
                        str(yardage + 50)[1],
                        rotation = 90,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                if (3 * yardage) - 1 + (2/12) < 0:
                    ax.text(
                        -53,
                        (3 * yardage) - 1 + (2/12),
                        str(yardage + 50)[1],
                        rotation = -90,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
                    
                    ax.text(
                        59,
                        (3 * yardage) - 1 + (2/12),
                        str(yardage + 50)[0],
                        rotation = 90,
                        fontsize = 54,
                        color = '#ffffff',
                        verticalalignment = 'top',
                        fontproperties = number_font
                    )
            else:
                ax.text(
                    -53,
                    (3 * yardage) + 5 - (2/12),
                    str(yardage + 50)[0],
                    rotation = -90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    59,
                    (3 * yardage) + 5 - (2/12),
                    str(yardage + 50)[1],
                    rotation = 90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    -53,
                    (3 * yardage) - 1 + (2/12),
                    str(yardage + 50)[1],
                    rotation = -90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    59,
                    (3 * yardage) - 1 + (2/12),
                    str(yardage + 50)[0],
                    rotation = 90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    -53,
                    (-3 * yardage) + 5 - (2/12),
                    str(yardage + 50)[0],
                    rotation = -90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    -53,
                    (-3 * yardage) - 1 + (2/12),
                    str(yardage + 50)[1],
                    rotation = -90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    59,
                    (-3 * yardage) + 5 - (2/12),
                    str(yardage + 50)[1],
                    rotation = 90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
                
                ax.text(
                    59,
                    (-3 * yardage) - 1 + (2/12),
                    str(yardage + 50)[0],
                    rotation = 90,
                    fontsize = 42,
                    color = '#ffffff',
                    verticalalignment = 'top',
                    fontproperties = number_font
                )
    
    return ax    