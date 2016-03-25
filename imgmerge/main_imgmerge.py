
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

import os
import sys

from imgmerge.imagemerge import ImageMerge
from imgmerge.mergeprocedure import NpMergeProcedure

def main():
    
    if len( sys.argv ) == 2 :
        dn = sys.argv[1]
        res_file = "res.jpg"
    elif len( sys.argv ) == 3 :
        dn = sys.argv[1]
        res_file = sys.argv[2]
    else :
        print( "bye" )
        return 1 
    
    dr = os.listdir(dn)
    
    mrg = ImageMerge()
    
    for fn in dr:
        print(fn)
        mrg.add_image( dn , fn)
    
    mrg.set_merge_procedure( NpMergeProcedure() )
    mrg.execute_merge()
    
    mrg.save_resulting_image( res_file )
    
    
if __name__ == '__main__':
    main()
        
