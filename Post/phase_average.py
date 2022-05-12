import numpy as np
import os
import tecplot_io as tec


def diff_central(x, y):
  x0 = x[:-2]
  x1 = x[1:-1]
  x2 = x[2:]
  y0 = y[:-2]
  y1 = y[1:-1]
  y2 = y[2:]
  f = (x2 - x1)/(x2 - x0)
  f1 = (1-f)*(y2 - y1)/(x2 - x1) + f*(y1 - y0)/(x1 - x0)
  f2 = x.copy()
  f2[1:-1] = f1
  f2[0] = f1[0]
  f2[-1] = f1[-1]
  return f2

def find_index(_z, _limits):
  _n = len(_z)
  _i_min = 0
  _i_max = _n - 1
  _limits2 = np.zeros(2)
  if isinstance(_limits, float):
    _limits2[0:2] = _limits
  else:
    _limits2 = _limits
          
  for i in range(_n):
    if _z[i]<_limits2[0] and i>_i_min :
      _i_min = i
    if _z[i]>_limits2[1] and i<_i_max :
      _i_max = i
  #print('zlimits='+str(_limits))
  #print('i_min='+str(_i_min)+', i_max='+str(_i_max))
  
  if isinstance(_limits, float):
    return _i_min
  else:
    return _i_min, _i_max

#function calculate the phase average
#input: folder name, phi, serial number, start time, end time, time interval
#output: phase average for that folder
def phase_average(_folder, _phi, t, tis, tie, tii,_NPZ,_NPX,_U,_Ustar):
    #change working directory
    os.chdir(_folder)
    print("current working directory is: {0}".format(os.getcwd()))
    #read data
    x_phase = np.zeros([_NPZ, 48])
    z_phase = np.zeros([_NPZ, 48])
    u_phase = np.zeros([_NPZ, 48])
    v_phase = np.zeros([_NPZ, 48])
    w_phase = np.zeros([_NPZ, 48])
    uu_phase = np.zeros([_NPZ, 48])
    vv_phase = np.zeros([_NPZ, 48])
    ww_phase = np.zeros([_NPZ, 48])
    uw_phase = np.zeros([_NPZ, 48])
    nti = int((tie - tis) / tii + 1)
    for it in range (nti):
        ti = tis + tii * it
        fname = 'Phase_Average_Phi{:01d}_{:04d}_{:08d}.dat'.format(_phi,t,ti)
        f = tec.tecplot_reader(fname, [_NPZ, _NPX, 6], 2)
        f = f.reshape([_NPZ, _NPX, 6])
        x = f[:,:,0]
        z = f[:,:,2]
        u = f[:,:,3]
        v = f[:,:,4]
        w = f[:,:,5]
        x_phase = x_phase + x[:,67:115]
        z_phase = z_phase +z[:,67:115]
        u_phase = u_phase + u[:,67:115]
        v_phase = v_phase + v[:,67:115]
        w_phase = w_phase + w[:,67:115]
        #uu_phase = uu_phase + u_phase**2
        #vv_phase = vv_phase +  v_phase**2
        #ww_phase =  ww_phase + w_phase**2
        #uw_phase =  uw_phase + u_phase*w_phase
    #time average
    x_phase = x_phase / int((tie - tis) / tii + 1)
    z_phase = z_phase / int((tie - tis) / tii + 1)
    u_phase = u_phase / int((tie - tis) / tii + 1)
    v_phase = v_phase / int((tie - tis) / tii + 1)
    w_phase = w_phase / int((tie - tis) / tii + 1)
    #uu_phase = uu_phase / int((tie - tis) / tii + 1)
    #vv_phase = vv_phase / int((tie - tis) / tii + 1)
    #ww_phase = ww_phase / int((tie - tis) / tii + 1)
    #uw_phase = uw_phase / int((tie - tis) / tii + 1)
    for it in range (nti):
        ti = tis + tii * it
        fname = 'Phase_Average_Phi{:01d}_{:04d}_{:08d}.dat'.format(_phi,t,ti)
        f = tec.tecplot_reader(fname, [_NPZ, _NPX, 6], 2)
        f = f.reshape([_NPZ, _NPX, 6])
        x = f[:,:,0]
        z = f[:,:,2]
        u = f[:,:,3]
        v = f[:,:,4]
        w = f[:,:,5]
        uu_phase = uu_phase + (u[:,67:115] - u_phase)**2
        vv_phase = vv_phase + (v[:,67:115] - v_phase)**2
        ww_phase = ww_phase + (w[:,67:115] - w_phase)**2
        uw_phase = uw_phase + (u[:,67:115] - u_phase)*(w[:,67:115] - w_phase)

    uu_phase = uu_phase / nti
    vv_phase = vv_phase / nti
    ww_phase = ww_phase / nti
    uw_phase = uw_phase / nti

    #reshape data
    x_phase = x_phase.reshape([_NPZ*48])
    z_phase = z_phase.reshape([_NPZ*48])
    u_phase = u_phase.reshape([_NPZ*48])
    v_phase = v_phase.reshape([_NPZ*48])
    w_phase = w_phase.reshape([_NPZ*48])
    uu_phase = uu_phase.reshape([_NPZ*48]) 
    vv_phase = vv_phase.reshape([_NPZ*48]) 
    ww_phase = ww_phase.reshape([_NPZ*48]) 
    uw_phase = uw_phase.reshape([_NPZ*48]) 
    #store data into array
    data = np.zeros([_NPZ*48, 9])
    data[:,0] = x_phase
    data[:,1] = z_phase
    data[:,2] = u_phase*_U/_Ustar
    data[:,3] = v_phase*_U/_Ustar
    data[:,4] = w_phase*_U/_Ustar
    data[:,5] = uu_phase*((_U/_Ustar)**2)
    data[:,6] = vv_phase*((_U/_Ustar)**2)
    data[:,7] = ww_phase*((_U/_Ustar)**2)
    data[:,8] = uw_phase*((_U/_Ustar)**2)
    #save data
    return data
def get_phi(folder, t, tis, tie, tii,_NPZ,_NPX):
    #change working directory
    os.chdir(folder)
    print("current working directory is: {0}".format(os.getcwd()))
    #read data
    x_phase = np.zeros([_NPZ, 48])
    z_phase = np.zeros([_NPZ, 48])
    u_phase = np.zeros([_NPZ, 48])
    v_phase = np.zeros([_NPZ, 48])
    w_phase = np.zeros([_NPZ, 48])
    uu_phase = np.zeros([_NPZ, 48])
    vv_phase = np.zeros([_NPZ, 48])
    ww_phase = np.zeros([_NPZ, 48])
    uw_phase = np.zeros([_NPZ, 48])
    nti = int((tie - tis) / tii + 1)
    for it in range (nti):
        ti = tis + tii * it
        fname = 'POST_U_2D3_{:010d}_{:04d}.dat'.format(ti,t)
        f = tec.tecplot_reader(fname, [_NPZ, _NPX, 6], 2)
        f = f.reshape([_NPZ, _NPX, 6])
        x = f[:,:,0]
        z = f[:,:,2]
        u = f[:,:,3]
        v = f[:,:,4]
        w = f[:,:,5]
        x_phase = x_phase + x[:,67:115]
        z_phase = z_phase + z[:,67:115]
        u_phase = u_phase + u[:,67:115]
        v_phase = v_phase + v[:,67:115]
        w_phase = w_phase + w[:,67:115]

    #time average
    x_phase = x_phase / int((tie - tis) / tii + 1)
    z_phase = z_phase / int((tie - tis) / tii + 1)
    u_phase = u_phase / int((tie - tis) / tii + 1)
    v_phase = v_phase / int((tie - tis) / tii + 1)
    w_phase = w_phase / int((tie - tis) / tii + 1)

    for it in range (nti):
        ti = tis + tii * it
        fname = 'POST_U_2D3_{:010d}_{:04d}.dat'.format(ti,t)
        f = tec.tecplot_reader(fname, [_NPZ, _NPX, 6], 2)
        f = f.reshape([_NPZ, _NPX, 6])
        x = f[:,:,0]
        z = f[:,:,2]
        u = f[:,:,3]
        v = f[:,:,4]
        w = f[:,:,5]
        uu_phase = uu_phase + (u[:,67:115] - u_phase)**2
        vv_phase = vv_phase + (v[:,67:115] - v_phase)**2
        ww_phase = ww_phase + (w[:,67:115] - w_phase)**2
        uw_phase = uw_phase + (u[:,67:115] - u_phase)*(w[:,67:115] - w_phase)

    uu_phase = uu_phase / nti
    vv_phase = vv_phase / nti
    ww_phase = ww_phase / nti
    uw_phase = uw_phase / nti
    #reshape data
    x_phase = x_phase.reshape([_NPZ*48])
    z_phase = z_phase.reshape([_NPZ*48])
    u_phase = u_phase.reshape([_NPZ*48])
    v_phase = v_phase.reshape([_NPZ*48])
    w_phase = w_phase.reshape([_NPZ*48])
    uu_phase = uu_phase.reshape([_NPZ*48]) - u_phase**2
    vv_phase = vv_phase.reshape([_NPZ*48]) - v_phase**2
    ww_phase = ww_phase.reshape([_NPZ*48]) - w_phase**2
    uw_phase = uw_phase.reshape([_NPZ*48]) - u_phase*w_phase
    #store data into array
    data = np.zeros([_NPZ*48, 9])
    data[:,0] = x_phase
    data[:,1] = z_phase
    data[:,2] = u_phase
    data[:,3] = v_phase
    data[:,4] = w_phase
    data[:,5] = uu_phase
    data[:,6] = vv_phase
    data[:,7] = ww_phase
    data[:,8] = -uw_phase
    #save data
    return data
