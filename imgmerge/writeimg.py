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

from matplotlib.image import imsave

try:
    import imageio
    imported_imageio = True
except:
    imported_imageio = False

class WriteImageVirtual( object ):
    def __init__(self):
        self._file_name = None
        
    def set_file_name(self, file_name):
        self._file_name = file_name 
        
    def get_file_name(self):
        return self._file_name
    
    file_name = property(get_file_name, set_file_name )
    
    def write(self, imagearr,  file_name=None):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )

class WriteImageBasic( WriteImageVirtual ):
    def __init__(self):
        super().__init__()
        
    def write(self, imagearr,  file_name=None):
        
        if file_name != None :
            self.file_name = file_name 
        elif self.file_name != None :
            pass
        else :
            raise Exception( " %s , Undefined file name: " % sys._getframe().f_code.co_name )
        
        imagearr.un_normalize() 
        imsave( self.file_name, imagearr.get_uint_array( tdepth=8 ) )


class WriteImageExtended( WriteImageVirtual ):
    def __init__(self):
        super().__init__()
        if not imported_imageio :
            raise Exception( " %s , imageio library is not installed: " % sys._getframe().f_code.co_name )

    def write(self, imagearr,  file_name=None):
        if file_name != None :
            self.file_name = file_name 
        elif self.file_name != None :
            pass
        else :
            raise Exception( " %s , Undefined file name: " % sys._getframe().f_code.co_name )
        
        imagearr.un_normalize()

        imageio.imwrite( file_name, imagearr.image )
        
    