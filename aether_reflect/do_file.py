def do_file(path):
    with open(path,"r",encoding="utf-8") as f:
        data=f.read()
    
    g={
    "filename":"",
    "structs":[],
    "includes":"",
    "comment":""
    }
    exec(data,g)
    obj={
        "filename":g["filename"],
        "structs":g["structs"],
        "includes":g["includes"],
        "comment":g["comment"],
    }
   
    return obj