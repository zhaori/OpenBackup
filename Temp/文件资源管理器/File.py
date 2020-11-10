path = "./文件夹"
lines = []
path_lines = []
textname_lines = []
# for (root,dirname,listname) in os.walk(path):

# print(os.path.splitext(path))
# l_l=os.path.join(path,"1.PNG")
# (a,b)=os.path.split(l_l)
# print(a)
"""
for i in li:
    num=os.path.splitext(i)[1]
    text_li.append(num)
#print(set(text_li))

for file in set(text_li):
    #字典
    dict_file={
        file:{
            
        }
    }
    print(dict_file)
"""

"""
for i in li:
       if  os.path.splitext(i)[1]==".PNG":
           text_li.append(i)
           str_line=','.join(text_li)
           dict_line={
                path:{
                    str_line
                }
            }
           with open("lines","w",encoding="utf-8") as f:
                f.write(str(dict_line))

with open("lines","r",encoding="utf-8") as f1:
    a=f1.read()
dict_st=eval(a)
print(dict_st.get(path))
"""
