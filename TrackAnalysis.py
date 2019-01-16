import time
import numpy as np
import sys
import os
from math import radians, cos, sin, asin, sqrt
import scipy
import scipy.cluster.hierarchy as sch
import matplotlib.pylab as plt
import matplotlib.pyplot as plot
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图

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
        self.startTime = startTime
        self.stopTime = stopTime
        self.k = k
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right  # 每次聚类都是一对数据，left保存其中一个数据，right保存另一个
        self.vec = vec  # 保存两个数据聚类后形成新的中心
        self.id = id
        self.distance = distance

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
    rootdir = 'C:\\Users\\LJ\\Desktop\\TA\\Geolife Trajectories 1.3\\Data\\000\\Trajectory'
    #rootdir = 'C:\\Users\\lcy\\Desktop\\HardwareSimulator\\TrackAnalysis\\Geolife Trajectories 1.3\\Data\\000\\Trajectory'
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
    # 数据清洗模块
    print('轨迹点序列排列正确，完成第一步，总计点数是：',len(listData))
    # fig = plot.figure()
    # # 得到画面
    # ax = Axes3D(fig)
    # ax.set_xlabel('维度')
    # ax.set_ylabel('经度')
    # ax.set_zlabel('时间(秒)')
    # 得到3d坐标的图
    #  画点
    # for i in listData:
    #     x.append(i.latitude)
    #     y.append(i.longitude)
    #     z.append(int(time.mktime(time.strptime(i.time,'%Y-%m-%d %H:%M:%S'))))
    # for x in listData[0:1000]:
    #     ax.scatter(x.latitude,x.longitude,int(time.mktime(time.strptime(x.time,'%Y-%m-%d %H:%M:%S'))),
    #                c='r')
    #
    # plot.savefig("轨迹点_1.png")
    # plot.show()
    # 驻留点集合
    clusteringList = []
    residentList = []
    #停留时间阈值
    Wt=100000
    #空间阈值0
    Wd=200000
    # 异常点检测的聚类数
    Wn=20
    # 异常点集合
    R=()
    i=0
    n=0
    #获取驻留点序列
    while i<(len(listData)-1):
        sumLatitude=listData[i].latitude
        sumLongitude=listData[i].longitude
        k=1
        startTime=listData[i].time
        while (compare_time(listData[i+1].time,listData[i].time)< Wt) and\
                (get_address_distance(listData[i+1].latitude,listData[i+1].longitude,listData[i].latitude,listData[i].longitude)<Wd):
             sumLatitude+=listData[i].latitude
             sumLongitude+=listData[i].longitude
             k+=1
             i+=1
             if i == len(listData)-1:
                 break
        stopTime=listData[i].time
        i+=1
        clusteringList.append([sumLatitude/k,sumLongitude/k])
        residentList.append(ResidentPoint(sumLatitude/k,sumLongitude/k,startTime,stopTime,k))
    #驻留点测试
    for i in range(len(residentList)-1):
            if compare_time(residentList[i].stopTime,residentList[i].startTime ) <0 :
                print("驻留点序列没有按时间排序")
    print('驻留点序列排列正确，完成第二步,总计点数是：',len(residentList))
    # fig = plot.figure()
    # # 得到画面
    # ax = Axes3D(fig)
    # # 得到3d坐标的图
    # #  画点
    # for x in residentList:
    #     ax.scatter(x.latitude, x.longitude, int(time.mktime(time.strptime(x.startTime, '%Y-%m-%d %H:%M:%S'))),
    #                c='r')
    # # plot.show()
    # plot.savefig('驻留点图_1.png')

    #对驻留点序列进行层次聚类
    # coding:UTF-8
    # Hierarchical clustering 层次聚类
    # k,l = hcluster(clusteringList[0:1000],8)
    # print(l)
    # stopTime1 =time.time()
    disMat = sch.distance.pdist(clusteringList, 'euclidean')
    # 进行层次聚类:
    Z = sch.linkage(disMat, method='average')
    # 将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
    print(Z)
    P = sch.dendrogram(Z)
    plt.savefig('聚类_1.png')
    # 根据linkage matrix Z得到聚类结果:
    cluster = sch.fcluster(Z, t=1)
    # lis = []
    # for i in cluster:
    #     lis.append(i)
    # print(lis)
    # n=set(lis)
    # print(n)
    # for i in n:
    #     if lis.count(i)==1:
    #         print(clusteringList[lis.index(i)])
    print("Original cluster by hierarchy clustering:\n", cluster,cluster.__len__())
    print(compare_time(stopTime,startTime))











