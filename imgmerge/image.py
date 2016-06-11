# ImageMerge
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

class Image(object):
    def __init__(self):
        self._dtype = np.float32
        self._image = np.array( [] , dtype=self._dtype )
        self._color_depth = 8 
        self._color_mode = "RGB"
        
        self._normalized = False 
    
    def set_dtype( self, dtype):
        self._dtype = dtype
        
    def get_dtype(self):
        return self._dtype
    
    dtype = property( get_dtype, set_dtype)    
    
    def get_shape(self):
        return self.image.shape
    
    shape = property( get_shape )
    
    def resize(self, size):

        if len(size) == 3 :
            if size[2] == 3 :
                self._color_mode = "RGB"
            elif size[2] == 4 :
                self._color_mode = "RGBA"
        elif self._color_mode == "RGB" :
            isize = size + (3,)
        elif self._color_mode == "RGBA" :
            isize = size + (4,)

        np.resize( self._image , isize )

    def to_white(self):
        self._image[:] = self.dtype( 2**self.color_depth - 1 )

    def to_black(self):
        self._image[:] = 0.0

    def get_color_depth(self):
        return self._color_depth
    
    def set_color_depth(self, cd):
        self._color_depth = cd 
        
    color_depth = property( get_color_depth, set_color_depth )
    
    def set_image(self, image_array ):
        self._image = np.array( image_array , dtype=self.dtype )
        
        if image_array.dtype == np.dtype('uint8') :
            self._color_depth = 8
        elif image_array.dtype == np.dtype('uint16') :
            self._color_depth = 16

    def get_image(self):
        return self._image
        
    image = property(get_image, set_image )
    
    def add(self,other):
        self.image[:] = self.image[:] + other.image[:]

    def normalize(self):
        if not self._normalized :
            self.image[:] = self.image[:] / (2.0**self.color_depth-1.0)
            
        self._normalized = True
    
    def un_normalize(self):
        if self._normalized :
            self.image[:] = self.image[:] * (2.0**self.color_depth-1.0)
            
        self._normalized = False 
    
    
    