import numpy as np
import scipy.optimize
import scipy.stats as st
import scipy as scp
import matplotlib.pyplot as plt
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore", category=FutureWarning)

def two_fak(arr):
    r = plt.boxplot(arr)
    top_points = r["fliers"][0].get_data()[1]
    b = np.delete(arr, np.array([(arr[i] in top_points) for i in range(arr.size)]))
    return b.mean()

if __name__ == "__main__":
    experiment_size = 10000
    k_huber = 1.44
    norm = np.zeros(100)
    cauchi = np.zeros(100)
    comb = np.zeros(100)
    estimates = {
        'norm': {
            'mean': np.zeros(experiment_size),
            'med': np.zeros(experiment_size),
            'huber': np.zeros(experiment_size),
            'twofac': np.zeros(experiment_size)
        },
        'cauchi': {
            'mean': np.zeros(experiment_size),
            'med': np.zeros(experiment_size),
            'huber': np.zeros(experiment_size),
            'twofac': np.zeros(experiment_size)
        },
        'comb': {
            'mean': np.zeros(experiment_size),
            'med': np.zeros(experiment_size),
            'huber': np.zeros(experiment_size),
            'twofac': np.zeros(experiment_size)
        }
    }

    def f_huber_norm(tet):
        suk = sum([scp.special.huber(k_huber, norm[j] - tet) for j in range(100)])
        return suk

    def f_huber_cauchi(tet):
        suk = sum([scp.special.huber(k_huber, cauchi[j] - tet) for j in range(100)])
        return suk

    def f_huber_comb(tet):
        suk = sum([scp.special.huber(k_huber, comb[j] - tet) for j in range(100)])
        return suk

    for i in tqdm(range(experiment_size)):
        norm = np.random.normal(0, 1, 100)
        norm.sort()
        cauchi = np.random.standard_cauchy(100)
        cauchi.sort()
        comb = np.random.normal(0, 1, 100) * 0.9 + np.random.standard_cauchy(100) * 0.1
        comb.sort()

        estimates['norm']['mean'][i] = norm.mean()
        estimates['cauchi']['mean'][i] = cauchi.mean()
        estimates['comb']['mean'][i] = comb.mean()

        estimates['norm']['med'][i] = norm[50]
        estimates['cauchi']['med'][i] = cauchi[50]
        estimates['comb']['med'][i] = comb[50]

        estimates['norm']['huber'][i] = scp.optimize.minimize_scalar(f_huber_norm).x
        estimates['cauchi']['huber'][i] = scp.optimize.minimize_scalar(f_huber_cauchi).x
        estimates['comb']['huber'][i] = scp.optimize.minimize_scalar(f_huber_comb).x

        estimates['norm']['twofac'][i] = two_fak(norm)
        estimates['cauchi']['twofac'][i] = two_fak(cauchi)
        estimates['comb']['twofac'][i] = two_fak(comb)

    print('Normal distribution:')
    print('mean: \t\t\t', estimates['norm']['mean'].mean(), '\t variance:\t', estimates['norm']['mean'].var())
    print('median: \t\t', estimates['norm']['med'].mean(), '\t variance:\t', estimates['norm']['med'].var())
    print('huber: \t\t\t', estimates['norm']['huber'].mean(), '\t variance:\t', estimates['norm']['huber'].var())
    print('two factor: \t', estimates['norm']['twofac'].mean(), '\t variance:\t', estimates['norm']['twofac'].var())

    print('Cauchy distribution:')
    print('mean: \t\t\t', estimates['cauchi']['mean'].mean(), '\t variance:\t', estimates['cauchi']['mean'].var())
    print('median: \t\t', estimates['cauchi']['med'].mean(), '\t variance:\t', estimates['cauchi']['med'].var())
    print('huber: \t\t\t', estimates['cauchi']['huber'].mean(), '\t variance:\t', estimates['cauchi']['huber'].var())
    print('two factor: \t', estimates['cauchi']['twofac'].mean(), '\t variance:\t', estimates['cauchi']['twofac'].var())

    print('Combined distribution:')
    print('mean: \t\t\t', estimates['comb']['mean'].mean(), '\t variance:\t', estimates['comb']['mean'].var())
    print('median: \t\t', estimates['comb']['med'].mean(), '\t variance:\t', estimates['comb']['med'].var())
    print('huber: \t\t\t', estimates['comb']['huber'].mean(), '\t variance:\t', estimates['comb']['huber'].var())
    print('two factor: \t', estimates['comb']['twofac'].mean(), '\t variance:\t', estimates['comb']['twofac'].var())