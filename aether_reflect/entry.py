import init
init.init()
import sys
from run_ut import run_ut
from config import get_config
from cpp_code.group import Group
from cpp_code.file import File
from do_file import do_file
import subprocess

import os
def get_files_recursive(dir):
    res=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            res.append(os.path.join(root,file).replace(dir,""))
    return res

def clang_format(dir):
    files=get_files_recursive(dir)
    for file in files:
        subprocess.run(["clang-format","-i",dir+file])
def main():
    if len(sys.argv)==2 and sys.argv[1]=="ut":
        run_ut()
    elif len(sys.argv)==3 and sys.argv[1]=="format":
        clang_format(sys.argv[2])
    elif len(sys.argv)==5:
        input_dir=sys.argv[1]
        output_dir=sys.argv[2]
        variant_header_path=sys.argv[3]
        variant_header_include=sys.argv[4]
        
        root=get_config().root
        input_files=get_files_recursive(input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        group=Group(output_dir)
        for path in input_files:
            file=File.from_obj(do_file(input_dir+"/"+path))
            parent_dir=os.path.dirname(path)
            if not os.path.exists(output_dir+"/"+parent_dir):
                os.makedirs(output_dir+"/"+parent_dir)
            group.add_file(parent_dir+"/"+file.name,file)
        group.write_variant_header_file(variant_header_path)
        for path,file in group.files:
            file.add_include_file_relative(variant_header_include)
        group.write_files()
        clang_format(output_dir)
    else:
        print("invalid args")
        exit()
main()