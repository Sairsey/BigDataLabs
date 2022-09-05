import math

def task(i):
    print("*** TASK", i)
    return

def norm1(x):
    ans = 0
    for i in x:
        ans += abs(i)
    return ans

def norm2(x):
    ans = 0
    for i in x:
        ans += i*i
    return math.sqrt(ans)
    
def normw(x, w):
    ans = 0        
    for i in range(len(x)):
        ans += abs(x[i]) * w[i]
    return ans
    
def main():
    task(2)
    x, y = [i for i in range(-10, 5)], [i for i in range(-5, 10)]
    print("vec x", x)
    print("vec y", y)
    task(3)
    z = [(y[int(i / 2)] if i % 2 == 0 else x[int((i-1) / 2)]) for i in range(len(x) + len(y))]
    print("vec z", z)
    task(4)   
    print("x norm_1", norm1(x), "norm_2", norm2(x))
    print("y norm_1", norm1(y), "norm_2", norm2(y))
    print("z norm_1", norm1(z), "norm_2", norm2(z))
    task(6)
    ans = int(input("Print number to calculate factorial:"))
    print(str(ans) + "! =", math.factorial(ans))
    task(7)
    print("Write your 5 number to create vector")
    ans = [float(t) for t in input().split()]
    if len(ans) != 5:
        print("Not 5 elements provided")
        return
    print("Max", max(ans), "Min", min(ans), "Sum", sum(ans))
    print("norm_1", norm1(ans))
    print("norm_2", norm2(ans))
    print("Write your 5 number to create vector of weights")
    w = [float(t) for t in input().split()]
    if len(w) != 5:
        print("Not 5 elements provided")
        return
    if min(w) <= 0:
        print("Weight cannot be negative")
        return
    if sum(w) != 1:
        print("Sum must be equal 1")
        return
    print("norm_w", normw(ans, w))
    
if __name__ == "__main__":
    main()