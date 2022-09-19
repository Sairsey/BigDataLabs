import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

def task(i):
    print("")
    print("*** TASK", i)
    return
    
def generate():
    h = 0.05
    #x1 = [0] * 200
    x = np.array([np.sqrt(k * h) + np.random.normal() for k in range(1000)])
    return x

def model():
    h = 0.05
    x = np.array([np.sqrt(k * h) for k in range(1000)])
    return x

def slide_mean(x, m):
    x_filtered = np.zeros(x.size)
    for i in range(x.size):
        if i < m:
            x_filtered[i] = sum([x[j] for j in range(0, 2 * i + 2)]) / (2.0 * i + 1)
        elif i >= x.size - m - 1:
            x_filtered[i] = sum([x[j] for j in range(i - (x.size - i), x.size)]) / len(range(i - (x.size - i), x.size))
        else:
            x_filtered[i] = sum([x[j] for j in range(i - m, i + m + 1)]) / (2.0 * m + 1)
    return x_filtered

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

def main():
    np.random.seed(0)
    task(1)
    x = generate()
    print(x)
    
    task(2)
    x_model = model()
    x_mean_21 = slide_mean(x, 10)
    x_mean_51 = slide_mean(x, 25)
    x_mean_111 = slide_mean(x, 55)
    plt.title("Task 2")
    plt.plot(x, label = 'source')
    plt.plot(x_model, label = 'model')
    plt.plot(x_mean_21, label='x_mean_21')
    plt.plot(x_mean_51, label='x_mean_51')
    plt.plot(x_mean_111, label='x_mean_111')
    plt.legend()

    plt.figure()    
    task(3)
    plt.title("Task 3")

    plt.plot(x, label = 'source')
    plt.plot(x_model, label = 'model')
    x_med_21 = slide_median(x, 10)
    x_med_51 = slide_median(x, 25)
    x_med_111 = slide_median(x, 55)
    plt.plot(x_med_21, label='x_med_21')
    plt.plot(x_med_51, label='x_med_51')
    plt.plot(x_med_111, label='x_med_111')
    plt.legend()
    
    task(4)
    print("x_mean_21")
    kandell(x_mean_21, x)
    print("x_mean_51")
    kandell(x_mean_51, x)
    print("x_mean_111")
    kandell(x_mean_111, x)
    print("x_med_21")
    kandell(x_med_21, x)
    print("x_med_51")
    kandell(x_med_51, x)
    print("x_med_111")
    kandell(x_med_111, x)

    plt.show()
   
    
if __name__ == "__main__":
    main()