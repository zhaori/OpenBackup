from Lib.MongoDBSever import Mongodb_server
from config.Mongo_config import *

file_path = r'D:\OneDrive\Python\垃圾回收站\文件资源管理器\文件夹\1.PNG'
with open(file_path, 'rb') as f:
    photo = f.read()
data = {
    'name': 'photo',
    'photo': photo
}
m = Mongodb_server(Mongo_host, Mongo_port)
# m.insert('photo', 'one', ca_info)
a = m.search('photo', 'one', {"_id": 0, "poto": 1})
print(a)
# print()
# with open('1.png', 'wb') as f:
#   f.write(dict(a[0])['photo'])
