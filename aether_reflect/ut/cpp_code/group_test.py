from cpp_code.group import Group

from cpp_code.file import File
from config import get_config
from do_file import do_file
import os
def run():
    root=get_config().root
    output_dir=root+"/test_output/group_test"
    input_files=[
        root+"/test_res/example.py",
        root+"/test_res/example1.py"
    ]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    group=Group(output_dir)
    for path in input_files:
        file=File.from_obj(do_file(path))
        group.add_file(file.name,file)
    group.write_files()
    
    