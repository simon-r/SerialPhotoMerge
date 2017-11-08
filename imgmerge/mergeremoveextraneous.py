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

from imgmerge.mergeprocedurevirtual import *

import numpy as np
import sys
import time

try:
    import pycuda.autoinit
    from pycuda import gpuarray
except:
    pass

import scipy.ndimage as ndimage
from imgmerge.readimg import ReadImageBasic
from imgmerge.image import Image
from imgmerge.readimgfactory import ReadImageFarctory


class MergeRemoveExtraneous(MergeProcedureVirtual):

    def __init__(self):
        super().__init__()

    def execute(self):
        self.resulting_image = None
        f_first = True

        resimg = self.images_iterator.read_reference_image()
        shape = resimg.shape

        resimg.image[:] = 2**resimg.color_depth / 2
        avrimg = Image(ishape=shape, dtype=resimg.dtype)
        std = np.zeros(shape[:2], dtype=resimg.dtype) + 2**resimg.color_depth

        dist = np.zeros(shape[:2], dtype=resimg.dtype)
        flags = np.zeros(shape[:2], dtype=np.bool8)

        iter_cnt = 5

        for itr in range(iter_cnt):
            invalid_imgs = []
            img_cnt = 0.0

            for imgarr in self.images_iterator:

                if shape != imgarr.shape:
                    self.images_iterator.discard_image()
                    continue

                img_cnt += 1

                dist[:] = np.sqrt(
                    np.power(resimg.image[:, :, 0] - imgarr.image[:, :, 0], 2) +
                    np.power(resimg.image[:, :, 1] - imgarr.image[:, :, 1], 2) +
                    np.power(resimg.image[:, :, 2] - imgarr.image[:, :, 2], 2))

                ca = time.clock()
                flags[:] = False
                flags[:] = dist[:] < std[:] / np.exp(np.float(itr) / 10.0)

                avrimg.image[flags] = avrimg.image[flags] + imgarr.image[flags]

                flags[:] = np.logical_not(flags)
                avrimg.image[flags] = avrimg.image[flags] + resimg.image[flags]

                cb = time.clock()
                print(cb - ca)

            resimg.image[:] = avrimg.image[:] / img_cnt
            std[:] = 0.0

            for imgarr in self.images_iterator:

                std[:] = (std[:] +
                          (np.power(resimg.image[:, :, 0] - imgarr.image[:, :, 0], 2) +
                           np.power(resimg.image[:, :, 1] - imgarr.image[:, :, 1], 2) +
                           np.power(resimg.image[:, :, 2] - imgarr.image[:, :, 2], 2)))

            std[:] = np.sqrt(std[:] / img_cnt)
            avrimg.image[:] = 0.0

        self.resulting_image = resimg


class MergeRemoveExtraneousCUDA(MergeProcedureVirtual):

    def __init__(self):
        super().__init__()

    def __init_kernel_dist_colors(self):
        self.__kernel_dist_colors =
        """
        __global__ void dist_colors(float *imgarr, float *avrimg, float w=10.0)
        {
            const int i = threadIdx.x;
            dest[i] = a[i] * b[i];
        }
        """

    def execute(self):
        self.resulting_image = None
        f_first = True

        resimg = self.images_iterator.read_reference_image()
        shape = resimg.shape

        resimg.image[:] = 2**resimg.color_depth / 2

        resimg_nda = np.ndarray(shape=resimg.image.shape,
                                dtype=resimg.image.dtype)
        resimg_nda[:] = resimg.image[:]

        resimg_cu = gpuarray.to_gpu(resimg_nda)
        imgarr_cu = gpuarray.to_gpu(resimg_nda)

        avrimg_cu = gpuarray.zeros_like(resimg_cu)
        std_cu = gpuarray.zeros(
            shape[:2], dtype=resimg.dtype) + 2**resimg.color_depth

        dist_cu = gpuarray.zeros(shape[:2], dtype=resimg.dtype)
        flags_cu = gpuarray.zeros(shape[:2], dtype=np.bool)

        iter_cnt = 5

        for itr in range(iter_cnt):
            invalid_imgs = []
            img_cnt = 0.0

            for imgarr in self.images_iterator:

                if shape != imgarr.shape:
                    self.images_iterator.discard_image()
                    continue

                imgarr_cu.set(imgarr.image)
