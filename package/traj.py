#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:28:37 2022

@author: dboateng
"""
from datetime import datetime, timedelta
from functools import partial
from functools import wraps
from multiprocessing.pool import Pool
from tempfile import mkdtemp
from warnings import warn

import numpy as np
from path import Path

from .traj_utils import from_netcdf, to_ascii, from_ascii, to_netcdf


class Tra(object):
    """Class to work with LAGRANTO out.

    Read trajectories from a LAGRANTO file and return a structured numpy array

    Parameters
    ----------
        filename : string
            File containing lagranto trajectories
        usedatetime: bool
            Read times as datetime objects, default True
        array: structured array
            If defined creates a new Tra object filled with the array

    Returns
    -------
        structured array (Tra): trajs(ntra,ntime) with variables as tuple.

    Examples
    --------

    >>>    filename = 'mylslfile.nc'
    >>>    trajs = Tra()
    >>>    trajs.load_netcdf(filename)
    >>>    trajs['lon'][0,:]  # return the longitudes for the first trajectory.

    >>> trajs = Tra(filename)
    >>> selected_trajs = Tra(array=trajs[[10, 20, 30], :])


    """

    _startdate = None

    def __init__(self, filename='', usedatetime=True, array=None, **kwargs):
        """Initialized a Tra object.

        If filename is given, try to load it directly;
        Arguments to the load function can be passed as key=value argument.
        """
        typefile = kwargs.pop('typefile', None)
        if typefile is not None:
            msg = 'typefile is not used anymore;' \
                  'it will be remove in futur version'
            raise DeprecationWarning(msg)
        if not filename:
            if array is None:
                self._array = None
            else:
                self._array = array
            return

        try:
            self.load_netcdf(filename, usedatetime=usedatetime, **kwargs)
        except (OSError, IOError, RuntimeError):
            try:
                self.load_ascii(filename, usedatetime=usedatetime, **kwargs)
            except Exception:
                raise IOError("Unkown fileformat. Known formats " 
                              "are ascii or netcdf")

    def __len__(self):
        return len(self._array)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._array, attr)

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, item):
        if isinstance(key, slice):
            self._array[key] = item
        elif key in self.dtype.names:
            self._array[key] = item
        else:
            dtypes = self._array.dtype.descr
            dtypes.append((key, item.dtype.descr[0][1]))
            dtypes = [(str(d[0]), d[1]) for d in dtypes]
            newarr = np.zeros(self._array.shape, dtype=dtypes)
            for var in self.variables:
                newarr[var] = self._array[var]
            newarr[key] = item
            self._array = newarr

    def __repr__(self):
        try:
            string = " \
            {} trajectories with {} time steps. \n \
            Available fields: {}\n \
            total duration: {} minutes".format(
                self.ntra, self.ntime,
                "/".join(self.variables),
                self.duration
            )
        except AttributeError:
            # Assume it's an empty Tra()
            string = "\
            Empty trajectories container.\n\
            Hint: use load_ascii() or load_netcdf()\n\
            to load data"
        return string

    @property
    def ntra(self):
        """Return the number of trajectories"""
        if self.ndim < 2:
            warn("\nBe careful with the dimensions, "
                 "you may want to change the shape:\n"
                 "either shape + (1,) or (1,)+shape")
            return None
        return self.shape[0]

    @property
    def ntime(self):
        """Return the number of time steps"""
        if self.ndim < 2:
            warn("\nBe careful with the dimensions, "
                 "you may want to change the shape:\n"
                 "either shape + (1,) or (1,)+shape")
            return None
        return self.shape[1]

    @property
    def variables(self):
        """Return the names of the variables"""
        return list(self.dtype.names)

    @property
    def duration(self):
        """Time duration in minutes."""
        end = self['time'][0, -1]
        start = self['time'][0, 0]
        delta = end - start
        if isinstance(delta, np.timedelta64):
            return delta.astype(timedelta).total_seconds() / 60.
        return delta * 60.

    @property
    def initial(self):
        """Give the initial time of the trajectories."""
        starttime = self['time'][0, 0]
        return starttime.astype(datetime)

    @property
    def startdate(self):
        """Return the starting date of the trajectories"""
        if self._startdate is None:
            time0 = self['time'][0, 0]
            if isinstance(time0, np.datetime64):
                self._startdate = time0.astype(datetime)
            else:
                self._startdate = datetime(1900, 1, 1, 0)
        return self._startdate

    def set_array(self, array):
        """To change the trajectories array."""
        self._array = array

    def get_array(self):
        """Return the trajectories array as numpy object"""
        return self._array

    def concatenate(self, trajs, time=False, inplace=False):
        """To concatenate trajectories together.

        Concatenate trajectories together and return a new object.
        The trajectories should contain the same variables.
        if time=False, the number of timestep in each trajs should be the same
        if time=True, the number of trajectories in each Tra should be the same

        Parameters
        ----------

            trajs: Tra or list of Tra
                Trajectories to concatenate with the current one
            time: bool, default False
                if True concatenate along the time dimension
            inplace: bool, default False
                if True append the trajs to current Tra object and return None

        Returns
        -------
        Tra
            Return a new Tra (trajectories) object

        Examples
        --------

        Create a new Tra object which include trajs and all newtrajs

        >>> files = ['lsl_20001010_00.4', 'lsl_2001010_01.4']
        >>> filename = files[0]
        >>> trajs = Tra(filename)
        >>> newtrajs = [Tra(f) for f in files]
        >>> alltrajs = trajs.concatenate(newtrajs)

        Append newtrajs to trajs

        >>> trajs = Tra(filename)
        >>> newtrajs = [Tra(f) for f in files]
        >>> trajs.concatenate(newtrajs, inplace=True)

        """
        if not isinstance(trajs, (tuple, list)):
            trajs = (trajs,)
        if time:
            trajstuple = (self.T,)
            trajstuple += tuple(tra.T for tra in trajs)
            test = np.concatenate(trajstuple).T
        else:
            trajstuple = (self.get_array(),)
            trajstuple += tuple(tra.get_array() for tra in trajs)
            test = np.concatenate(trajstuple)

        if inplace:
            self._array = test
        else:
            newtrajs = Tra()
            newtrajs.set_array(test)
            return newtrajs

    def append(self, trajs):
        """append trajectories

        Parameters
        ---------
        trajs: single Tra or list of Tra
                Trajectories to concatenate with the current one

        Examples
        --------

        >>> files = ['lsl_20001010_00.4', 'lsl_2001010_01.4']
        >>> filename = files[0]
        >>> trajs = Tra(filename)
        >>> newtrajs = [Tra(f) for f in files]
        >>> trajs.append(newtrajs)
        """
        self.concatenate(trajs, inplace=True)

    def write(self, filename, fileformat='netcdf'):
        """Method to write the trajectories to a file"""
        globals()['_write_{}'.format(fileformat)](self, filename)

    def load_netcdf(self, filename, usedatetime=True, msv=-999, unit='hours',
                    **kwargs):
        """Method to load trajectories from a netcdf file"""
        self._array, self._startdate = from_netcdf(filename,
                                                   usedatetime=usedatetime,
                                                   msv=msv,
                                                   unit=unit,
                                                   **kwargs)
    load_netcdf.__doc__ = from_netcdf.__doc__

    def write_netcdf(self, filename, exclude=None, unit='hours'):
        """Write netcdf"""
        to_netcdf(self, filename, exclude=exclude, unit=unit)
    write_netcdf.__doc__ = to_netcdf.__doc__

    def write_ascii(self, filename, gz=False, digit=3, mode='w'):
        """Write ascii"""
        to_ascii(self, filename, gz=gz, digit=digit, mode=mode)
    write_ascii.__doc__ = to_ascii.__doc__

    def load_ascii(self, filename, usedatetime=True, msv=-999.999, gz=False):
        """Load ascii"""
        self._array, self._startdate = from_ascii(filename,
                                                  usedatetime=usedatetime,
                                                  msv=msv,
                                                  gz=gz)
    load_ascii.__doc__ = from_ascii.__doc__
