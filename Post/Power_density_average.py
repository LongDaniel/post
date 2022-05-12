#import library
import numpy as np
import pandas as pd
import os
#function get power_density_average
#require working directory and return power density average
#input: path
#output: power density average
def power_density_average(path,_nturbine,_dt,_Sx,_Sy,_D):
  #Declare working directory
  os.chdir(path)
  print(os.getcwd())
      #Clean data
  fid = open('log.uref','r')
  content=fid.readlines()
  # Turbine_           1 :angvel=   50.735637598099999      , TSR=   4.4059452767309510      , Uref=  0.86364504796591524
  196034763     

  nline = len(content)
  nt = nline / _nturbine
  data=np.zeros((nline,4))

  for i in range(int(nt)):
    for j in range(_nturbine):
      i2 = _nturbine * i + j
      value=content[i2].split()
      #print(value)
      data[i2,0]=(i+1)*_dt
      data[i2,1]=value[3] # angvel
      data[i2,2]=value[6] # TSR
      data[i2,3]=value[9] # Uref
  fid.close()

  np.savetxt('uref.dat', data)
  fid = open('log.cthrust','r')
  content=fid.readlines()
  # Thrust=  0.10233803188671066      , Torque=   6.1668522808625047E-003 , C_Thrust=  0.38109671967396186      , Power=   6.3533464098887757E-002 , C_Power=  0.12840488196034763     

  nline = len(content)
  nt = nline / _nturbine
  data=np.zeros((int(_nturbine*nt),6))

  for i in range(int(nt)):
    for j in range(_nturbine):
      i2 = _nturbine * i + j
      value=content[i2].split()
      #print(value)
      data[i2,0]=(i+1)*_dt # time
      data[i2,1]=value[1] # thrust
      data[i2,2]=value[4] # torque
      data[i2,3]=value[7] # c_thrust
      data[i2,4]=value[10] # power
      data[i2,5]=float(value[13])*1.0 # c_power
  fid.close()

  np.savetxt('coeff.dat', data)
  #Data Frame
  data = pd.read_csv('coeff.dat', sep = '\s+', header = None)
  data = pd.DataFrame(data)
  x = data[4] #Turbine power
  #rearrange series to array multidimensional
  x = np.array(x)
  x = x.reshape([int(nt), _nturbine])

  #calculate power density
  power_density = x/(_Sx*_Sy*_D)
  power_density_average = np.mean(power_density, axis = 1)
  return power_density_average

#function get time variable
#require working directory and return time variable
#input: path
#output: time variable
def get_time(path,_nturbine,_T_turb):
    os.chdir(path)
    data = pd.read_csv('coeff.dat', sep = '\s+', header = None)
    data = pd.DataFrame(data)
    x = data[0]
    time = []
    #Normalized time variable
    for i in range(0, int(len(x)), _nturbine):
      #time.append(x[i]*(U/H_hub))
      time.append(x[i]/_T_turb)           #Using T_turb
    return time
