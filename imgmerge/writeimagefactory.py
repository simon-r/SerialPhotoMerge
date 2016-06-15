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

from imgmerge.writeimg import *

class WriteImageFactory( object ):
    def __init__(self):
        self._default_wi = None
        self._chosen_wi = None

    def force_default(self, wi):
        self._default_wi = wi
    
    def remove_default(self):
        self._default_wi = None

    def set_image_parameters(self, format="jpg", color_depth=8, lossy=True, **kwargs ):
        if format in [ "jpg", "jpeg" ]:
            self._chosen_wi = WriteImageBasic()
            return 
        elif format in [ "png" ]:
            pass
        elif format in [ "tif", "tiff" ]:
            pass
    
    def get_write_image(self):
        if self._default_wi :
            return self._default_wi