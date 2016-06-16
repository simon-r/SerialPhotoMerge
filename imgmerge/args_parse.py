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

import argparse

def args_parse():
    desc = "" 
    desc =  desc + ""

    parser = argparse.ArgumentParser( description=desc  )

    parser.add_argument("-d", "--dir_in",
        action="store",
        dest="dir_in",
        help="")

    parser.add_argument("-o", "--out_image",
        action="store",
        dest="out_image",
        help="")  

    parser.add_argument("-ocd", "--out_color_depth",
        action="store",
        choices=["8", "16", "auto"],
        default="auto",
        dest="out_color_depth",
        help="")  

    parser.add_argument("-a", "--algorithm",
        action="store",
        choices=["avg", "average", "re", "remove_extraneous"],
        default="avg",
        dest="algorithm",
        help="")

    return parser.parse_args()       