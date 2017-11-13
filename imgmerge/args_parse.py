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

import argparse


def args_parse():
    desc = """ 
    Serial Photo Merge is a python3 tool for computing the average of an unlimited number of images. ImageMerge (ideally) do not load in memory all the images so it can work with a very big numbers of images. It is useful for creating a daylight very long exposure photography.
    """

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-d", "--dir_in",
                        action="store",
                        dest="dir_in",
                        help="The directory that stores the input images")

    parser.add_argument("-o", "--out_image",
                        action="store",
                        dest="out_image",
                        help="The output image")

    parser.add_argument("-ocd", "--out_color_depth",
                        action="store",
                        choices=["8", "16", "auto"],
                        default="auto",
                        dest="out_color_depth",
                        help="Color depth of the output image. "
                        "At the moment 16bit is supported only by tif")

    parser.add_argument("-a", "--algorithm",
                        action="store",
                        choices=["avg", "average", "re", "remove_extraneous"],
                        default="avg",
                        dest="algorithm",
                        help="Algorithm applied on the images: "
                        "avg|average: Average of the images "
                        "re|remove_extraneous: remove extraneous elements")

    parser.add_argument("-c", "--cuda",
                        action="store_true",
                        dest="cuda",
                        help="Uses CUDA if possible")

    parser.add_argument("-sm", "--store",
                        action="store_true",
                        dest="store_images",
                        help="In the algorithm ""remove extraneous"" load all images in RAM")                        

    return parser.parse_args()
