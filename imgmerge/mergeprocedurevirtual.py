# Serial Photo Merge
# Copyright (C) 2012  Simone Riva mail: simone.rva {at} gmail {dot} com
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import sys

import scipy.ndimage as ndimage
from imgmerge.readimg import ReadImageBasic
from imgmerge.image import Image
from imgmerge.readimgfactory import ReadImageFarctory

#import matplotlib.pyplot as plt

def get_dtype(color_bits):
    if color_bits == 8 :
        return np.uint8
    elif color_bits == 16 :
        return np.uint16

class MergeProcedureVirtual( object ):
    def __init__(self):
        self._img_list = None
        self._resimg = None
        self._refimage = None
        self._read_img_factory = ReadImageFarctory()

    def set_images_list(self, img_list):
        self._img_list = img_list 
    
    def get_images_list(self):
        return self._img_list
    
    images_list = property( get_images_list , set_images_list )

    def set_reference_image(self, file_name ):
        self._refimage = file_name

    def get_reference_image(self):
        return self._refimage

    reference_image = property(get_reference_image, set_reference_image )

    def get_read_image_factory(self):
        return self._read_img_factory

    def set_read_image_factory(self, rif):
        self._read_img_factory = rif

    read_image_factory = property(get_read_image_factory, set_read_image_factory)

    def execute(self):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def get_resulting_image(self):
        return self._resimg
    
    def set_resulting_image(self, resarr):
        self._resimg = resarr
        
    resulting_image = property( get_resulting_image, set_resulting_image )



        
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
