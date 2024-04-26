from cpp_code.file import File


class Group:
    def __init__(self,dir_path):
        self.dir_path=dir_path
        self.files:list[str,File]=[]
    def add_file(self,path,file):
        self.files.append([path,file])
    def create_variant_file(self,variant_type_full_name):
        all_field_type=[]
        for path,file in self.files:
            for struct in file.structs:
                for field in struct.fields:
                    all_field_type.append(field.type)
        all_field_type=list(set(all_field_type))

        name_arr=variant_type_full_name.split("::")
        name_arr_t=[]
        for item in name_arr:
            if item=="":
                continue
            name_arr_t.append(item)
        name_arr=name_arr_t
        namespace_begin=""
        namespace_end=""
        if len(name_arr)>1:
            for i in range(len(name_arr)-1) :
                item=name_arr[i]
                namespace_begin+=f"namespace {item}{{"
                namespace_end+="}"
            
        variant_str=f"using {name_arr[-1]}=std::variant<"
        
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
    {namespace_begin}
    {variant_str}

    {namespace_end}
    """
    def write_files(self,variant_type_full_name,meta_type_full_name):
        for path,file in self.files:
            with open(f"{self.dir_path}/{path}","w",encoding="utf-8") as f:
                f.write(file.to_string(variant_type_full_name,meta_type_full_name))
        
        
    def write_variant_header_file(self,path,variant_type_full_name):
        with open(path,"w",encoding="utf-8") as f:
            f.write(self.create_variant_file(variant_type_full_name))