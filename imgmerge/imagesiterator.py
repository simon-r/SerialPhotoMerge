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
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theS
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from imgmerge.image import Image

from imgmerge.image import Image
from imgmerge.readimgfactory import ReadImageFarctory

class ImagesIterator( object ):
    def __init__(self):
        self._imgs_list=[]
        self._read_img_factory = ReadImageFarctory()
        self._image = None
        self._index = 0 
        self._refimage = None
        self._reference_image = None # file name

    def __iter__(self):
        if self._reference_image:
            self._imgs_list = list( filter( (self._reference_image).__ne__, self._imgs_list ))
            self._imgs_list = [self._reference_image] + self._imgs_list
        
        self._index = 0

        return self

    def __next__(self):
        if self._index >= len( self._imgs_list ) :
            raise StopIteration

        while True:
            try:
                readimg = self._read_img_factory.get_readimage( self._imgs_list[self._index] )
                self._image = readimg.read()
                break
            except:
                self._index += 1

        self._index += 1
        return self._image

    def from_images_list(self, imgs_list):
        self._imgs_list=[]
        for el in imgs_list:
            if not isinstance(el, str):
                continue
            self._imgs_list.append(el)

    def from_directory(self, in_dir):
        self._imgs_list = os.listdir(dn)

    def set_reference_image(self, file_name ):
        self._refimage = file_name

    def get_reference_image(self):
        return self._refimage

    reference_image = property(get_reference_image, set_reference_image )

    def get_read_image_factory(self):
        return self._read_img_factory

    def set_read_image_factory(self, rif):
        self._read_img_factory = rif

    read_image_factory = property(get_read_image_factory, set_read_image_factory)

    def get_image_class(self):
        return self._image

    image = property( get_image_class )
        