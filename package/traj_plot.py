#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:36:40 2022

@author: dboateng
"""

# importing modules 
import datetime
from functools import partial
import numpy as np 
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
import numpy as np
from cartopy import crs as ccrs
from cartopy import feature as cfeature
from cartopy.mpl.geoaxes import GeoAxes, GeoAxesSubplot
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm
from matplotlib.pyplot import get_cmap
from matplotlib.pyplot import subplot

def plot_trajs(ax, trajs, variable, cmap='Spectral', levels=None, **kwargs):
    """Plot trajectories on axis

    Parameters
    ----------
    ax:
    trajs: Tra (from dypy.lagranto) object
    variable: string
    cmap: string
    levels: ndarray
    transform: CRS (Coordinate Reference System) object, default ccrs.Geodetic()
    kwargs: dict,
        passed to LineCollection

    Examples
    --------

    >>>    from cartopy import crs as ccrs
    >>>    fig = plt.figure()
    >>>    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=45))
    >>>    lc = plot_trajs(ax, trajs, 'z')

    """
    segments, colors = list(zip(*
                                [(_get_segments(traj),
                                  traj[variable][:-1])
                                 for traj in trajs])
                           )
    segments = np.concatenate(segments)
    colors = np.concatenate(colors)
    cmap = get_cmap(cmap)
    if levels is None:
        minlev = np.nanmin(trajs[variable])
        maxlev = np.nanmax(trajs[variable])
        levels = np.linspace(minlev, maxlev, 20)
    norm = BoundaryNorm(levels, cmap.N)
    nkwargs = {'array': colors,
               'cmap': cmap,
               'norm': norm}
    if isinstance(ax, GeoAxes):
        nkwargs['transform'] = ccrs.Geodetic()
    nkwargs.update(kwargs)
    lc = LineCollection(segments, **nkwargs)

    ax.add_collection(lc)

    return lc

def _get_segments(trajs):
    lon, lat = trajs['lon'], trajs['lat']
    points = np.array([lon, lat]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    # remove all segments crossing the 180th meridian !! to be improved
    # diff = segments[:, 0, 0] - segments[:, 1, 0]
    # maxval = abs(self.m(-179, 0)[0] - self.m(179, 0)[0])
    # index = np.where((diff < maxval) & (diff > -maxval))
    return segments  # [index[0], :, :]



class Mapfigure:
    """
        Class based on Basemap with additional functionality
        such as plot_trajectories
    """

    def __init__(
        self,
        resolution="i",
        projection="cyl",
        domain=None,
        lon=None,
        lat=None,
        basemap=None,
        **kwargs
    ):

        if basemap is None:
            if (domain is None) & (lon is not None):
                domain = [lon.min(), lon.max(), lat.min(), lat.max()]
            if projection == "eqc":
                projection = "cyl"
            if domain is not None:
                kwargs["llcrnrlon"] = domain[0]
                kwargs["urcrnrlon"] = domain[1]
                kwargs["llcrnrlat"] = domain[2]
                kwargs["urcrnrlat"] = domain[3]
            kwargs["resolution"] = resolution
            kwargs["projection"] = projection
            self.m = Basemap(**kwargs)
        else:
            self.m = basemap
        if lon is not None:
            self.x, self.y = self.m(lon, lat)

    def __getattr__(self, item):
        return getattr(self.m, item)

    def __call__(self, *args, **kwargs):
        return self.m(*args, **kwargs)

    def __dir__(self):
        return self.m.__dir__() + ["drawmap", "plot_traj"]

    def drawmap(
        self,
        continent=False,
        nbrem=10,
        nbrep=10,
        coastargs={},
        countryargs={},
        meridiansargs={},
        parallelsargs={},
    ):
        """
        draw basic features on the map
        nbrem: interval bewteen meridians
        nbrep: interval between parallels
        """
        self.drawcoastlines(**coastargs)
        self.drawcountries(**countryargs)
        merid = np.arange(-180, 180, nbrem)
        parall = np.arange(-90, 90, nbrep)
        self.drawmeridians(merid, labels=[0, 0, 0, 1], **meridiansargs)
        self.drawparallels(parall, labels=[1, 0, 0, 0], **parallelsargs)
        if continent:
            self.fillcontinents(color="lightgrey")

    def plot_traj(self, trajs, variable, cmap="Spectral", levels=None, **kwargs):
        """Plot trajectories on a map

        Usage:
            m = Mapfigure(domain=[5, 15, 40, 50])
            m.drawmap()
            m.plot_traj(trajs, 'QV')
        """
        if self.ax is None:
            self.ax = subplot()
        lon, lat = trajs["lon"].copy(), trajs["lat"].copy()
        lonnanvalues = np.isnan(lon)
        latnanvalues = np.isnan(lat)
        x, y = self.m(trajs["lon"], trajs["lat"])
        # m() does not account for nan values
        x[lonnanvalues] = np.nan
        y[latnanvalues] = np.nan
        trajs["lon"] = x
        trajs["lat"] = y
        lc = plot_trajs(self.ax, trajs, variable, cmap=cmap, levels=levels, **kwargs)
        trajs["lon"] = lon
        trajs["lat"] = lat
        return lc
    
    
class CartoFigure:
    """Wrapper to create maps based on cartopy
    """

    default_projection = ccrs.PlateCarree()
    default_extent = [0, 20, 40, 60]
    default_resolution = '50m'

    def __init__(self, ax=None, projection=None, extent=None, resolution=None,
                 **kwargs):
        """

        Parameters
        ----------
        ax: matplotlib.Axes
            If given use it to define the position the GeoAx
        projection: cartopy.crs
            projection to override the default projection PlateCarree
        extent: list
            list defining the domain extent;
            [minlon, maxlon, minlat, maxlat];
            default is [0, 20, 40, 60]
        resolution: string
            resolution to use for plotting the boundaries;
            default 50m;
            available: 10m, 50m, 110m
        kwargs: Keyword arguments
            Keyword arguments to pass to plt.axes
        """
        self.projection = projection if projection else self.default_projection
        self.extent = extent if extent else self.default_extent
        self.resolution = resolution if resolution else self.default_resolution
        if ax:
            self.ax = plt.axes(ax.get_position(), projection=self.projection,
                               **kwargs)
            ax.set_visible(False)
        else:
            self.ax = plt.axes(projection=self.projection, **kwargs)
        if self.extent is not None:
            self.ax.set_extent(self.extent)

    def __getattr__(self, item):
        return getattr(self.ax, item)

    def __dir__(self):
        return self.ax.__dir__() + ['drawmap', 'plot_trajs']

    def drawmap(self):
        """Draw the land feature

        Add from NaturalEarth the admin_0_countries
        """
        land = cfeature.NaturalEarthFeature('cultural', 'admin_0_countries',
                                            self.resolution, edgecolor='gray',
                                            facecolor='none', linewidth=0.5)
        self.ax.add_feature(land)

    def plot_trajs(self, trajs, variable='', **kwargs):
        """Plot trajectories on the map"""
        variable = variable if variable else trajs.variables[-1]
        kwargs['variable'] = variable
        return plot_trajs(self.ax, trajs, **kwargs)


