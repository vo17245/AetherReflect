filename="example2.h"
comment="""
example of a struct definition
"""#optional
includes="""
#include <string>
"""#optional

structs=[
    {
        "name":"::Aether::Person2",
        "comment":"a struct for test",# optional
        "fields":[
            {
                "name":"tag",
                "type":"::std::string",
                "comment":"tag field"#optional
            },
            {
                "name":"age",
                "type":"uint64_t",
                "comment":"age field"#optional
            }
            
        ],
        "constructors":[
            """
            Person2(const std::string& _tag,uint64_t _age):
                tag(_tag),age(_age)
            {}
            """,
        ]
    }
]#optional