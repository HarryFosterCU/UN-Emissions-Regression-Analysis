import numpy as np


def Pearson_correlation(X,Y):
    if len(X) == len(Y):
        Sum_xy = sum((X-X.mean())*(Y-Y.mean()))
        Sum_x_squared = sum((X-X.mean())**2)
        Sum_y_squared = sum((Y-Y.mean())**2)       
        corr = Sum_xy / np.sqrt(Sum_x_squared * Sum_y_squared)
    return(corr)


def Regression_Selector(X, Y, Min, Max):
    degree = int(input("What degree of best fit would you like?"))
    print("Degree = ", degree)
    coeffs = np.polyfit(X, Y, deg=degree)
    K = np.linspace(Min, Max, Max*10)
    M = 0
    for x in range(len(coeffs)):
        M += coeffs[x] * K ** ((len(coeffs) - x) - 1)
    return(K, M)