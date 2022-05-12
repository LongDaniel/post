import os
import numpy as np
from Power_density_average import power_density_average
from Power_density_average import get_time


#parameters
#Declare some variable 
nturbinex = 4
nturbiney = 4
nturbine = 16
#Diameter of turbine
D = 80
#Other variable
Sx = 7
Sy = 7
#kappa = 0.4
#nu = 1.511e-5
#PEX = 1.45444104333
#PEY = 8.72664625997
#hbar = 0.46
#uinfty = 2.54390548295
dt = 0.2941315855
#Rotational angular period
T_turb = 42.84
U_star = 0.356
H_hub = 70
#Mean finite velocity
U = 11.5258407161
tis = 100
tie = 15000
tii = 100
nti = int((tie - tis) / tii + 1)
NPX = 192
NPY = 192
NPZ = 65
path  = 'd:\post'
os.chdir(path)
#delare working casename
casenames = [ "Pitch_test", "Wave_no"]
unametags = ["U", "UI", "UI"]
tis = 200
tie = 15000
tii = 100
casename_s = 0
casename_e = 2
for icase in range(casename_s, casename_e):
    foldername = "./"+casenames[icase]
    #change working directory
    #os.chdir(path+foldername)

    #create dynamic variables
    globals()["{casenames[icase]}"] = power_density_average\
                                        (path+foldername,nturbine,dt,Sx,Sy,D)
    #checked
    print(os.getcwd())    
time = get_time(path+"./"+casenames[0],nturbine,T_turb)
data = np.zeros((len(time),int(casename_e-casename_s+1)))
data [:,0] = time
for icase in range(casename_s, casename_e):
    data[:, int(icase+1)] = globals()["{casenames[icase]}"]


outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
print("Current working directory: {0}".format(os.getcwd()))

f = open( outputfolder + "Power density average.plt",'w')
f.write("VARIABLES = t/T, Pitch, Noway  \n")
np.savetxt(f, data)
f.close()