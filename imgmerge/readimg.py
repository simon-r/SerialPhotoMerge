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
import sys

import scipy.ndimage as ndimage

class ReadImage( object ):
    def __init__(self):
        self._dtype = np.float32
        self._file_name = None
    
    def set_file_name(self, file_name):
        self._file_name = file_name 
        
    def get_file_name(self):
        return self._file_name
    
    def set_dtype(self, dtype):
        self._dtype = dtype
        
    def get_dtype(self):
        return self._dtype
    
    dtype = property( get_dtype, set_dtype)
    
    file_name = property(get_file_name, set_file_name )
    
    def read(self, file_name=None):
        
        if file_name != None :
            self._file_name = file_name 
        elif self._file_name != None :
            pass
        else :
            raise Exception( " %s , Undefined file name: " % sys._getframe().f_code.co_name )
        
        img_rgb = np.array( ndimage.imread( self._file_name ) , dtype=self._dtype )
        
        return img_rgb
    
    
    
    
    
    
    
    
    
    