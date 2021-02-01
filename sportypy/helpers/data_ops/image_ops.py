"""
Functions to manipulate images

@author: Ross Drucker
"""
def rotate(img, rotation_angle = 90, rotation_dir = 'ccw'):
    """
    Rotate an image

    Parameters
    ----------
    img: an instance of class PIL.Image (a logo)
    rotation_angle: an angle (in degrees) to rotate the image
    rotation_dir: the direction in which to rotate the image

    Returns
    -------
    img: an instance of class PIL.Image, but rotated

    """
    if rotation_dir == 'ccw':
        img = img.rotate(rotation_angle)
    else:
        img = img.rotate(-rotation_angle)
        
    return img

def crop(img, rotate = False, rotation_angle = 90, rotation_dir = 'ccw'):
    """
    Crop (and rotate) an image when necessary. This is useful for cropping
    logos so long as they have a square bounding box

    Parameters
    ----------
    img: an instance of class PIL.Image (a logo)
    rotation_angle: an angle (in degrees) to rotate the image
    rotate: a bool indicating whether or not this image needs to be rotated
    rotation_dir: a string indicating which direction to rotate the feature

    Returns
    -------
    img_dict: a dictionary containing two images. 'img_a' will be the left
        half of a non-rotated image, or the lower half of a rotated image,
        and 'img_b' will be the right half of a non-rotated image, or the
        upper half of a rotated image
    """
    # Get the image's dimensions    
    w, h = img.size
    
    # If the image isn't rotated, split the logo in half left to right
    if not rotate:
        # a_box corresponds to the left half of the logo, and b_box to the
        # right half of the logo. The bounding box is measured starting from
        # the top left corner of the ORIGINAL image, and the bounding box
        # tuple is given as (left, top, right, bottom)
        a_box = (0, 0, w/2, h + 1)
        b_box = (w/2, 0, w, h + 1)
    
    # If the image is rotated, first rotate the image the correct direction,
    # then split the log in half top to bottom
    else:
        img = rotate(img, rotation_angle, rotation_dir)
            
        a_box = (0, h/2, w, h + 1)
        b_box = (0, 0, w, h/2)
    
    img_a = img.crop(a_box)
    img_b = img.crop(b_box)
    
    img_dict = {
        'img_a': img_a,
        'img_b': img_b
    }
    
    return img_dict