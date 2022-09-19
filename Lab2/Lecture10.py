import numpy as np
import scipy as sc
import scipy.stats as st
import matplotlib.pyplot as plt

def task(i):
    print("")
    print("*** TASK", i)
    return
    
def generate():
    h = 0.1
    x = np.array([0.5 * np.sin(k * h) + np.random.normal() for k in range(200)])
    return x

def model():
    h = 0.1
    x = np.array([0.5 * np.sin(k * h) for k in range(200)])
    return x

def exp_mean(x, a):
    y = np.zeros(x.size)
    y[0] = x[0]
    for i in range(1, x.size):
        y[i] = a * x[i] + (1.0 - a) * y[i - 1]
    return y

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
    
    print('mean reminder ', r.mean())
    print('disp reminder ', st.tstd(r))

    print('normal with p = ', np.sqrt(st.normaltest(r)[1]))

def main():
    np.random.seed(0)
    task(1)
    x = generate()
    print(x)
    
    task(2)
    x_model = model()
    x_exp_0_01 = exp_mean(x, 0.01)
    x_exp_0_05 = exp_mean(x, 0.05)
    x_exp_0_1 = exp_mean(x, 0.1)
    x_exp_0_3 = exp_mean(x, 0.3)
    plt.title("Task 2")
    plt.plot(x, label = 'source')
    plt.plot(x_model, label = 'model')
    plt.plot(x_exp_0_01, label='x_exp_0_01')
    plt.plot(x_exp_0_05, label='x_exp_0_05')
    plt.plot(x_exp_0_1, label='x_exp_0_1')
    plt.plot(x_exp_0_3, label='x_exp_0_3')
    plt.legend()

    plt.figure()    
    task(4)
    plt.title("Task 4")
    
    f = np.fft.fft(x)
    ff = f.real * f.real + f.imag * f.imag
    plt.plot([(i + 1) / x.size * 2 * np.pi for i in range(x.size)], ff)
    #plt.plot(ff)
    freq = (ff[:180].argmax() + 1.0) / x.size * 2.0 * np.pi
    freq_i = ff.argmax()
    print(freq)
    plt.figure()
    
    task(5)
    print("x_exp_0_01")
    kandell(x_exp_0_01, x)
    print("x_exp_0_05")
    kandell(x_exp_0_05, x)
    print("x_exp_0_1")
    kandell(x_exp_0_1, x)
    print("x_exp_0_3")
    kandell(x_exp_0_3, x)

    plt.show()
   
    
if __name__ == "__main__":
    main()