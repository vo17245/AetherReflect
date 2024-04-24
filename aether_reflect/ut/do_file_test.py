from do_file import do_file
from config import get_config
from cpp_code.file import File
def run():
    path=get_config().root+"/test_res/example.py"
    output_path=get_config().root+"/test_output/example.h"
    cpp_file_obj=do_file(path)
    cpp_file=File.from_obj(cpp_file_obj)
    with open(output_path,"w",encoding="utf-8") as f:
        f.write(cpp_file.to_string())
        
