"""
State Mercator Projection SVG: https://www.mccurley.org/svg/data/states.svg
Credit: Kevin McCurley

@author: Ross Drucker
"""
import pandas as pd

from util import get_soup

def clean_coord_pairs(pair_str):
    coord_strings_list = pair_str.split(',')
    coords = [float(s) for s in coord_strings_list]
    return coords

def get_state_name(tag):
    state_name = tag.get('statename')
    return state_name

def get_state_abbr(tag):
    state_abbr = tag.get('id')
    return state_abbr

def get_state_centroid(tag):
    centroid_tag = tag.findChildren('centroid')[0]
    clat = float(centroid_tag.findChildren('lat')[0].contents[0])
    clon = float(centroid_tag.findChildren('lon')[0].contents[0])
    
    return clat, clon
    
def get_coords(tag):
    # Get the points from the SVG image
    polygon = tag.findChildren('polygon')[0].get('points').strip()
    
    # Split the points on a space character, as these are how they are stored
    # in the SVG image
    coord_pairs = polygon.split(' ')
    
    # Make a list of lists of the coordinate pairs
    coords_list = [clean_coord_pairs(pair_str) for pair_str in coord_pairs]
    
    # Convert to a data frame
    coords = pd.DataFrame(coords_list, columns = ['x', 'y'])
    
    # Get the state information
    state_name = get_state_name(tag)
    state_abbr = get_state_abbr(tag)
    clat, clon = get_state_centroid(tag)
    
    # Add the name and abbreviation to the dataframe for future subsetting
    coords['state_name'] = state_name.upper()
    coords['state_abbr'] = state_abbr.upper()
    
    # Translate the state's coordinates to locate the centroid at (0, 0)
    coords['x1'] = coords['x'] - clat
    coords['y1'] = coords['y'] - clon
    
    return coords

def get_state_shapes():
    url = 'https://www.mccurley.org/svg/data/states.svg'
    
    soup = get_soup(url)
    
    state_tags = soup.find_all('g', attrs = {'statename': True})
    
    full_coords = pd.DataFrame()
    
    for tag in state_tags:
        new_coords = get_coords(tag)
        
        full_coords = pd.concat([full_coords, new_coords])
        
    return full_coords
        