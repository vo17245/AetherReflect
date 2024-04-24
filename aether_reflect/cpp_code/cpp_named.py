class CppNamed:
    def __init__(self,name):
        self.name=name
    def parse_name(self):
        arr=self.name.split("::")
        t=[]
        for item in arr:
            if item=="":
                continue
            t.append(item)
        arr=t
        
        if len(arr)==1:
            return None,arr[0]    
        else:
            return arr[0:-1],arr[-1]
    def get_full_name(self):
        return self.name
    def get_name(self):
        _,name=self.parse_name()
        return name
    def get_namespace(self):
        namespace,_=self.parse_name()
        return namespace