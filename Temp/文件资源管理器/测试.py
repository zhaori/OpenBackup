import os

"""
text_all_line=[]
text_all=os.listdir(path)
#string_all=" ".join(text_all)
#print(os.path.abspath(text_all))
for i in text_all:
    text_all_path=os.path.abspath(''.join(i))
    print(text_all_path)
"""
"""
def search_lines(path):
    li=os.listdir(path)
    text_li=[]
    for i in li:
       text_li.append(i)
       str_line=','.join(text_li)
       dict_line={
           os.path.abspath(path):{
                str_line
            }
        }
    with open("lines", "w", encoding="utf-8") as f:
        f.write(str(dict_line))
    return dict_line
"""
li = os.listdir("./文件夹")
text_li = []
for i in li:
    num = os.path.splitext(i)[1]
    text_li.append(num)
suffix = set(text_li)
# for a in suffix:
#    print(a)
# for (root,dir,file) in os.walk("./文件夹"):
#    filename=','.join(file)
for key in suffix:
    for i in li:
        if os.path.splitext(i)[1] == ".PNG":
            text_li.append(i)
            dict_line = {
                key: {
                    i
                }
            }
    print(dict_line)
