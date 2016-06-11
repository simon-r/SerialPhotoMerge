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
from imgmerge.readimg import ReadImageBasic
from imgmerge.image import Image

#import matplotlib.pyplot as plt

def get_dtype(color_bits):
    if color_bits == 8 :
        return np.uint8
    elif color_bits == 16 :
        return np.uint16

class MergeProcedure( object ):
    def __init__(self):
        self._img_list = None
        self._resimg = None
        self._refimage = None

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

    def execute(self):
        NotImplementedError(" %s : is virutal and must be overridden." % sys._getframe().f_code.co_name )
    
    def get_resulting_image(self):
        return self._resimg
    
    def set_resulting_image(self, resarr):
        self._resimg = resarr
        
    resulting_image = property( get_resulting_image, set_resulting_image )



class NpMergeProcedure( MergeProcedure ):
    def __init__(self):
        super().__init__()
        self._resimg = None
    
    def execute(self):
        
        readimg = ReadImageBasic()
        
        color_bit = 8 
        
        self.resulting_image = None

        if len( self.images_list ) == 0 :
            raise Exception( " %s , Empty List" % sys._getframe().f_code.co_name )
        
        if self.reference_image:
            self.images_list = list(filter(( self.reference_image ).__ne__, self.images_list ))
            self.images_list = [self.reference_image] + self.images_list

        while True :
            try :
                readimg.file_name = self.images_list[0] ;
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
            
            readimg.file_name = img
            try :
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
        
        
class MergeRemoveUnwanted( MergeProcedure ):
    def __init__(self):
        pass
    
    def execute(self):
        readimg = ReadImageBasic()
        
        if len( self.images_list ) == 0 :
            raise Exception( " %s , Empty List" % sys._getframe().f_code.co_name )
    
        while True :
            try :
                readimg.file_name = self.images_list[0] ;
                resimg = readimg.read()
                break 
            except :
                self.images_list.pop(0)    
    
        shape = resimg.shape
    
        resimg[:] = 128.0 
        avrimg = np.zeros( shape , dtype=readimg.dtype )
        std = np.zeros( shape[:2] , dtype=readimg.dtype ) + 256.0
        
        dist = np.zeros( shape[:2] , dtype=readimg.dtype ) 
        flags = np.zeros( shape[:2] , dtype=np.bool8 )
    
        iter_cnt = 10 
    
        for itr in range( iter_cnt ) :
            invalid_imgs = []
            img_cnt = 0.0
        
            for img in self.images_list :
                
                readimg.file_name = img
                
                try :
                    imgarr = readimg.read()
                    
                    if shape != imgarr.shape :
                        invalid_imgs.append(img)
                        continue 
                    
                    img_cnt += 1.0
                    
                    dist[:] = np.sqrt( 
                                np.power( resimg[:,:,0] - imgarr[:,:,0] , 2 ) + 
                                np.power( resimg[:,:,1] - imgarr[:,:,1] , 2 ) + 
                                np.power( resimg[:,:,2] - imgarr[:,:,2] , 2 ) )
                    
                    flags[:] = False
                    flags[:] = dist[:] < std[:] / np.exp( np.float( itr ) / 10.0 )
                    
                    avrimg[flags] = avrimg[flags] + imgarr[flags]
                    
                    flags[:] = np.logical_not( flags ) 
                    avrimg[flags] = avrimg[flags] + resimg[flags]
                    
                except :
                    invalid_imgs.append(img) 
                
            resimg[:] = avrimg[:] / img_cnt
            
            std[:] = 0.0 
            
            for inv in invalid_imgs :
                self.images_list.remove(inv)
            
            for img in self.images_list :
                
                readimg.file_name = img
                imgarr = readimg.read()
                
                std[:] = ( std[:] +
                           ( np.power( resimg[:,:,0] - imgarr[:,:,0] , 2 ) + 
                             np.power( resimg[:,:,1] - imgarr[:,:,1] , 2 ) + 
                             np.power( resimg[:,:,2] - imgarr[:,:,2] , 2 ) ) )   
                
            std[:] = np.sqrt( std[:] / img_cnt )
            avrimg[:] = 0.0 
        
        self.resulting_image = np.array( resimg[:] , dtype=np.uint8 )
            
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
