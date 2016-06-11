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
import os

import scipy.ndimage as ndimage
from imgmerge.image import Image

try:
    import rawpy
    imported_rawpy = True
except:
    imported_rawpy = False

class ReadImageVirtual( object ):
    def __init__(self):
        self._dtype = np.float32
        self._file_name = None
        self._supported_formats = []
    
    def set_file_name( self, file_name):
        self._file_name = file_name 
        
    def get_file_name(self):
        return self._file_name
    
    def set_dtype( self, dtype):
        self._dtype = dtype
        
    def get_dtype(self):
        return self._dtype
    
    def get_supported_formats(self):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def is_supported(self, file_name):
        foo, file_extension = os.path.splitext(file_name)

        if file_extension.lower() in self._supported_formats :
            return True
        else :
            return False
            
    def _add_supported_formats(self, fmts):
        self._supported_formats = self._supported_formats + fmts 
    
    dtype = property( get_dtype, set_dtype)
    
    file_name = property( get_file_name, set_file_name )
    
    supported_formats = property( get_supported_formats )
    
    def read(self, file_name ):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name ) 
    
    
class ReadImageBasic( ReadImageVirtual ):
    def __init__(self):
        ReadImageVirtual.__init__(self)
        ReadImageVirtual._add_supported_formats(self, [ '.jpg' , '.jpeg' , '.png' , '.tiff' ] ) 
                  
    def read(self, file_name=None):
        
        if file_name != None :
            self._file_name = file_name 
        elif self._file_name != None :
            pass
        else :
            raise Exception( " %s , Undefined file name: " % sys._getframe().f_code.co_name )
        
        img_rgb = Image( color_depth=8 )

        img_rgb.image = np.array( ndimage.imread( self._file_name ) , dtype=img_rgb.dtype )       

        return img_rgb 
    
    
class ReadImageRaw( ReadImageVirtual ):
    def __init__(self):
        
        ReadImageVirtual.__init__(self)
        if not imported_rawpy :
            raise Exception( " %s , RAWPY library not supported: " % sys._getframe().f_code.co_name )

        raw_str = """       
            .3fr,
            .ari, .arw,
            .bay,
            .crw, .cr2,
            .cap,
            .data, .dcs, .dcr, .dng,
            .drf,
            .eip, .erf,
            .fff,
            .iiq,
            .k25, .kdc,
            .mdc, .mef, .mos, .mrw,
            .nef, .nrw,
            .obm, .orf,
            .pef, .ptx, .pxn,
            .r3d, .raf, .raw, .rwl, .rw2, .rwz,
            .sr2, .srf, .srw,
            .tif,
            .x3f
            """.replace(" ","").replace("\n","")
       
        raw_lst = raw_str.split( "," )
       
        ReadImageVirtual._add_supported_formats(self, raw_lst )
        
        
    def read(self, file_name=None):
        
        if file_name != None :
            self._file_name = file_name 
        elif self._file_name != None :
            pass
        else :
            raise Exception( " %s , Undefined file name: " % sys._getframe().f_code.co_name )

        rgb = Image( color_depth=16 )

        with rawpy.imread ( file_name ) as raw:
            rgb = np.array( raw.postprocess( output_bps=16 ) , dtype=rgb.dtype )
            
        return rgb 

    
    
    
    
    
    
    
    
    
    