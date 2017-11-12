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
    from pycuda.compiler import SourceModule
    import pycuda.driver as drv
    import pycuda.cumath as cumath
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
        self.__init_kernel_dist_colors()
        self.__init_kernel_std()

    def __init_kernel_dist_colors(self):
        self.__kernel_dist_colors = """
        __global__ void dist_colors(float *imgarr,
                                    float *resimg,
                                    float *avrimg,
                                    float *std,
                                    int size_x, int size_y,
                                    int itr, float w=10.0)
        {
            int x = threadIdx.x + blockIdx.x * blockDim.x;
            int y = threadIdx.y + blockIdx.y * blockDim.y;
            int offset = x + y * blockDim.x * gridDim.x;

            if (offset < size_x * size_y) {
                int ia_red = 3*offset ;
                int ia_green = 3*offset + 1;
                int ia_blue = 3*offset + 2;

                float dist;

                dist = sqrtf(
                            powf( resimg[ia_red] - imgarr[ia_red], 2.0) +
                            powf( resimg[ia_green] - imgarr[ia_green], 2.0) +
                            powf( resimg[ia_blue] - imgarr[ia_blue], 2.0));

                bool flag = false;

                if(dist < std[offset] / expf(itr / w)){
                    flag = true;
                }

                if(flag){
                    avrimg[ia_red] = avrimg[ia_red] + imgarr[ia_red];
                    avrimg[ia_green] = avrimg[ia_green] + imgarr[ia_green];
                    avrimg[ia_blue] = avrimg[ia_blue] + imgarr[ia_blue];
                } else {
                    avrimg[ia_red] = avrimg[ia_red] + resimg[ia_red];
                    avrimg[ia_green] = avrimg[ia_green] + resimg[ia_green];
                    avrimg[ia_blue] = avrimg[ia_blue] + resimg[ia_blue];
                }
            }
        }
        """

    def __init_kernel_std(self):
        self.__kernel_std = """
        __global__ void img_merge_std(float *imgarr,
                            float *resimg,
                            float *std,
                            int size_x, int size_y)
        {
            int x = threadIdx.x + blockIdx.x * blockDim.x;
            int y = threadIdx.y + blockIdx.y * blockDim.y;
            int offset = x + y * blockDim.x * gridDim.x;

            if (offset < size_x * size_y) {
                int ia_red = 3*offset ;
                int ia_green = 3*offset + 1;
                int ia_blue = 3*offset + 2;

                std[offset] = std[offset] +
                                powf( resimg[ia_red] - imgarr[ia_red], 2.0) +
                                powf( resimg[ia_green] - imgarr[ia_green], 2.0) +
                                powf( resimg[ia_blue] - imgarr[ia_blue], 2.0) ;
            }
        }
        """

    def execute(self):
        f_first = True

        resimg = self.images_iterator.read_reference_image()
        self.resulting_image = self.images_iterator.read_reference_image()

        shape = resimg.shape

        resimg.image[:] = 2**resimg.color_depth / 2

        resimg_nda = np.ndarray(shape=resimg.image.shape,
                                dtype=resimg.image.dtype)
        resimg_nda[:] = resimg.image[:]

        resimg_cu = gpuarray.to_gpu(resimg_nda)
        imgarr_cu = gpuarray.to_gpu(resimg_nda)

        avrimg_cu = gpuarray.zeros_like(resimg_cu)

        std_cu = gpuarray.zeros(shape[:2], dtype=resimg.dtype)

        std_cu.fill(np.float32(2**resimg.color_depth))

        dist_cu = gpuarray.zeros(shape[:2], dtype=resimg.dtype)
        flags_cu = gpuarray.zeros(shape[:2], dtype=np.bool)

        iter_cnt = 5

        print(shape)
        th_x = 32
        th_y = 32

        blk_x = int(shape[0] / th_x) + 1
        blk_y = int(shape[1] / th_y) + 1

        grid_im = (blk_x, blk_y, 1)
        block_im = (th_x, th_y, 1)

        print(block_im)
        print(grid_im)

        mod_dist_colors = SourceModule(self.__kernel_dist_colors)
        mod_std = SourceModule(self.__kernel_std)

        dist_colors = mod_dist_colors.get_function("dist_colors")
        img_merge_std = mod_std.get_function("img_merge_std")

        for itr in range(iter_cnt):
            invalid_imgs = []
            img_cnt = 0.0

            for imgarr in self.images_iterator:

                if shape != imgarr.shape:
                    self.images_iterator.discard_image()
                    continue

                ca = time.clock()
                img_cnt += 1
                imgarr_cu.set(imgarr.image)

                dist_colors(imgarr_cu,
                            resimg_cu,
                            avrimg_cu,
                            std_cu,
                            np.int32(shape[0]), np.int32(shape[1]),
                            np.int32(itr), np.float32(10.0),
                            block=block_im, grid=grid_im)

                cb = time.clock()
                print("clock: %1.4f" % (cb - ca))

            resimg_cu = avrimg_cu[:] / np.float32(img_cnt)
            std_cu.fill(0.0)

            for imgarr in self.images_iterator:
                imgarr_cu.set(imgarr.image)
                img_merge_std(imgarr_cu,
                              resimg_cu,
                              std_cu,
                              np.int32(shape[0]), np.int32(shape[1]),
                              block=block_im, grid=grid_im)

            std_cu /= np.float32(img_cnt)
            cumath.sqrt(std_cu, out=std_cu)

            avrimg_cu.fill(0.0)

        self.resulting_image.image = np.array(resimg_cu.get())
