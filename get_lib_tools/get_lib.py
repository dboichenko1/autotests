import requests
def get_lib_export_data(version):
    req = requests.get(f"https://mbakholdin.xstaging.tv/pine-facade/get_lib_export_data/Batut/MyLibrar234/1?v={version}")
    return req.json()
print(f"v2 = {get_lib_export_data(2).keys()}\nv3 = {get_lib_export_data(3).keys()}")
print(f"v2 = {get_lib_export_data(2)['libInfo'].keys()}\nv3 = {get_lib_export_data(3)['libInfo'].keys()}")

print(f"v2 = {get_lib_export_data(2)['exports'].keys()}\nv3 = {get_lib_export_data(3)['exports'].keys()}")
with open("v2.json" ,"w") as q:
    q.write(str(get_lib_export_data(2)))
with open("v3.json" ,"w") as q:
    q.write(str(get_lib_export_data(3)))


# print(get_lib_export_data(2))
# print(get_lib_export_data(3))