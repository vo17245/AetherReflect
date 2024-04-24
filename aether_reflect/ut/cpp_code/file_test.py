from cpp_code.struct import Struct, Field
from cpp_code.file import File
from config import get_config
import os
def run():
    output_file_path=get_config().root+"/test_output/test.h"
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))
    tag_component=Struct("::Aether::TagComponent","ECS Tag Component")
    tag_component.add_field(Field("tag","::std::string","Tag"))
    tag_component.add_constructor("""\
TagComponent(const std::string& _tag):tag(_tag){}\
""")
    file=File("test.h")
    file.add_struct(tag_component)
    file.add_include_file("string")
    with open(output_file_path,"w") as f:
        f.write(file.to_string())