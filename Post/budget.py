import os
import tecplot_io as tec
import numpy as np

def get_mkeb_wt(_path,NPZ):
    os.chdir(_path)
    print('Current working directory is ' + os.getcwd())
    filename = "mean_field_1d.dat"
    data = tec.tecplot_reader(filename, [NPZ, 24], 2)
    mkeb_wt = data[:,20]
    return mkeb_wt

def get_tau_sum(_path,NPZ):
    os.chdir(_path)
    print('Current working directory is ' + os.getcwd())
    filename = "mean_field_1d.dat"
    data = tec.tecplot_reader(filename, [NPZ, 24], 2)
    tau_sum = data[:,4]
    return tau_sum

def get_um(_path,NPZ):
    os.chdir(_path)
    print('Current working directory is ' + os.getcwd())
    filename = "mean_field_1d.dat"
    data = tec.tecplot_reader(filename, [NPZ, 24], 2)
    tau_sum = data[:,1]
    return tau_sum
    
def get_z(path,NPZ):
    os.chdir(path)
    print('Current working directory is ' + os.getcwd())
    filename = "mean_field_1d.dat"
    data = tec.tecplot_reader(filename, [NPZ, 24], 2)
    z = data[:,0]
    return z
