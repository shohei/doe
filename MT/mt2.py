import pandas as pd
import numpy as np
import pdb
import math

def mahalanobis(df, labels=[1,2,3,4,5,6]):
    N = len(labels)
    x_Y = [[]]*N
    for i in range(N):
        x_Y[i] = df[df.healthy=='Y']["x"+str(labels[i])]
    
    x_Y_base = [[]]*N
    for i in range(N):
        x_Y_base[i] = (x_Y[i]-x_Y[i].mean())/x_Y[i].std(ddof=0)
    
    x_N = [[]]*N
    for i in range(N):
        x_N[i] = df[df.healthy=='N']["x"+str(labels[i])]

    x_N_base = [[]]*N
    for i in range(N):
        x_N_base[i] = (x_N[i]-x_Y[i].mean())/x_Y[i].std(ddof=0)

    hash = {}
    for i in range(N):
        hash['x'+str(labels[i])] = x_Y_base[i]

    x_Y_base = pd.DataFrame(hash)
    S = np.cov(x_Y_base,rowvar=0,bias=True)
    V = np.linalg.inv(S)
    
    N_sample_Y = len(x_Y[0])
    M_Y = [0]*N_sample_Y
    xm_Y = [0]*N_sample_Y
    for i in range(N_sample_Y):
        xm_Y_temp = 0
        for j in range(N):
            x_Y_base_j = x_Y_base["x"+str(labels[j])]
            xm_Y_temp = np.vstack((xm_Y_temp,x_Y_base_j.tolist()[i]))
        xm_Y[i] = xm_Y_temp[1:]

        M_Y[i] = (xm_Y[i].transpose() @ V @ xm_Y[i]) / N #評価項目数Nで割る
    
    N_sample_N = len(x_N[0])
    M_N = [0]*N_sample_N
    xm_N = [0]*N_sample_N
    for i in range(N_sample_N):
        xm_N_temp = 0
        for j in range(N):
            # x_N_base_j = x_N_base["x"+str(labels[j])]
            x_N_base_j = x_N_base[j]
            xm_N_temp = np.vstack((xm_N_temp,x_N_base_j.tolist()[i]))

        xm_N[i] = xm_N_temp[1:]
        M_N[i] = (xm_N[i].transpose() @ V @ xm_N[i]) / N #評価項目数Nで割る

    return (M_Y, M_N)    

if __name__=="__main__":
    df = pd.read_csv('health.csv')
    labels = [[1,2,3,4,5,6],[1,2,3],[1,4,5],[1,6],[2,4],[2,5],[3,4],[3,5,6]]
    N = len(labels) #8
    M_N = [0]*N
    for i in range(N):
        _, M_N[i] = mahalanobis(df, labels[i])
        print(M_N[i])

    # Calculate SN ratio
    SN = [0]*N
    N_labels = len(df[df["healthy"]=='N'])
    for i in range(N):
        sumD = sum([1/m for m in M_N[i]])
        SN[i] = -10*math.log10(1/N_labels*sumD)

    print(SN)



