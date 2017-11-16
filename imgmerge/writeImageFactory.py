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

from imgmerge.writeImg import *


def get_16bit_support():
    return [".tif", ".tiff"]


class WriteImageFactory(object):

    def __init__(self):
        self._default_wi = None
        self._chosen_wi = None

    def force_default(self, wi):
        self._default_wi = wi

    def remove_default(self):
        self._default_wi = None

    def set_image_parameters(self, format=".jpg", color_depth=8, lossy=True, **kwargs):

        if not color_depth:
            color_depth = 8

        try:
            if format in [".jpg", ".jpeg"]:
                self._chosen_wi = WriteImageBasic()
            elif format in [".png"]:
                if color_depth == 8 and len(kwargs) == 0:
                    self._chosen_wi = WriteImageBasic()
                elif color_depth in [8] or len(kwargs) > 0:
                    self._chosen_wi = WriteImageExtended()
            elif format in [".tif", ".tiff"]:
                if color_depth == 8 and len(kwargs) == 0:
                    self._chosen_wi = WriteImageBasic()
                elif color_depth in [8, 16] or len(kwargs) > 0:
                    self._chosen_wi = WriteImageExtended()
        except UnsupportedWriterException as exc:
            print("!!Warning!! 16bit tiff format is not supported; you must install imageio (https://github.com/imageio/imageio) for the support!")
            print("!! The resulting image will be written in 8bit")
            self._chosen_wi = WriteImageBasic()
            color_depth = 8

        if len(kwargs) > 0:
            self._chosen_wi.image_fmt_arguments = kwargs

        self._chosen_wi.out_color_depth = color_depth

    def get_write_image(self):
        if self._default_wi:
            return self._default_wi
        else:
            return self._chosen_wi
