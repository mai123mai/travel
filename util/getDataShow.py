from travel.util.utils import *


def get_province_type():
    addressList = df_travel['address'].values
    types = list(map(lambda x: x.split(','), addressList))
    typeList = set()
    for i in types:
        typeList.add(i[0])
    # print(typeList)
    return list(typeList)

if __name__ == '__main__':
    print(get_province_type())