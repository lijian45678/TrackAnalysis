# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 0:28
# @Author  : LiJian
# @Site    : 
# @File    : Kmean.py
# @Software: PyCharm

#K-means算法
from pylab import *
from numpy import *
import codecs
import matplotlib.pyplot as plt
data=[]
labels=[]
#数据读取
with codecs.open("data.txt","r") as f:
    for line in f.readlines():
        x,y,label=line.strip().split('\t')
        data.append([float(x),float(y)])
        labels.append(float(label))
datas=array(data)
k=3#聚类数目
#计算欧式距离
def distance(x1,x2):
    return sqrt(sum(power(x1-x2,2)))
#随机初始化类中心
def randcenter(set,k):
    dim=shape(set)[1]
    init_cen=zeros((k,dim))
    for i in range(dim):
        min_i=min(set[:,i])
        range_i=float(max(set[:,i]) - min_i)
        init_cen[:,i]=min_i + range_i*random.rand(k)
    return init_cen
#主程序
def Kmeans(dataset,k):
    row_m=shape(dataset)[0]
    cluster_assign=zeros((row_m,2))
    center=randcenter(dataset,k)
    change=True
    while change:
        change=False
        for i in range(row_m):
            mindist=inf
            min_index=-1
            for j in range(k):
                distance1=distance(center[j,:],dataset[i,:])
                if distance1<mindist:
                    mindist=distance1
                    min_index=j
            if cluster_assign[i,0] != min_index:
                change=True
            cluster_assign[i,:]=min_index,mindist**2
        for cen in range(k):
            cluster_data=dataset[nonzero(cluster_assign[:,0]==cen)]
            center[cen,:]=mean(cluster_data,0)
    return center ,cluster_assign
cluster_center,cluster_assign=Kmeans(datas,k)
print(cluster_center)
#设置x,y轴的范围
xlim(0, 10)
ylim(0, 10)
#做散点图
f1 = plt.figure(1)
plt.scatter(datas[nonzero(cluster_assign[:,0]==0),0],datas[nonzero(cluster_assign[:,0]==0),1],marker='o',color='r',label='0',s=30)
plt.scatter(datas[nonzero(cluster_assign[:,0]==1),0],datas[nonzero(cluster_assign[:,0]==1),1],marker='+',color='b',label='1',s=30)
plt.scatter(datas[nonzero(cluster_assign[:,0]==2),0],datas[nonzero(cluster_assign[:,0]==2),1],marker='*',color='g',label='2',s=30)
plt.scatter(cluster_center[:,1],cluster_center[:,0],marker = 'x', color = 'm', s = 50)
