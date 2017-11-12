
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
import sys

from imgmerge.imagemerge import ImageMerge
from imgmerge.mergeremoveextraneous import MergeRemoveExtraneous, MergeRemoveExtraneousCUDA
from imgmerge.mergeaverageimage import MergeAverageImage, MergeAverageImageCUDA
from imgmerge.args_parse import args_parse
from imgmerge.writeimagefactory import WriteImageFactory, get_16bit_support
from imgmerge.imagesiterator import ImagesIterator, ImagesRandomIterator
from imgmerge.readimgfactory import ReadStoreImageFactory


def main():

    options = args_parse()

    if options.dir_in:
        dn = options.dir_in
    else:
        raise Exception()

    wif = WriteImageFactory()

    img_itr = ImagesIterator()

    merge_procedure = None
    if options.algorithm in ["avg", "average"]:
        if options.cuda:
            merge_procedure = MergeAverageImageCUDA()
            print("CUDA")
        else:
            merge_procedure = MergeAverageImage()

    elif options.algorithm in ["re", "remove_extraneous"]:
        if options.cuda:
            merge_procedure = MergeRemoveExtraneousCUDA()
            print("CUDA")
        else:
            merge_procedure = MergeRemoveExtraneous()
        img_itr = ImagesRandomIterator()

        #merge_procedure.read_image_factory = ReadStoreImageFactory()

    dr = os.listdir(dn)

    img_itr.from_directory(dn)
    merge_procedure.images_iterator = img_itr

    mrg = ImageMerge()

    for fn in dr:
        print(fn)
        mrg.add_image(dn, fn)

    mrg.set_merge_procedure(merge_procedure)
    mrg.execute_merge()

    if options.out_image:
        out_image = options.out_image
    else:
        out_image = "/tmp/out_merge.jpg"

    foo, file_extension = os.path.splitext(out_image)
    file_extension = file_extension.lower()

    if options.out_color_depth == "auto":
        if mrg.get_resulting_image().color_depth == 16 and file_extension in get_16bit_support():
            out_color_depth = 16
        else:
            out_color_depth = 8
    else:
        out_color_depth = int(options.out_color_depth)

    wif.set_image_parameters(format=file_extension,
                             color_depth=out_color_depth)
    mrg.save_resulting_image(out_image, wif)


if __name__ == '__main__':
    main()
