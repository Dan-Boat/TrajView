#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 12:13:05 2022

@author: dboateng
"""

import sys
sys.path.append("/home/dboateng/Python_scripts/TrajView") 

from package.traj import Tra
from package.traj_plot import Mapfigure
import os 
import matplotlib.pyplot as plt
import numpy as np

# User specifications 
main_path="/home/dboateng/source_codes/lagranto/new/"

exp_name_AW100E100 = "a002"
exp_name_AW100E0 = "a003"
exp_name_AW100E200 = "a001"

loc_1 = "Lyon"
lat_1 = 45.81
lon_1 = 4.82
varname = "p"

# AW100E100_path_june = os.path.join(main_path, exp_name_AW100E100, "June", "Trace", loc_1)
# AW100E100_path_july = os.path.join(main_path, exp_name_AW100E100, "July", "Trace", loc_1)
# AW100E100_path_august = os.path.join(main_path, exp_name_AW100E100, "August", "Trace", loc_1)

# AW100E0_path_june = os.path.join(main_path, exp_name_AW100E0, "June", "Trace", loc_1)
# AW100E0_path_july = os.path.join(main_path, exp_name_AW100E0, "July", "Trace", loc_1)
# AW100E0_path_august = os.path.join(main_path, exp_name_AW100E0, "August", "Trace", loc_1)

AW100E200_path_june = os.path.join(main_path, exp_name_AW100E200, "June", "Trace", loc_1)
AW100E200_path_july = os.path.join(main_path, exp_name_AW100E200, "July", "Trace", loc_1)
AW100E200_path_august = os.path.join(main_path, exp_name_AW100E200, "August", "Trace", loc_1)


files = ["wcb_1.1", "wcb_2.1", "wcb_3.1", "wcb_4.1", "wcb_5.1","wcb_6.1", "wcb_7.1", "wcb_8.1","wcb_9.1", "wcb_10.1"]


# combining trajectories 
# file = os.path.join(AW100E100_path_june, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E100_path_june, i)) for i in files]
# AW100E100_June_Trajs = trajs.concatenate(trajs_add)

# file = os.path.join(AW100E100_path_july, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E100_path_july, i)) for i in files]
# AW100E100_July_Trajs = trajs.concatenate(trajs_add)

# file = os.path.join(AW100E100_path_august, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E100_path_august, i)) for i in files]
# AW100E100_August_Trajs = trajs.concatenate(trajs_add)




# file = os.path.join(AW100E0_path_june, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E0_path_june, i)) for i in files]
# AW100E0_June_Trajs = trajs.concatenate(trajs_add)

# ile = os.path.join(AW100E0_path_july, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E0_path_july, i)) for i in files]
# AW100E0_July_Trajs = trajs.concatenate(trajs_add)

# file = os.path.join(AW100E0_path_august, files[0])
# trajs = Tra(file)
# trajs_add = [Tra(os.path.join(AW100E0_path_august, i)) for i in files]
# AW100E0_August_Trajs = trajs.concatenate(trajs_add)



file = os.path.join(AW100E200_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E200_path_june, i)) for i in files]
AW100E200_June_Trajs = trajs.concatenate(trajs_add)

ile = os.path.join(AW100E200_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E200_path_july, i)) for i in files]
AW100E200_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW100E200_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E200_path_august, i)) for i in files]
AW100E200_August_Trajs = trajs.concatenate(trajs_add)



#cat = CartoFigure()
#cat.plot_trajs(trajs0, variable="p")
plt.rcParams.update({'font.size': 18, "font.weight":"semibold", "lines.markersize":18})

path_to_store = "/home/dboateng/Model_output_pst/plots/Trajs"

# fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(20,15))

# levels = np.linspace(600, 1000, 22)
# m = Mapfigure(width=10000000,height=6500000,
#         resolution='l',projection='laea',\
#         lat_ts=50,lat_0=52,lon_0=0., ax=ax1)
# m.drawmap(nbrem=10, nbrep=10) 
# #m.shadedrelief()
# m.scatter(lon_1, lat_1, latlon=True, marker=(5, 0), color=("black"),)

# p =m.plot_traj(AW100E100_June_Trajs, variable=varname, levels=levels)
# m.plot_traj(AW100E100_July_Trajs, variable=varname, levels=levels)
# m.plot_traj(AW100E100_August_Trajs, variable=varname, levels=levels)
# cb = m.colorbar(p, drawedges=True, 
#                   pad=0.15, shrink= 0.50, format= "%.0f", extend= "both",)
# cb.set_label("Pressure [hPa]", size=20, fontweight= "bold")
# plt.title("AW100E100")
# plt.tight_layout()
# plt.subplots_adjust(left=0.05, right=0.89, top=0.94, bottom=0.06)
# plt.savefig(os.path.join(path_to_store, loc_1 + "_AW100E100.svg"), format= "svg", bbox_inches="tight", dpi=600)


                                 
# fig2, ax2 = plt.subplots(nrows = 1, ncols = 1, figsize=(20,15))

# levels = np.linspace(800, 1000, 20)
# m = Mapfigure(width=10000000,height=6500000,
#         resolution='l',projection='laea',\
#         lat_ts=50,lat_0=52,lon_0=0., ax=ax2)
# m.drawmap(nbrem=10, nbrep=10) 
# #m.shadedrelief()
# m.scatter(lon_1, lat_1, latlon=True, marker=(5, 0), color=("black"),)

# p =m.plot_traj(AW100E0_June_Trajs, variable=varname, levels=levels)
# m.plot_traj(AW100E0_July_Trajs, variable=varname, levels=levels)
# m.plot_traj(AW100E0_August_Trajs, variable=varname, levels=levels)
# cb = m.colorbar(p, drawedges=True, 
#                   pad=0.15, shrink= 0.50, format= "%.0f", extend= "neither",)
# cb.set_label("Pressure [hPa]", size=20, fontweight= "bold")
# plt.title("AW100E0")
# plt.tight_layout()
# plt.subplots_adjust(left=0.05, right=0.89, top=0.94, bottom=0.06)
# plt.savefig(os.path.join(path_to_store, loc_1 + "_AW100E0.svg"), format= "svg", bbox_inches="tight", dpi=600)



fig3, ax3 = plt.subplots(nrows = 1, ncols = 1, figsize=(20,15))

levels = np.linspace(700, 900, 20)
m = Mapfigure(width=9000000,height=6500000,
        resolution='l',projection='laea',\
        lat_ts=50,lat_0=52,lon_0=0., ax=ax3)
m.drawmap(nbrem=10, nbrep=10) 
#m.shadedrelief()
m.scatter(lon_1, lat_1, latlon=True, marker=(5, 0), color=("black"),)

p =m.plot_traj(AW100E200_June_Trajs, variable=varname, levels=levels)
m.plot_traj(AW100E200_July_Trajs, variable=varname, levels=levels)
m.plot_traj(AW100E200_August_Trajs, variable=varname, levels=levels)
cb = m.colorbar(p, drawedges=True, 
                  pad=0.15, shrink= 0.30, format= "%.0f", extend= "both",)
cb.set_label("Pressure [hPa]", size=20, fontweight= "bold")
plt.title("AW100E200")
plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.89, top=0.94, bottom=0.06)
#plt.savefig(os.path.join(path_to_store, loc_1 + "_AW100E200.svg"), format= "svg", bbox_inches="tight", dpi=600)

plt.show()
  