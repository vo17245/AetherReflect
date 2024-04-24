filename="example.h"
comment="""
example of a struct definition
"""#optional
includes="""
#include <string>
"""#optional

structs=[
    {
        "name":"::Aether::Person",
        "comment":"a struct for test",# optional
        "fields":[
            {
                "name":"tag",
                "type":"::std::string",
                "comment":"tag field"#optional
            }
            
        ],
        "constructors":[
            """
            Person(const std::string& _tag):
                tag(_tag)
            {}
            """,
        ]
    }
]#optional