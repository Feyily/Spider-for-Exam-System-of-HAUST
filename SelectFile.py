def selectfile(text,name):
    reader=open(name,encoding="utf-8")
    line=reader.readline()
    while line!='' and line!=None:
        if text in line:
            return True
        line = reader.readline()
    return False
