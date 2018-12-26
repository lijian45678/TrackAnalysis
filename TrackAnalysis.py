import time
import numpy as np
import sys
import os
from math import radians, cos, sin, asin, sqrt

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
class TrackPoint:

    def __init__(self ,  latitude =0.0, longitude =0.0 ,time='' ):
        self.latitude =latitude
        self.longitude = longitude
        self.time = time
    def print(self):
        print(self.latitude+' '+self.longitude+' '+self.time)
class ResidentPoint:
    def __init__(self ,  latitude =0.0, longitude =0.0 ,startTime='',stopTime ='',k=0):
        self.latitude =latitude
        self.longitude = longitude
        self.startTime=startTime
        self.stopTime =stopTime
        self.k=k
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right  # 每次聚类都是一对数据，left保存其中一个数据，right保存另一个
        self.vec = vec  # 保存两个数据聚类后形成新的中心
        self.id = id
        self.distance = distance
def yezi(clust):
        if clust.left == None and clust.right == None:
            return [clust.id]
        return yezi(clust.left) + yezi(clust.right)


def Euclidean_distance(vector1, vector2):
    TSum = sum([pow((vector1[i] - vector2[i]), 2) for i in range(len(vector1))])
    SSum = sqrt(TSum)
    return SSum


def hcluster(blogwords, n):
    biclusters = [bicluster(vec=blogwords[i], id=i) for i in range(len(blogwords))]
    distances = {}
    flag = None;
    currentclusted = -1
    while (len(biclusters) > n):  # 假设聚成n个类
        min_val = 999999999999;  # Python的无穷大应该是inf
        biclusters_len = len(biclusters)
        for i in range(biclusters_len - 1):
            for j in range(i + 1, biclusters_len):
                if distances.get((biclusters[i].id, biclusters[j].id)) == None:
                    distances[(biclusters[i].id, biclusters[j].id)] = Euclidean_distance(biclusters[i].vec,
                                                                                         biclusters[j].vec)
                d = distances[(biclusters[i].id, biclusters[j].id)]
                if d < min_val:
                    min_val = d
                    flag = (i, j)
        bic1, bic2 = flag  # 解包bic1 = i , bic2 = j
        newvec = [(biclusters[bic1].vec[i] + biclusters[bic2].vec[i]) / 2 for i in
                  range(len(biclusters[bic1].vec))]  # 形成新的类中心，平均
        newbic = bicluster(newvec, left=biclusters[bic1], right=biclusters[bic2], distance=min_val,
                           id=currentclusted)  # 二合一
        currentclusted -= 1
        del biclusters[bic2]  # 删除聚成一起的两个数据，由于这两个数据要聚成一起
        del biclusters[bic1]
        biclusters.append(newbic)  # 补回新聚类中心
        clusters = [yezi(biclusters[i]) for i in range(len(biclusters))]  # 深度优先搜索叶子节点，用于输出显示
    return biclusters, clusters

def compare_time(time1,time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    return int(s_time) - int(e_time)

def get_address_distance(lat1,lon1,lat2,lon2):
    # lon1 = 104.071000
    # lat1 = 30.670000
    # lon2 = 104.622000
    # lat2 = 28.765000
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    #返回结果除以米为单位保留两位小数
    return int(c * r * 1000*1000)


if __name__ == '__main__':
    startTime1 = time.time()
    listData = [] #轨迹序列
    rootdir = '.\\Geolife Trajectories 1.3\\Data\\000\\Trajectory'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                fileList = f.readlines()
                for dataLine in fileList[6:fileList.__len__()]:
                    dataLineList=dataLine.split(',')
                    trackPoint = TrackPoint(float(dataLineList[0]),float(dataLineList[1]),
                                            str(dataLineList[5]+' '+dataLineList[6]).split('\n')[0])
                    listData.append(trackPoint)
            f.close()


    for i in range(len(listData)-1):
            if compare_time(listData[i].time, listData[i + 1].time) >=0 :
                print("轨迹点序列没有按时间排序")

    print('轨迹点序列排列正确，完成第一步')
    # 驻留点集合
    clusteringList = []
    residentList = []
    #停留时间阈值
    Wt=100
    #空间阈值
    Wd=20
    # 异常点检测的聚类数
    Wn=20
    # 异常点集合
    R=()
    i=0

    #获取驻留点序列
    while i<(len(listData)-1):
        sumx=0
        sumy=0
        k=1
        startTime=listData[i].time
        while (compare_time(listData[i+1].time,listData[i].time)< Wt) and\
                (get_address_distance(listData[i+1].latitude,listData[i+1].longitude,listData[i].latitude,listData[i].longitude)<Wd):
             sumx+=listData[i].latitude
             sumy+=listData[i].longitude
             k+=1
             i+=1
        stopTime=listData[i].time
        i+=1
        clusteringList.append([sumx/k,sumy/k])
        residentList.append(ResidentPoint(sumx/k,sumy/k,startTime,stopTime,k))
    for i in range(len(residentList)-1):
            if compare_time(residentList[i].stopTime,residentList[i].startTime ) <0 :
                print("轨迹点序列没有按时间排序")
    print('驻留点序列排列正确，完成第二步')

    #对驻留点序列进行层次聚类
    # coding:UTF-8
    # Hierarchical clustering 层次聚类
    k,l = hcluster(clusteringList[0:1000],8)
    print(l)
    stopTime1 =time.time()
    print(compare_time(stopTime,startTime))











