from util.utils import *


def getDeatailById(searchId):
    tableDate = df_travel.iloc[:,:13].values
    resultData = []
    for i in tableDate:
        if i[1] == int(searchId):
            i[12] = eval(i[12])
            resultData.append(list(i))
    return resultData


def getDeatailBySearchById(searchWord):
    # print(searchWord)
    tableDate = df_travel.iloc[:,:13].values
    resultData = []
    for i in tableDate:
        if i[2].find(searchWord) != -1:
            i[12] = eval(i[12])
            resultData.append(i)
    return resultData

if __name__ == '__main__':
    print(getDeatailById('682134'))
