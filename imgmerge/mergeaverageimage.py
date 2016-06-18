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

from imgmerge.mergeprocedurevirtual import *

import numpy as np
import sys

import scipy.ndimage as ndimage
from imgmerge.readimg import ReadImageBasic
from imgmerge.image import Image
from imgmerge.readimgfactory import ReadImageFarctory

class MergeAverageImage( MergeProcedureVirtual ):
    def __init__(self):
        super().__init__()
        #self._resimg = None
    

    def execute_new(self): ##### new version
        self.resulting_image = None
        f_first = True 

        img_cnt = 0.0
        for itr_img in self.images_iterator :

            img_cnt += 1.0

            if f_first:
               self.resulting_image = itr_img.image_class
               f_first = False
               continue

            read_image = itr_img.image_class

            if read_image.shape != self.resulting_image.shape:
               img_cnt -= 1.0
               continue 

            self.resulting_image.add( read_image )

        self.resulting_image.image[:] = self.resulting_image.image[:] / img_cnt

    def execute(self):
        
        readimg = None
        
        self.resulting_image = None

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
        
        img_cnt = 1.0 
        
        f_first = True
        invalid_imgs = []
        
        for img in self.images_list :
            
            if f_first :
                f_first = False 
                continue 
            
            try :
                readimg = self.read_image_factory.get_readimage( img )
                imgarr = readimg.read()
                                
                if imgarr.color_depth != resimg.color_depth :
                    raise Exception() 
                
                # discard image if the shape is not equivalent!
                if resimg.shape != imgarr.shape :
                    raise Exception() 
                 
                resimg.add( imgarr )
                img_cnt += 1.0 
                
                #print( imgarr.shape )
            except :
                invalid_imgs.append(img)
        
        resimg.image[:] = resimg.image[:] / img_cnt 
        
        self.resulting_image = resimg
                
        return invalid_imgs
        