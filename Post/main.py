import os
import numpy as np
from power_density_average import power_density_average
from power_density_average import get_time
from phase_average import get_phi
from mean_velocity import get_mean_velocity
from mean_velocity import get_z_coordinate
from budget import get_mkeb_wt
from budget import get_tau_sum
from budget import get_um
from budget import get_z

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
#dt = 0.68543297937
#dt = 0.3150659270689523
#Rotational angular period
T_turb = 42.84
T_wave = 126.02637082758092 
#T_wave = 14.7065792758511
#U_star = 0.356
H_hub = 70
#Mean finite velocity
U = 11.5258407161
U_star = 0.421
tis = 200
tie = 15000
tii = 200
nti = int((tie - tis) / tii + 1)
NPX = 192
NPY = 192
NPZ = 64
path  = 'd:\post\Project'
os.chdir(path)
#delare working casename
casenames = ["Pitch_Turbine"]
unametags = ["U", "UI", "UI"]
casename_s = 0
casename_e = 1
for icase in range(casename_s, casename_e):
    foldername = "./"+casenames[icase]
    #change working directory
    #os.chdir(path+foldername)

    #create dynamic variables
    globals()["{casenames[icase]}"] = power_density_average\
                                        (path+foldername,nturbine,dt,Sx,Sy,D)
    #checked
    print(os.getcwd())
    print(len(globals()["{casenames[icase]}"]))    
    time = get_time(path+"./"+casenames[icase],nturbine,T_wave)
    print(len(time))
    data = np.zeros((len(time),int(casename_e-casename_s+1)))
    data [:,0] = time
    for icase in range(casename_s, casename_e):
        data[:, int(icase+1)] = globals()["{casenames[icase]}"]


outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
print("Current working directory is: {0}".format(os.getcwd()))

f = open( outputfolder + "Power density average.plt",'w')
f.write("VARIABLES = t/T, Fixed  \n")
np.savetxt(f, data)
f.close()

data1 = get_phi(path+foldername+'\POST_U_2D3_0001', 1, 10000, 15000, 200, NPZ, NPX,U,U_star)
data2 = get_phi(path+foldername+'\POST_U_2D3_0002', 2, 10000, 15000, 200, NPZ, NPX,U,U_star)
data3 = get_phi(path+foldername+'\POST_U_2D3_0003', 3, 10000, 15000, 200, NPZ, NPX,U,U_star)
data4 = get_phi(path+foldername+'\POST_U_2D3_0004', 4, 10000, 15000, 200, NPZ, NPX,U,U_star)
#aveage data
data = np.zeros([NPZ*48, 10])
data = (data1 + data2 + data3 + data4)/4

os.chdir('d:\post')
outputfolder = 'post_result/'
#create output folder named 'post_result' 
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)
f = open('d:\post' + './'+ outputfolder + casenames[0]+ "phase_contour.plt",'w')
f.write("VARIABLES = X, Z, <U>/U*, <V>/U*, <W>/W*, UU/U*^2, VV/U*^2,\
         WW/U*^2, UW/U*^2, tke_tm  \n")

np.savetxt(f, data)
f.close()

dat = np.zeros((NPZ,7))
dat[:,0] = get_z_coordinate(path+foldername,tis)/H_hub
dat[:,1:4] = (get_mean_velocity(path+foldername,tis,tie,tii)*U)#/U_star
dat[:,4] = get_mkeb_wt(path+foldername,NPZ)
dat[:,5] = get_tau_sum(path+foldername,NPZ)
dat[:,6] = get_um(path+foldername,NPZ)

f1 = open( 'd:\post'+'./' + outputfolder + './' + casenames[0]+"phase_test_code.plt",'w')
f1.write("VARIABLES = Z, <U>, <V>, <W>, mkeb_wt, tau_sum,um \n")
         
np.savetxt(f1, dat)
f1.close()
print("End process directory: {0}".format(os.getcwd()) )