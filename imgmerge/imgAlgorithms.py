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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
import sys

from imgmerge.image import Image


class ImageAlgorithm(object):

    def __init__(self):
        pass

    def set_target_image(self, img):
        self._target_img = img

    def get_target_image(self):
        return self._target_img

    targer_image = property(get_target_image, set_target_image)

    def set_area(self, area):
        self._area = area

    def get_area(self):
        return self._area

    area = property(get_area, set_area)

    def execute(self):
        pass


class PairImagesAgorithm(ImageAlgorithm):

    def __init__(self):
        super().__init__()

    def set_reference_image(self, img):
        self._ref_img = img

    def get_reference_image(self):
        return self._ref_img

    reference_image = property(get_reference_image, set_reference_image)


class AlignImages(PairImagesAgorithm):

    def __init__(self):
        super().__init__()
