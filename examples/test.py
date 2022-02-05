#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 12:13:05 2022

@author: dboateng

Replace many of the codes with function....I am keeping it since I was just trying the individual model outputs
"""

import sys
sys.path.append("/home/dboateng/Python_scripts/TrajView") 

from package.traj import Tra
from package.traj_plot import Mapfigure, CartoFigure
import os 
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs

# User specifications 
main_path="/home/dboateng/source_codes/lagranto/new/"

exp_name_AW100E100 = "a002"
exp_name_AW100E0 = "a003"
exp_name_AW100E200 = "a001"
exp_name_AW200E100 = "a009"
exp_name_AW200E0 = "a010"
exp_name_AW200E200 = "t017"

loc_1 = "Bologna"
lat_1 = 44.49
lon_1 = 11.38
varname = "p"

AW100E100_path_june = os.path.join(main_path, exp_name_AW100E100, "June", "Trace", loc_1)
AW100E100_path_july = os.path.join(main_path, exp_name_AW100E100, "July", "Trace", loc_1)
AW100E100_path_august = os.path.join(main_path, exp_name_AW100E100, "August", "Trace", loc_1)

AW100E0_path_june = os.path.join(main_path, exp_name_AW100E0, "June", "Trace", loc_1)
AW100E0_path_july = os.path.join(main_path, exp_name_AW100E0, "July", "Trace", loc_1)
AW100E0_path_august = os.path.join(main_path, exp_name_AW100E0, "August", "Trace", loc_1)

AW100E200_path_june = os.path.join(main_path, exp_name_AW100E200, "June", "Trace", loc_1)
AW100E200_path_july = os.path.join(main_path, exp_name_AW100E200, "July", "Trace", loc_1)
AW100E200_path_august = os.path.join(main_path, exp_name_AW100E200, "August", "Trace", loc_1)

AW200E100_path_june = os.path.join(main_path, exp_name_AW200E100, "June", "Trace", loc_1)
AW200E100_path_july = os.path.join(main_path, exp_name_AW200E100, "July", "Trace", loc_1)
AW200E100_path_august = os.path.join(main_path, exp_name_AW200E100, "August", "Trace", loc_1)

AW200E0_path_june = os.path.join(main_path, exp_name_AW200E0, "June", "Trace", loc_1)
AW200E0_path_july = os.path.join(main_path, exp_name_AW200E0, "July", "Trace", loc_1)
AW200E0_path_august = os.path.join(main_path, exp_name_AW200E0, "August", "Trace", loc_1)

AW200E200_path_june = os.path.join(main_path, exp_name_AW200E200, "June", "Trace", loc_1)
AW200E200_path_july = os.path.join(main_path, exp_name_AW200E200, "July", "Trace", loc_1)
AW200E200_path_august = os.path.join(main_path, exp_name_AW200E200, "August", "Trace", loc_1)




files = ["wcb_1.1", "wcb_2.1", "wcb_3.1", "wcb_4.1", "wcb_5.1","wcb_6.1", "wcb_7.1", "wcb_8.1","wcb_9.1", "wcb_10.1"]


# combining trajectories
#AW100E100 
file = os.path.join(AW100E100_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E100_path_june, i)) for i in files]
AW100E100_June_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW100E100_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E100_path_july, i)) for i in files]
AW100E100_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW100E100_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E100_path_august, i)) for i in files]
AW100E100_August_Trajs = trajs.concatenate(trajs_add)



#AW100E0
file = os.path.join(AW100E0_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E0_path_june, i)) for i in files]
AW100E0_June_Trajs = trajs.concatenate(trajs_add)

ile = os.path.join(AW100E0_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E0_path_july, i)) for i in files]
AW100E0_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW100E0_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW100E0_path_august, i)) for i in files]
AW100E0_August_Trajs = trajs.concatenate(trajs_add)


#AW100E200
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


#AW200E200
file = os.path.join(AW200E200_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E200_path_june, i)) for i in files]
AW200E200_June_Trajs = trajs.concatenate(trajs_add)

ile = os.path.join(AW200E200_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E200_path_july, i)) for i in files]
AW200E200_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW200E200_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E200_path_august, i)) for i in files]
AW200E200_August_Trajs = trajs.concatenate(trajs_add)


#AW200E100
file = os.path.join(AW200E100_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E100_path_june, i)) for i in files]
AW200E100_June_Trajs = trajs.concatenate(trajs_add)

ile = os.path.join(AW200E100_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E100_path_july, i)) for i in files]
AW200E100_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW200E100_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E100_path_august, i)) for i in files]
AW200E100_August_Trajs = trajs.concatenate(trajs_add)


#AW200E0
file = os.path.join(AW200E0_path_june, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E0_path_june, i)) for i in files]
AW200E0_June_Trajs = trajs.concatenate(trajs_add)

ile = os.path.join(AW200E0_path_july, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E0_path_july, i)) for i in files]
AW200E0_July_Trajs = trajs.concatenate(trajs_add)

file = os.path.join(AW200E0_path_august, files[0])
trajs = Tra(file)
trajs_add = [Tra(os.path.join(AW200E0_path_august, i)) for i in files]
AW200E0_August_Trajs = trajs.concatenate(trajs_add)




plt.rcParams.update({'font.size': 18, "font.weight":"semibold", "lines.markersize":18})

path_to_store = os.path.join("/home/dboateng/Model_output_pst/", "plots")

levels = np.linspace(700, 900, 22)
cmap = "Spectral"
projection = ccrs.PlateCarree()
cbar_pos = [0.90, 0.30, 0.03, 0.45]


# #AW100E100
fig, ((ax1,ax2),(ax3, ax4), (ax5,ax6)) = plt.subplots(nrows = 3, ncols = 2, figsize=(20,18), subplot_kw={"projection": projection})

cbar_ax = fig.add_axes(cbar_pos)   # axis for subplot colorbar # left, bottom, width, height
cbar_ax.get_xaxis().set_visible(False)
cbar_ax.yaxis.set_ticks_position('right')
cbar_ax.set_yticklabels([])
cbar_ax.tick_params(size=0)

#CTL
m = CartoFigure(ax=ax1, projection=projection, extent=[-38,20,30,65], resolution="50m", bottom_labels=False)
ax1.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW100E100_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E100_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E100_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax1.set_title("[A]   CTL", fontsize=20, weight="bold", loc="left")

#W1E0
m = CartoFigure(ax=ax3, projection=projection, extent=[-38,20,30,65], resolution="50m", bottom_labels=False)
ax3.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW100E0_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E0_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E0_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax3.set_title("[C]   W1E0", fontsize=20, weight="bold", loc="left")

#W1E2
m = CartoFigure(ax=ax5, projection=projection, extent=[-38,20,30,65], resolution="50m",)
ax5.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW100E200_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E200_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW100E200_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax5.set_title("[E]   W1E2", fontsize=20, weight="bold", loc="left")

#W2E1
m = CartoFigure(ax=ax2, projection=projection, extent=[-38,20,30,65], resolution="50m", bottom_labels=False,
                left_labels=False)
ax2.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW200E100_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E100_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E100_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax2.set_title("[B]   W2E1", fontsize=20, weight="bold", loc="left")

#W2E0
m = CartoFigure(ax=ax4, projection=projection, extent=[-38,20,30,65], resolution="50m", bottom_labels=False,
                left_labels=False)
ax4.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW200E0_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E0_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E0_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax4.set_title("[D]   W2E0", fontsize=20, weight="bold", loc="left")

#W2E0
m = CartoFigure(ax=ax6, projection=projection, extent=[-38,20,30,65], resolution="50m", left_labels=False)
ax6.scatter(lon_1, lat_1, marker=(5, 0), color=("black"),)
p =m.plot_trajs(AW200E200_June_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E200_July_Trajs, variable=varname, levels=levels, cmap=cmap)
m.plot_trajs(AW200E200_August_Trajs, variable=varname, levels=levels, cmap=cmap)
ax6.set_title("[D]   W2E2", fontsize=20, weight="bold", loc="left")


cb = plt.colorbar(p, drawedges=True, 
                  pad=0.15, shrink= 0.30, format= "%.0f", extend= "both", cax=cbar_ax)
cb.set_label("Pressure [hPa]", size=20, fontweight= "bold")

#fig.canvas.draw() 
plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.89, top=0.94, bottom=0.06)
plt.savefig(os.path.join(path_to_store, "fig9.svg"), format= "svg", bbox_inches="tight", dpi=600)

plt.show()                              
