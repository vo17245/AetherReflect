from cpp_code.file import File


class Group:
    def __init__(self,dir_path):
        self.dir_path=dir_path
        self.files:list[str,File]=[]
    def add_file(self,path,file):
        self.files.append([path,file])
    def create_variant_file(self):
        all_field_type=[]
        for path,file in self.files:
            for struct in file.structs:
                for field in struct.fields:
                    all_field_type.append(field.type)
        all_field_type=list(set(all_field_type))
        variant_str="using ReflectVariant=std::variant<"
        
        for i in range(len(all_field_type)):
            if i==0:
                variant_str+=f"{all_field_type[i]}"
            else:
                variant_str+=f",{all_field_type[i]}"
        variant_str+=">;"
        
        all_include=""
        for path,file in self.files:
            for include in file.include_files:
                all_include+=f"{include}\n"
            for block in file.include_blocks:
                all_include+=f"{block}\n"
        all_include_lines=all_include.splitlines()
        all_include_lines=list(set(all_include_lines))
        all_include="\n".join(all_include_lines)
        header="""#pragma once
        #include <variant>
        """
        
        
        return f"""{header}
    {all_include}
    namespace Aether{{
    template<typename T>
    struct Reflect{{}};
    {variant_str}
    }}"""
    def write_files(self):
        for path,file in self.files:
            with open(f"{self.dir_path}/{path}","w",encoding="utf-8") as f:
                f.write(file.to_string())
        
        
    def write_variant_header_file(self,path):
        variant_path=f"{self.dir_path}/reflect_variant.h"
        with open(variant_path,"w",encoding="utf-8") as f:
            f.write(self.create_variant_file())