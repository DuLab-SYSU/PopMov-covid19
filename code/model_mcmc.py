import random
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import poisson
from scipy.stats import powerlaw
from pathlib import Path

os.chdir('../')
root_dir = Path.cwd()
data_dir = root_dir.joinpath('data')

if not result_dir.exists():
    result_dir.mkdir()

if not data_dir.exists():
    data_dir.mkdir()


def MCMC(X, Y, num):
    N = 3000  # MCMC步数
    a = 10
    b = 0  # 初始值
    A = []
    B = []  # 参数更新
    C = []
    D = []
    LK = 0
    Result = {}
    for x, y in zip(X, Y):
        ilk = norm.logpdf(y, a * x + b, 1)
        LK += (ilk)  # record likelihood
    for i in range(N):
        a2 = norm.rvs(a, 0.5, 1)
        b2 = norm.rvs(b, 0.5, 1)
        lk1 = 0
        lk2 = 0
        for x, y in zip(X, Y):

            lk1 += np.log(poisson.pmf(k=int(y), mu=a * x + b))
            lk2 += np.log(poisson.pmf(k=int(y), mu=a2 * x + b2))
        R = np.exp(lk2 - lk1)
        if (random.random() < R):
            a = a2
            b = b2
            print('iters:', i, 1000, a, b, lk2)

        C.append((lk2))
        A.append(a)
        B.append(b)
        D.append((float(a), float(b), float(lk2)))
    D = [i for i in D if str(i[2]) != 'nan']
    D = sorted(D, key=lambda x: x[2], reverse=True)[0]

    a, b, c = D[0], D[1], D[2]

    return (float(a), float(b))


def CalAIC(y_test, y_pred, k, n):
    SSR = []
    for i, j in zip(y_test, y_pred):
        resid = i - j
        SSR.append(resid**2)
    SSR = sum(SSR)
    AICValue = 2 * k + n * np.log(float(SSR) / n)
    return AICValue


if __name__ == "__main__":

    df = pd.read_csv('./data/model_input_data.csv')
    df1 = df.iloc[:181, :]
    df2 = df.iloc[181:, :]
    CityList = list(df['city'])
    betaList = []
    for num in range(1000):
        df3 = df1.sample(n=100, frac=None, replace=True, weights=None, axis=0)
        df4 = df2.sample(n=100, frac=None, replace=True, weights=None, axis=0)
        df_para = pd.concat([df3, df4])
        X, Y = list(df_para['risk']), list(df_para['case'])
        betaList.append(MCMC(X, Y, num))

    with open(result_dir / ('bootstrap_para_100'), 'w') as f:
        for i in betaList:
            f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
