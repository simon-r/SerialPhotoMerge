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

import os

from imgmerge.writeImg import WriteImageBasic
from imgmerge.writeImageFactory import WriteImageFactory


class ImageMerge(object):

    def __init__(self):
        self._imgs = []
        self._merger = None

    def set_merge_procedure(self, merger):
        self._merger = merger

    def execute_merge(self):
        self._merger.images_list = self._imgs
        self._merger.execute()

    def add_image(self, path, file_name, img_params=None):
        img_path = os.path.join(os.path.abspath(path), file_name)
        self._imgs.append(img_path)

    def get_resulting_image(self):
        return self._merger.get_resulting_image()

    def save_resulting_image(self, file_name, wi_factory):
        imgw = wi_factory.get_write_image()
        #imgw = WriteImageBasic()
        imgw.file_name = file_name
        imgw.write(self._merger.get_resulting_image())
