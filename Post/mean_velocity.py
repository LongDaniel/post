import os
import h5py
import numpy as np


def get_mean_velocity(_path,_tis,_tie,_tii):
    _nti = int((_tie - _tis) / _tii + 1)
    os.chdir(_path)
    print("Calculate mean velocity in working directory is: {0}".format(os.getcwd()))
    for _it in range(_nti):
        _ti = _tis + _tii * _it
        fname = 'DAT_{:010d}.h5'.format(_ti)
        f = h5py.File(fname,'r')
        u = f["u"]
        v = f["v"]
        w2 = f["w"]
        w = np.array(w2).copy()

        NPZ = u.shape[0]

        if _it==0:
            u_m_t = np.zeros((NPZ,3))
        
        w[0, :, :] = w2[0, :, :]
        for k in range(1,NPZ):
            w[k, :, :] = 0.5*(w2[k-1, :, :] + w2[k, :, :])
        
        u_m = np.zeros((NPZ,3))
        
        for k in range(NPZ):
            u_m[k,0] = np.mean(u[k,:,:])
            u_m[k,1] = np.mean(v[k,:,:])
            u_m[k,2] = np.mean(w[k,:,:])
    
        u_m_t = u_m_t + u_m
    
    u_m_t = u_m_t / _nti

    return u_m_t

def get_z_coordinate(_path,_tis):
    os.chdir(_path)
    print("Calculate z coordinate in working directory is: {0}".format(os.getcwd())) 
    fname = 'DAT_{:010d}.h5'.format(_tis)
    f = h5py.File(fname,'r')
    zz = np.array(f["z"][:,0,0]).copy()
    return zz