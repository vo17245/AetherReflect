from cpp_code.cpp_named import CppNamed
def add_indent(s,indent):
    res=""
    for i in range(indent):
        res+=" "
    res+=s
    return res



class Field(CppNamed):
    def __init__(self,name,type,comment):
        super().__init__(name)
        self.type=type
        self.comment=comment
    def to_string(self):
        return f"{self.type} {self.name};\n"
    @staticmethod
    def from_obj(obj):
        comment=obj.get("comment","")
        return Field(obj["name"],obj["type"],comment)
        
class Struct(CppNamed):
    def __init__(self,name:str,comment:str):
        super().__init__(name)
        self.fields:list[Field]=[]
        self.comment=comment
        self.constructors:list[str]=[]
    def add_field(self, field):
        self.fields.append(field)
    def add_constructor(self,constructor:str):
        self.constructors.append(constructor)
    def to_string(self,indent):
        cur_indent=0
        namespace=self.get_namespace()
        namespace_begin=""
        namespace_end=""
        if len(namespace)!=0:
            for s in namespace:
                namespace_begin += f"namespace {s}{{\n"
                namespace_end+=f"}}\n"
        
        struct_begin=""
        
        for line in self.comment.splitlines():
            struct_begin+=add_indent(f"// {line}\n",cur_indent)
        struct_begin+=add_indent(f"struct {self.get_name()}\n",cur_indent)
        struct_begin+=add_indent("{\n",cur_indent)
        struct_end=add_indent("};\n",cur_indent)
        cur_indent+=indent
        constructors_str=""
        for constructor in self.constructors:
            for line in constructor.splitlines():
                constructors_str+=add_indent(f"{line}\n",cur_indent)
        
        
        fields_str=""
        for field in self.fields:
            fields_str+=add_indent(field.to_string(),indent)
        cur_indent-=indent
        return f"{namespace_begin}{struct_begin}{constructors_str}{fields_str}{struct_end}{namespace_end}"
    def create_reflect_code(self):
        namespace="Aether"
        name="Reflect"
        field_names="{"
        for field in self.fields:
            field_names+=f'"{field.name}",'
        field_names+="};"
        field_types="{"
        for field in self.fields:
            field_types+=f'"{field.type}",'
        field_types+="};"
        # ======= getter
        getter_str=""
        
        getter_str+=f"\
        static ReflectVariant Get(const {self.name}& obj,const std::string& key){{"
        for i in range(len(self.fields)):
            if i==0:
                getter_str+=f"""
            if(key=="{self.fields[i].name}"){{
                return obj.{self.fields[i].name};
            }}"""
            else:
                getter_str+=f"""
            else if(key=="{self.fields[i].name}"){{
                return obj.{self.fields[i].name};
            }}"""
        getter_str+="\n}"

    
    # ======= setter
        setter_str=f"static void Set({self.name}& obj,const std::string& key,const ReflectVariant& value){{\n"
        for i in range(len(self.fields)):
            if i==0:
                setter_str+=f"""
            if(key=="{self.fields[i].name}"){{
                obj.{self.fields[i].name}=std::get<{self.fields[i].type}>(value);
            }}"""
            else:
                setter_str+=f"""
            else if(key=="{self.fields[i].name}"){{
                obj.{self.fields[i].name}=std::get<{self.fields[i].type}>(value);
            }}"""
        setter_str+="\n}"

    #======= field comment
        field_comment="static constexpr const inline char* field_comments[]={"
        for field in self.fields:
            field_comment+=f'"{field.comment}",'
        field_comment+="};"
    # ======= code
        code=f"""\
namespace {namespace}{{
    template<>
    struct {name}<{self.name}>
    {{
        static constexpr const inline char* name="{self.name}";
        static constexpr const inline char* comment="{self.comment}";
        static constexpr const inline size_t field_count={len(self.fields)};
        static constexpr const inline char* field_names[]={field_names}
        static constexpr const inline char* field_types[]={field_types}
        {field_comment}
        {getter_str}
        {setter_str}
    }};
}}
        """
        return code
    @staticmethod
    def from_obj(obj:dict):
        comment=obj.get("comment","")
        struct=Struct(obj["name"],comment)
        for constructor in obj["constructors"]:
            struct.add_constructor(constructor)
        for field in obj["fields"]:
            struct.add_field(Field.from_obj(field))
        return struct
        



        

