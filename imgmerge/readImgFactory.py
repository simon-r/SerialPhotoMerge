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

from imgmerge.readImg import ReadImageBasic, ReadImageRaw, ReadImageArray


class ReadImageFarctory(object):

    def __init__(self):
        self._img_reads = [ReadImageBasic()]
        try:
            self._img_reads.append(ReadImageRaw())
        except:
            print("!!Warning!! RAW formats are not supported; you must install rawpy (https://github.com/neothemachine/rawpy) for the support!")

        self._default_reader = self._img_reads[0]
        self._force_dafault = False

    def get_default_reader(self):
        return self._default_reader

    def set_default_reader(self, def_r):
        self._default_reader = def_r

    default_reader = property(get_default_reader, set_default_reader)

    def get_force_default(self):
        return self._force_dafault

    def set_force_dafault(self, f):
        self._force_dafault = f

    force_default = property(get_force_default, set_force_dafault)

    def get_readimage(self, file_name=None):
        if not file_name or self.force_default:
            self._default_reader.file_name = file_name
            return self._default_reader

        for reader in self._img_reads:
            if reader.is_supported(file_name):
                reader.file_name = file_name
                return reader

        raise Exception("%s : Image file format not supported." %
                        sys._getframe().f_code.co_name)
        return None


class ReadStoreImageFactory(ReadImageFarctory):

    def __init__(self):
        super().__init__()
        self.__img_dict = dict()

    def get_readimage(self, file_name=None):

        ria = ReadImageArray()

        if file_name in self.__img_dict.keys():
            ria.set_array(self.__img_dict[file_name])
            return ria

        chosed_reader = None

        if not file_name or self.force_default:
            self._default_reader.file_name = file_name
            chosed_reader = self._default_reader

        unsupprted_format = True

        if not chosed_reader:
            for reader in self._img_reads:
                if reader.is_supported(file_name):
                    reader.file_name = file_name
                    chosed_reader = reader
                    unsupprted_format = False
                    break

        if unsupprted_format:
            raise Exception("%s : Image file format not supported." %
                            sys._getframe().f_code.co_name)

        rgb = chosed_reader.read()
        
        self.__img_dict[file_name] = chosed_reader.raw

        ria.set_array(self.__img_dict[file_name])

        return ria
