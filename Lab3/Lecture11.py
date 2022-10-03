import numpy as np
import scipy as sp
import scipy.linalg
import csv
from scipy import fft

def prony(x: np.array, T: float):
    if len(x) % 2 == 1:
        x = x[:len(x)-1]

    p = len(x) // 2

    shift_x = [0] + list(x)
    a = scipy.linalg.solve([shift_x[p+i:i:-1] for i in range(p)], -x[p::])

    z = np.roots([*a[::-1], 1])

    h = scipy.linalg.solve([z**n for n in range(1, p + 1)], x[:p])

    f = 1 / (2 * np.pi * T) * np.arctan(np.imag(z) / np.real(z))
    alfa = 1 / T * np.log(np.abs(z))
    A = np.abs(h)
    fi = np.arctan(np.imag(h) / np.real(h))

    return f, alfa, A, fi    

def median(b):
    a = b.copy()
    a.sort()
    if a.size % 2:
        return a[int(a.size / 2)]
    return (a[int((a.size) / 2)] + a[int((a.size) / 2 - 1)]) / 2.0

def slide_median(x: np.ndarray, m):
    x_filtered = np.zeros(x.size)
    for i in range(x.size):
        if i < m:
            x_filtered[i] = median(x[0 : 2 * i + 1])
        elif i >= x.size - m - 1:
            x_filtered[i] = median(x[i - (x.size - i) : x.size])
        else:
            x_filtered[i] = median(x[i - m : i + m + 1])
    return x_filtered

def rot_point_arr(a):
    f = lambda a, b, c: 1 if (b > a and b > c) or (b < a and b < c) else 0
    rot = np.array([f(a[i], a[i + 1], a[i + 2]) for i in range(a.size - 2)])
    return rot

def kandell(x, x_model):
    r = x - x_model
    r_est = 2.0 / 3.0 * (x.size - 2)
    r_disp = (16 * x.size - 29) / 90.0
    rot_points_amount = rot_point_arr(r).sum()
    print("Rotation points amount:", rot_points_amount)
    print("Estimated", r_est, "+-", r_disp)
    if rot_points_amount < r_est + r_disp and rot_points_amount > r_est - r_disp:
        print('rot point random')
    elif rot_points_amount > r_est + r_disp:
        print('rot point oscillating')
    elif rot_points_amount < r_est - r_disp:
        print('rot point korrelation')   

if __name__ == "__main__":
    from matplotlib import pyplot as plt
        
    # Signal
    h = 0.02
    x = np.array([sum([(k * np.exp(-h * i / k) * np.cos(2 * np.pi * k * h * i + np.pi / 4.)) for k in range(1, 4)]) for i in range(1, 201)])


    # test signal
    N = 128
    # Time vector
    t = np.linspace(0, 1, N, endpoint=True)

    # Amplitudes and freqs
    f1, f2, f3 = 2, 7, 12
    A1, A2, A3 = 5, 1, 3

    # Signal
    x = A1 * np.cos(2*np.pi*f1*t) + A2 * np.cos(2*np.pi*f2*t) + A3 * np.cos(2*np.pi*f3*t)
    
    f, alfa, A, fi = prony(x, 0.1)
    plt.stem(2*A)
    plt.plot()
    plt.grid()
    plt.figure()

    time = []
    temp = []

    with open('export.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            time.append(row[0])
            temp.append((float(row[2]) + float(row[3])) / 2.0)
    #remove names
    time = time[1::]
    temp = temp[1::]

    temp = [float(t) for t in temp]

    # plot all values
    plt.plot(temp)
    trend = slide_median(np.array(temp), 55)
    plt.plot(trend)

    # 3 parts: trend, regular coleb, ostatki
    # kandell says if ostatki is random
    kandell(trend, np.array(temp))

    plt.figure()
    # regular coleb with fft
    f = np.fft.fft(temp)
    ff = f.real * f.real + f.imag * f.imag
    sz = len(ff)
    ff = ff[0:100]
    plt.plot(ff)
    plt.grid()
    for delta in [1, 8]:
        ff = ff[delta:100]
        print(sz / ((ff.argmax() + delta)), "days")    
    plt.show()
