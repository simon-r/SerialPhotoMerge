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

def estimate_color_depth( image_array ):
    if image_array.dtype == np.dtype('uint8') :
        return 8
    elif image_array.dtype == np.dtype('uint16') :
        return 16
    elif image_array.dtype == np.dtype('uint32') :
        return 32
    
    mx = np.max( image_array )
    mn = np.min( image_array )

    if mn < 0.0 :
        raise Exception( "%s : Invalid image_array, negatives values not allowed" % sys._getframe().f_code.co_name )

    if mx < 2**8 :
        return 8
    elif mx < 2**16 :
        return 16
    elif mx < 2**32 :
        return 32


class Image(object):
    def __init__(self, color_depth=8, ishape=(0,0), color_mode="RGB", dtype= np.float32 ):
        self._dtype = dtype
        self._color_depth = color_depth 
        self._color_mode = "RGB"

        if len( ishape ) == 2:
            if color_mode == "RGB":
                ishape = ishape + (3,)
            elif color_mode == "RGBA":
                ishape = ishape + (4,)
            elif color_mode == "MONO":
                ishape = ishape
        elif len( ishape ) == 3:
            if ishape[2] not in [3,4]:
                raise Exception()
            elif ishape[2]==3:
                self._color_mode = "RGB"
            else:
                self._color_mode = "RGBA"

        
        self._image = np.zeros( ishape , dtype=self._dtype )
        
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

    def get_uint_array(self):

        if self.color_depth == 8 :
            idtype = np.uint8
        elif self.color_depth == 16 :
            idtype = np.uint16
        else :
            idtype = np.uint8

        return np.array( self.image , dtype=idtype )

    def to_white(self):
        self._image[:] = self.dtype( 2**self.color_depth - 1 )

    def to_black(self):
        self._image[:] = 0.0

    def get_color_depth(self):
        return self._color_depth
    
    def set_color_depth(self, cd):
        self._color_depth = cd 
        
    color_depth = property( get_color_depth, set_color_depth )
    
    def set_image_extended(self, image_array, color_depth=None, idtype=np.float32 ):
        if not color_depth:
            self.color_depth = estimate_color_depth( image_array )
        else:
            self.color_depth = color_depth

        self.dtype = idtype
        self._image = np.array( image_array , dtype=self.dtype )

    def set_image(self, image_array ):
        
        self.dtype = np.float32

        if image_array.dtype == np.dtype('uint8') :
            self.color_depth = 8
        elif image_array.dtype == np.dtype('uint16') :
            self.color_depth = 16
        elif image_array.dtype == np.dtype('uint32') :
            self.color_depth = 32
        else:
            self.color_depth = estimate_color_depth( image_array )

        self._image = np.array( image_array , dtype=self.dtype )

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
    
    
    