from typing import Any

import numpy as np
from PIL import Image
import exifread
import os

from numpy import ndarray, dtype
from numpy._core.multiarray import scalar


class ImageUtils:
    @staticmethod
    def _get_exif_orientation(image_path):
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
        # Exifread uses 'Image Orientation' to store the orientation data
        orientation_tag = 'Image Orientation'
        if orientation_tag in tags:
            # Convert the value to an integer
            orientation_value = tags[orientation_tag].values[0]
            # Return the orientation value
            return orientation_value
        else:
            # No orientation tag found, return a default value
            return 1

    @staticmethod
    def _apply_rotation(image, orientation):       
        """
        Applies rotation to the image based on the EXIF orientation.
        """
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)
        return image

    @staticmethod
    def check_image_format(image_input_format: str): 
        # "rgb" 3 channels Red Green Blue image format.
        # "bgr" 3 channels Blue Green Red image format.
        # "rgba" 4 channels Red Green Blue for colors and an Alpha channel.
        if not image_input_format.lower() in ['rgb', 'bgr', 'rgba']:            
            raise ValueError(f"Invalid image format: {image_input_format}")
    
    @staticmethod
    def check_image_array(image_array:np.ndarray, image_input_format: str): 
        ImageUtils.check_image_format(image_input_format)        
        input_format = image_input_format.lower()        
        if image_array.dtype != np.uint8:
            raise ValueError("Image array must be of type np.uint8")
        if input_format == 'rgba':
            if len(image_array.shape) != 3 or image_array.shape[2] != 4:
                raise ValueError("Image array must have 4 channels for rgba format")
        else:
            if len(image_array.shape) != 3 or image_array.shape[2] != 3:
                raise ValueError("Image array must be a 3D array with 3 channels")
    
    @staticmethod
    def image_path_to_numpy_array(image_path:str,input_format:str='',apply_rotation: bool = True) -> list[
        ndarray[tuple[Any, ...], dtype[scalar]] | str]:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        # open file
        input_format = input_format.lower()
        image = Image.open(image_path)
        # read pixel format 
        pixel_format = image.mode.lower()

        # if caller specified a specfic format that is different from the pixel format, convert it
        if input_format != '' and ImageUtils.check_image_format(input_format):
            if pixel_format != input_format:
                image = image.convert(input_format.upper())
                pixel_format = input_format
        else:
            # check if the pixel format is supported
            ImageUtils.check_image_format(pixel_format)

        if apply_rotation:
            rotation = ImageUtils._get_exif_orientation(image_path)
            image=ImageUtils._apply_rotation(image,rotation)

        return [np.array(image),pixel_format]
        

