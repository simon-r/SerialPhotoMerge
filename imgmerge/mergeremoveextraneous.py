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

from imgmerge.mergeprocedurevirtual import *

import numpy as np
import sys

import scipy.ndimage as ndimage
from imgmerge.readimg import ReadImageBasic
from imgmerge.image import Image
from imgmerge.readimgfactory import ReadImageFarctory


class MergeRemoveExtraneous( MergeProcedureVirtual ):
    def __init__(self):
        super().__init__()
    
    def execute(self):
        readimg = None
        
        if len( self.images_list ) == 0 :
            raise Exception( " %s , Empty List" % sys._getframe().f_code.co_name )
    
        if self.reference_image:
            self.images_list = list(filter(( self.reference_image ).__ne__, self.images_list ))
            self.images_list = [self.reference_image] + self.images_list

        while True :
            try :
                readimg = self.read_image_factory.get_readimage( self.images_list[0] )
                resimg = readimg.read()
                break 
            except :
                self.images_list.pop(0)    
    
        shape = resimg.shape
    
        resimg.image[:] = 2**resimg.color_depth / 2 
        avrimg = Image( ishape=shape , dtype=readimg.dtype )
        std = np.zeros( shape[:2] , dtype=readimg.dtype ) + 2**resimg.color_depth
        
        dist = np.zeros( shape[:2] , dtype=readimg.dtype ) 
        flags = np.zeros( shape[:2] , dtype=np.bool8 )
    
        iter_cnt = 5 
    
        for itr in range( iter_cnt ) :
            invalid_imgs = []
            img_cnt = 0.0
        
            for img in self.images_list :
                try :
                    readimg = self.read_image_factory.get_readimage( img )
                    imgarr = readimg.read()
                    
                    if shape != imgarr.shape :
                        invalid_imgs.append(img)
                        continue 
                    
                    img_cnt += 1.0
                    
                    dist[:] = np.sqrt( 
                                np.power( resimg.image[:,:,0] - imgarr.image[:,:,0] , 2 ) + 
                                np.power( resimg.image[:,:,1] - imgarr.image[:,:,1] , 2 ) + 
                                np.power( resimg.image[:,:,2] - imgarr.image[:,:,2] , 2 ) )
                    
                    flags[:] = False
                    flags[:] = dist[:] < std[:] / np.exp( np.float( itr ) / 10.0 )
                    
                    avrimg.image[flags] = avrimg.image[flags] + imgarr.image[flags]
                    
                    flags[:] = np.logical_not( flags ) 
                    avrimg.image[flags] = avrimg.image[flags] + resimg.image[flags]
                    
                except :
                    invalid_imgs.append(img) 
                
            resimg.image[:] = avrimg.image[:] / img_cnt
            
            std[:] = 0.0 
            
            for inv in invalid_imgs :
                self.images_list.remove(inv)
            
            for img in self.images_list :
                
                readimg = self.read_image_factory.get_readimage( img )
                imgarr = readimg.read()
                
                std[:] = ( std[:] +
                           ( np.power( resimg.image[:,:,0] - imgarr.image[:,:,0] , 2 ) + 
                             np.power( resimg.image[:,:,1] - imgarr.image[:,:,1] , 2 ) + 
                             np.power( resimg.image[:,:,2] - imgarr.image[:,:,2] , 2 ) ) )   
                
            std[:] = np.sqrt( std[:] / img_cnt )
            avrimg.image[:] = 0.0 
        
        self.resulting_image = resimg
            
   