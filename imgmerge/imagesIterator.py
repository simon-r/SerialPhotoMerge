# Serial Photo Merge
# Copyright (C) 2017  Simone Riva mail: simone.rva {at} gmail {dot} com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See theS
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import random

from imgmerge.image import Image
from imgmerge.readImgFactory import ReadImageFarctory


class ImagesIterator(object):

    def __init__(self):
        self._imgs_list = []
        self._read_img_factory = ReadImageFarctory()
        self._image = None
        self._index = 0
        self._in_dir = None
        self._reference_image = None  # file name
        self._discarded_files = []

    def __iter__(self):

        self.clean_files_list()

        if self._reference_image:
            self._imgs_list = list(
                filter((self._reference_image).__ne__, self._imgs_list))
            self._imgs_list = [self._reference_image] + self._imgs_list

        self._index = 0

        return self

    def __next__(self):
        if self._index >= len(self._imgs_list):
            raise StopIteration

        while True:
            try:
                readImg = self._read_img_factory.get_readimage(
                    self._imgs_list[self._index])
                self._image = readImg.read()
                break
            except:
                self._index += 1
                if self._index >= len(self._imgs_list):
                    raise StopIteration

        self._index += 1
        return self._image

    def from_images_list(self, imgs_list):
        self._imgs_list = []
        for el in imgs_list:
            if not isinstance(el, str):
                continue
            self._imgs_list.append(el)

    def from_directory(self, in_dir):
        self._imgs_list = []
        self._in_dir = in_dir
        for file_name in os.listdir(in_dir):
            self._imgs_list.append(os.path.join(
                os.path.abspath(in_dir), file_name))

    def get_images_list(self):
        return self._imgs_list

    images_list = property(fget=get_images_list)

    def set_reference_image(self, file_name):
        if self._in_dir:
            self._reference_image = os.path.join(
                os.path.abspath(self._in_dir), file_name)
        else:
            self._reference_image = file_name

    def get_reference_image(self):
        return self._reference_image

    reference_image = property(get_reference_image, set_reference_image)

    def read_reference_image(self):
        if self.reference_image:
            readImg = self._read_img_factory.get_readimage(
                self.reference_image)
            image = readImg.read() 
            return image

        index = 0
        while True:
            try:
                readImg = self._read_img_factory.get_readimage(
                    self._imgs_list[index])
                image = readImg.read()
                return image
            except:
                index += 1
                if index >= len(self._imgs_list):
                    return None

    def discard_file(self, fr=None):
        if not fr:
            self._discarded_files.append(self._index)
        else:
            self._discarded_files.append(fr)

    def clean_files_list(self):
        for e in self._discarded_files:
            if isinstance(e, int):
                del self._imgs_list[e]
            elif isinstance(e, str):
                self._imgs_list.remove(e)

        self._discarded_files = []

    def get_read_image_factory(self):
        return self._read_img_factory

    def set_read_image_factory(self, rif):
        self._read_img_factory = rif

    read_image_factory = property(
        get_read_image_factory, set_read_image_factory)

    def get_image_class(self):
        return self._image

    image_class = property(get_image_class)


class ImagesRandomIterator(ImagesIterator):

    def __init__(self):
        super().__init__()
        self._el_dict = {}
        self._first = True
        self._key_ref = None

    def __iter__(self):
        self.clean_files_list()
        self._first = True
        k = 0

        self._el_dict = {}
        self._key_ref = None

        for im in self.images_list:
            self._el_dict[k] = im
            k += 1
            if self.reference_image == im:
                self._key_ref = k

        return self

    def __next__(self):
        if len(self._el_dict) == 0:
            raise StopIteration

        if self._first and self.reference_image:
            f_name = self._el_dict[self._key_ref]
            del self._el_dict[self._key_ref]

            readImg = self._read_img_factory.get_readimage(f_name)
            self._image = readImg.read()
            return self._image

        self._first = False

        while True:
            try:
                k = random.choice(list(self._el_dict.keys()))
                f_name = self._el_dict[k]
                #print( f_name )
                del self._el_dict[k]

                readImg = self._read_img_factory.get_readimage(f_name)
                self._image = readImg.read()
                break
            except:
                if len(self._el_dict) == 0:
                    raise StopIteration

        return self._image
