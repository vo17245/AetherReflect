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
import os


def to_abs_path(path):
    return os.path.abspath(path)

def get_standard_unix_path(path):
    res=to_abs_path(path)
    res=res.replace("\\","/")
    while res.find("//")!=-1:
        res=res.replace("//","/")
    return res
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
    if len(sys.argv)==6:
        input_dir=get_standard_unix_path(sys.argv[1])
        output_dir=get_standard_unix_path(sys.argv[2])
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        variant_header_filename=sys.argv[3]
        variant_type_full_name=sys.argv[4]
        meta_type_full_name=sys.argv[5]
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
        group.write_variant_header_file(f"{output_dir}/{variant_header_filename}",variant_type_full_name)
        for path,file in group.files:
            path=get_standard_unix_path(path)
            t=path.replace(input_dir,"")
            arr=t.split("/")
            arr_t=[]
            for item in arr:
                if item=="":
                    continue
                arr_t.append(item)
            arr=arr_t
            d=""
            if len(arr)>=2:
                for i in range(len(arr)-2):
                    d+="../"
            file.add_include_file_relative(d+f"{variant_header_filename}")
        group.write_files(variant_type_full_name,meta_type_full_name)
        clang_format(output_dir)
    else:
        print("invalid args")
        exit()
main()