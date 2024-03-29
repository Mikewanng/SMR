﻿#随机可信中继，固定拓扑，随机请求

from Topo import *
from Net import *
from Alg1 import *
from RandomRouting import *
from Alg2 import *
from Securitylevel import *
import copy,random,time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
count=1000



#g=Net().network

g=Topo().create_random_topology(100)
g1=Topo().CreatNodeEdgeSet(g,10,5,0.8)
g2=Topo().CreatTopo(g1)
source=random.randint(0,len(g2[0])-1)
des=random.randint(0,len(g2[0])-1)
while des==source:
    des=random.randint(0,len(g2[0])-1)
sth=np.arange(0.5,1,0.05)
filename='Sp_vs_sth'+str(count)+'time='+str(time.time())+'.txt'
fp = open(filename, 'w')
fp.write('sth    avesecurityprobability1    ressecurityprobability    respond_rate    avekeyconsume    reskeyconsume    keynum    time1    avesecurityprobability2    ressecurityprobability    respond_rate    avekeyconsume    requestkeyconsume    keynum2    time2    avesecurityprobabilityr    ressecurityprobability    respond_rate    avekeyconsume    requestkeyconsume    keynumr    timer\n')
#平均安全概率
sp1=[0]*len(sth)
sp2=[0]*len(sth)
spr=[0]*len(sth)
#响应安全概率
sp1r=[0]*len(sth)
sp2r=[0]*len(sth)
sprr=[0]*len(sth)
#响应统计数
count1=[0]*len(sth)
count2=[0]*len(sth)
countr=[0]*len(sth)
countk=[0]*len(sth)
#响应率
respondrate1=[0]*len(sth)
respondrate2=[0]*len(sth)
respondrater=[0]*len(sth)

#平均总消耗
cost1=[0]*len(sth)
cost2=[0]*len(sth)
costr=[0]*len(sth)
#响应平均消耗
cost1r=[0]*len(sth)
cost2r=[0]*len(sth)
costrr=[0]*len(sth)
#密钥数量
keynum1=[0]*len(sth)
keynum2=[0]*len(sth)
keynumr=[0]*len(sth)
#时间
time1=[0]*len(sth)
time2=[0]*len(sth)
timer=[0]*len(sth)

f=0
for i in range(100):
    
    source=random.randint(0,len(g2[0])-1)
    des=random.randint(0,len(g2[0])-1)
    print('source=',source,'des=',des)
    while des==source:
        des=random.randint(0,len(g2[0])-1)
    for j in range(len(sth)):
        print(sth[j])
        ts1=time.time()
        t1=Alg1().alg1maxs(copy.deepcopy(g2),source,des)
        if t1[0][2]==1:
            continue
        print(t1)
        
        print(Seclev().sl(t1,sth[j]))
        t21=time.time()
        tsr=time.time()
        tr=Rr().rrmaxs(copy.deepcopy(g2),source,des)
        print(tr)
        print(Seclev().sl(tr,sth[j]))
        t2r=time.time()

        ts2=time.time()
        t2=Alg2().alg2max(copy.deepcopy(g2),source,des)
        print(t2)
        print(Seclev().sl(t2,sth[j]))
        t22=time.time()
     
        
       
        

for j in range(len(sp1)):#响应
    if count1[j]>0:
        sp1r[j]=sp1[j]/count1[j]
        cost1r[j]=cost1[j]/count1[j]
    if count2[j]>0:
        sp2r[j]=sp2[j]/count2[j]
        cost2r[j]=cost2[j]/count2[j]

    if countr[j]>0:
        sprr[j]=spr[j]/countr[j]
        costrr[j]=costr[j]/countr[j]










for j in range(len(sp1)):#平均
    sp1[j]/=count
    sp2[j]/=count
    spr[j]/=count
    respondrate1[j]=count1[j]/count
    respondrate2[j]=count2[j]/count
    respondrater[j]=countr[j]/count
    cost1[j]/=count
    cost2[j]/=count
    costr[j]/=count
    keynum1[j]/=count
    keynum2[j]/=count
    keynumr[j]/=count
    time1[j]/=count
    time2[j]/=count
    timer[j]/=count


for j in range(len(sth)):
    fp.write(str(sth[j])+'    '+str(sp1[j])+'    '+str(sp1r[j])+'    '+str(respondrate1[j])+'    '+str(cost1[j])+'    '+str(cost1r[j])+'    '+str(keynum1[j])+'    '+str(time1[j])+'    '+str(sp2[j])+'    '+str(sp2r[j])+'    '+str(respondrate2[j])+'    '+str(cost2[j])+'    '+str(cost2r[j])+'    '+str(keynum2[j])+'    '+str(time2[j])+'    '+str(spr[j])+'    '+str(sprr[j])+'    '+str(respondrater[j])+'    '+str(costr[j])+'    '+str(costrr[j])+'    '+str(keynumr[j])+'    '+str(timer[j])+'\n')
fp.close()
fig = plt.figure()
plt.plot(sth,sp1,color='red')
plt.plot(sth,sp2,color='green')
plt.plot(sth,spr,color='black')
plt.title("average Security probability")
plt.xlabel('sth')
plt.ylabel('Security probability')
plt.show()

fig = plt.figure()
plt.plot(sth,sp1r,color='red')
plt.plot(sth,sp2r,color='green')
plt.plot(sth,sprr,color='black')
plt.title("res Security probability")
plt.xlabel('sth')
plt.ylabel('Security probability')
plt.show()

fig = plt.figure()
plt.plot(sth,count1,color='red')
plt.plot(sth,count2,color='green')
plt.plot(sth,countr,color='black')
plt.title("request Response rate  ")
plt.xlabel('sth')
plt.ylabel('Response rate')
plt.show()

fig = plt.figure()
plt.plot(sth,cost1,color='red')
plt.plot(sth,cost2,color='green')
plt.plot(sth,costr,color='black')
plt.title("ave key consume")
plt.xlabel('sth')
plt.ylabel('consume')
plt.show()


fig = plt.figure()
plt.plot(sth,cost1r,color='red')
plt.plot(sth,cost2r,color='green')
plt.plot(sth,costrr,color='black')
plt.title("res key consume")
plt.xlabel('sth')
plt.ylabel('consume')
plt.show()

fig = plt.figure()
plt.plot(sth,keynum1,color='red')
plt.plot(sth,keynum2,color='green')
plt.plot(sth,keynumr,color='black')
plt.title("final key number")
plt.xlabel('sth')
plt.ylabel('final key')
plt.show()