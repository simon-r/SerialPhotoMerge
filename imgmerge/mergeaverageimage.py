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
    

    def execute(self): ##### new version
        self.resulting_image = None
        f_first = True 

        img_cnt = 0.0
        for itr_img in self.images_iterator :

            img_cnt += 1.0

            if f_first:
               self.resulting_image = itr_img
               f_first = False
               continue

            if itr_img.shape != self.resulting_image.shape:
               img_cnt -= 1.0
               continue 

            self.resulting_image.add( itr_img )

        self.resulting_image.image[:] = self.resulting_image.image[:] / img_cnt

        