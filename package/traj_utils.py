#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:28:58 2022

@author: dboateng
"""

# coding: utf8
import gzip
from datetime import datetime, timedelta
from functools import partial

import netCDF4
import numpy as np

def from_netcdf(filename, usedatetime=True, msv=-999, unit='hours',
                exclude=None, date=None, indices=None):
    """ Load trajectories from a netcdf


        Parameters
        ----------

        filename : string,
            path to a netcdf file containing trajectories
        usedatetime : bool, default True
                If True then return time as datetime object
        msv : float, default -999
                Define the missing value
        unit : string, default hours
                Define the units of the times (hours, seconds or hhmm)
        exclude: list of string, default empty
                Define a list of variables to exclude from reading
        date: datetime or list
                Can be used to select particular dates, for example
                to read in a single timestep
        indices: list or tuple
                Can be used to select particular trajectories
    """
    if exclude is None:
        exclude = []
    exclude.append('BASEDATE')
    try:
        with netCDF4.Dataset(filename) as ncfile:

            variables = [var for var in ncfile.variables if var not in exclude]

            formats = [ncfile.variables[var].dtype for var in variables]

            if usedatetime:
                formats[variables.index('time')] = 'datetime64[s]'

            ntra, ntime = _get_netcdf_traj_dim(ncfile)

            dates = _netcdf_time(ncfile, usedatetime=usedatetime, unit=unit)

            dates, index = _return_subset_netcdf(dates, date=date, indices=indices)

            ntime = ntime if date is None else len(dates)
            ntra = ntra if indices is None else len(index[1])

            array = np.zeros((ntra, ntime), dtype={'names': variables,
                                                   'formats': formats})

            array['time'] = repeat_time(dates, ntra)

            for var in variables:
                if var == 'time':
                    continue
                vardata = ncfile.variables[var][index].T
                vardata[vardata <= msv] = np.nan

                # Check need for netcdf trajectories produced by LAGRANTO
                # which make use of a old fortran library to write netcdf.
                # This library add two dummies dimensions.
                if vardata.ndim > 2:
                    array[var] = vardata.squeeze()
                else:
                    array[var] = vardata

            if 'latitude' in variables:
                variables[variables.index('latitude')] = u'lat'
                variables[variables.index('longitude')] = u'lon'
                try:
                    array.dtype.names = variables
                except ValueError:
                    array.dtype.names = [v.encode('utf8') for v in variables]

            starttime = get_netcdf_startdate(ncfile)
            time_zero = ncfile.variables['time'][0]
            if time_zero != 0:
                starttime += timedelta(**{unit: int(time_zero)})
    except RuntimeError as err:
        err.args += (str(filename), )
        raise
    return array, starttime


def get_netcdf_startdate(ncfile):
    """return the startdate of trajectories"""
    try:
        # if netcdf produced by lagranto
        date = [int(i) for i in ncfile.variables['BASEDATE'][0, 0, 0, :]]
        starttime = datetime(date[0], date[1], date[2], date[3], date[4])
    except KeyError:
        # if netcdf produced by the online trajectory module from COSMO
        starttime = datetime(ncfile.ref_year, ncfile.ref_month,
                             ncfile.ref_day, ncfile.ref_hour,
                             ncfile.ref_min)
    return starttime


def _netcdf_time(ncfile, usedatetime=True, unit='hours'):
    """ return netcdf times

        Paramters
        --------
        ncfile : netCDF4.Dataset instance
        usedatetime: bool, default True
            Read dates as datetime
        unit : string, default hours
            unit of times hours or seconds
    """
    if usedatetime:
        otimes = ncfile.variables['time'][:]
        starttime = get_netcdf_startdate(ncfile)

        if unit == 'hhmm':
            # lagranto writes the times as hh.mm instead as fractional times
            times = hhmm2frac(otimes)
            unit = 'hours'
        else:
            times = otimes

        units = '{} since {:%Y-%m-%d %H:%M:%S}'.format(unit, starttime)

        dates = netCDF4.num2date(times, units=units)
        return dates

    return ncfile['time'][:]


def _return_subset_netcdf(dates, date=None, indices=None):
    """

    Parameters
    ----------
    dates: list of dates
        trajectories times
    date: single date or list of dates
        Allow to select timestep of the trajectories
    indices: single index or list of indices
        Allow to select subset of trajectories

    Returns
    -------
    dates: list of dates
        Filtered using `date`
    indices: list of slices
        if no selection is done index is [slice(None), slice(None)]
    """
    index = [slice(None), slice(None)]
    if date is not None:
        if not isinstance(date, (list, tuple)):
            date = [date]
        d_index = np.hstack([np.where(dates == d)[0] for d in date])
        if d_index.size == 0:
            sdate = [str(d) for d in date]
            msg = '{} not found in time'.format(','.join(sdate))
            raise RuntimeError(msg)
        index = [np.sort(d_index), slice(None)]
        dates = dates[d_index]

    if indices is not None:
        if not isinstance(indices, (list, tuple)):
            raise ValueError('indices must be of type list or tuple')
        index[1] = indices
    return dates, index


def repeat_time(dates, ntra):
    """Copy the dates for all ntra"""
    dates.shape = (1, ) + dates.shape
    return dates.repeat(ntra, axis=0)


def _get_netcdf_traj_dim(ncfile):
    """ return nbre of trajectories (ntra) and nbre of timestep (ntime)"""

    dim_set = {'dimx_lon', 'id', 'ntra'}
    dim_nc = set(ncfile.dimensions.keys())

    try:
        ntra_dim = dim_set.intersection(dim_nc).pop()
        ntra = len(ncfile.dimensions[ntra_dim])
    except KeyError:
        raise Exception('Cannot read the number of trajectories, ' +
                        'not one of (' + ' '.join(dim_set) + ')')

    try:
        ntime = len(ncfile.dimensions['time'])
    except KeyError:
        ntime = len(ncfile.dimensions['ntim'])

    return ntra, ntime


def datetime_to_hours_since_start(date, start, units='hhmm'):
    """return date -start in hours"""
    hours = (date - start).total_seconds()/3600
    if units == 'hhmm':
        hours = int(hours) + 0.6 * (hours - int(hours))
    return hours


def vectorized_datetime_to_hours(*args, **kwargs):
    """Return a vectorized version of datetime_to_hours_since_start"""
    vectorized = np.vectorize(datetime_to_hours_since_start)
    return vectorized(*args, **kwargs)


def hhmm_to_hours(time):
    """Change from hh.mm to fractional hour"""
    if isinstance(time, bytes):
        hhmm = [float(t) for t in time.decode().split('.')]
        time = np.copysign(1, hhmm[0]) * (abs(hhmm[0]) + hhmm[1] / 60)
    else:
        hours = int(time)
        minutes = round(100 * (time - hours)) / 60
        time = hours + minutes
    return time


def hhmm2frac(*args, **kwargs):
    """Return a vectorized version of hhmm_to_hours"""
    vectorized = np.vectorize(hhmm_to_hours)
    return vectorized(*args, **kwargs)


def time_since_start_to_datetime(start, time, unit='hhmm'):
    """return start + time as datetime"""
    units = 'hours'
    if unit == 'hhmm':
        time = hhmm_to_hours(time)
    else:
        units = unit
    return start + timedelta(**{units: float(time)})


def add_times_to_netcdf(ncfile, times, startdate, unit='hours'):
    """Write times information on a netcdf file"""
    shift = startdate.second
    startdate -= timedelta(seconds=shift)
    ncfile.ref_year, ncfile.ref_month, ncfile.ref_day, ncfile.ref_hour,\
        ncfile.ref_min = startdate.timetuple()[0:5]
    ntimes = ncfile.createVariable('time', 'f4', ('ntim', ))
    units = ''
    if unit == 'seconds':
        units = 'seconds since {:%Y-%m-%d %H:%M:%S}'.format(startdate)
    elif unit == 'hours':
        units = 'hours since {:%Y-%m-%d %H:%M:%S}'.format(startdate)
    elif unit == 'hhmm':
        hhmms = vectorized_datetime_to_hours(times.astype(datetime), startdate)
        ntimes[:] = hhmms[0, :]
        return

    if isinstance(times[0, 0], np.datetime64):
        ntimes[:] = netCDF4.date2num(times[0, :].astype(datetime), units)
    else:
        ntimes[:] = times[0, :] + shift / 3600


def to_netcdf(trajs, filename, exclude=None, unit='hours'):
    """
    Write the trajectories in a netCDF file

    Parameters
    ----------
    trajs : Tra
        A Tra instance
    filename : string
        The name of the output file
    exclude : list, optional
        A list of variables to exclude
    unit : string, optional
        The unit of the dates, can be hours, seconds or hhmm
    """
    if exclude is None:
        exclude = []
    with netCDF4.Dataset(filename, 'w', format='NETCDF3_CLASSIC') as ncfile:
        ncfile.createDimension('ntra', trajs.ntra)
        ncfile.createDimension('ntim', trajs.ntime)
        ncfile.duration = int(trajs.duration)
        ncfile.pollon = 0.
        ncfile.pollat = 90.
        add_times_to_netcdf(ncfile, trajs['time'], trajs.startdate, unit=unit)
        exclude.append('time')
        for var in trajs.variables:
            if var in exclude:
                continue
            try:
                vararray = ncfile.createVariable(var, trajs[var].dtype,
                                                 ('ntim', 'ntra'))
            except RuntimeError as err:
                err.args += (var, trajs[var].dtype)
                raise
            vararray[:] = trajs[var].T


def to_ascii(trajs, filename, mode='w', gz=False, digit=3):
    """ Write the trajectories in an ASCII format

        Parameters:

        filename : string
            filename where the trajectories are written
        mode : string, default w
            define the mode for opening the file.
            By default in write mode ('w'),
            append (a) is another option

    Parameters
    ----------
    filename: string
        filename where the trajectories are written
    mode: string, default w
        define the mode for opening the file.
        By default in write mode ('w'),
        append ('a') is another option.
    gz: boolean, default False
        If true write the file as a gzip file
    digit: int, default 3
        Number of digit after the comma to use for lon, lat;
        Only 3 or 2 digits allowed

    """
    if trajs['time'].dtype != np.float:
        trajs['timeh'] = vectorized_datetime_to_hours(
            trajs['time'].astype(datetime), trajs.initial)

    for var in trajs.variables[1:]:
        trajs[var][np.isnan(trajs[var])] = -1000

    # skip 'time' and move 'timeh' to front
    if trajs['time'].dtype != np.float:
        variables = ['timeh']+trajs.variables[1:-1]
    else:
        variables = trajs.variables

    ntraj = trajs.shape[0]
    ntim = trajs.shape[1]
    nvar = len(variables)

    trajs_resh = np.reshape(np.array([np.reshape(trajs[var], ntraj*ntim)
                                      for var in variables]).T,
                            ntraj*ntim*nvar)
    # String template for header, variables header and variables
    header = 'Reference date {:%Y%m%d_%H%M} / Time range{:>8.0f} min\n \n'
    varheader = '{:>7}{:>10}{:>9}{:>6}'

    if digit == 2:
        fixvar = '{:>7.2f}{:>9.2f}{:>8.2f}{:>6.0f}'
        lineheader = '{:->7}{:->10}{:->9}{:->6}'
    elif digit == 3:
        fixvar = '{:>7.2f}{:>10.3f}{:>9.3f}{:>6.0f}'
        lineheader = '{:->7}{:->10}{:->9}{:->6}'
    else:
        raise ValueError('digit must be either 2 or 3')
    row_format = (' \n' + ((fixvar + '{:>10.3f}' * (nvar - 4)+'\n') * ntim))
    row_format *= ntraj

    if gz:
        with gzip.open(filename, mode + 't') as fname:
            # write the header
            fname.write(header.format(trajs.startdate, trajs.duration))

            # write the variables header
            if trajs['time'].dtype != np.float:
                fname.write((varheader + '{:>10}' * (nvar - 4)
                            ).format(*trajs.variables[:-1]) + '\n')
            else:
                fname.write((varheader + '{:>10}' * (nvar - 4)
                            ).format(*trajs.variables) + '\n')

            # write the line
            fname.write(
                (lineheader + '{:->10}' * (nvar - 4)
                ).format(*[''] * nvar) + '\n')

            # write the variables values
            fname.write(row_format.format(*trajs_resh))
    else:
        with open(filename, mode) as fname:
            # write the header
            fname.write(header.format(trajs.startdate, trajs.duration))

            # write the variables header
            if trajs['time'].dtype != np.float:
                fname.write((varheader + '{:>10}' * (nvar - 4)
                            ).format(*trajs.variables[:-1]) + '\n')
            else:
                fname.write((varheader + '{:>10}' * (nvar - 4)
                            ).format(*trajs.variables) + '\n')

            # write the line
            fname.write(
                (lineheader + '{:->10}' * (nvar - 4)
                ).format(*[''] * nvar) + '\n')

            # write the variables values
            fname.write(row_format.format(*trajs_resh))

    # remove the artificial timeh
    if trajs['time'].dtype != np.float:
        trajs.set_array(trajs[[name for name in trajs.variables[:-1]]])


def header_to_date(header):
    """ return the initial date based on the header of an ascii file"""
    try:
        starttime = datetime.strptime(header[2], '%Y%m%d_%H%M')
    except ValueError:
        try:
            starttime = datetime.strptime(
                header[2] + '_' + header[3], '%Y%m%d_%H'
            )
        except ValueError:
            print("Warning: could not retrieve starttime from header,\
                  setting to default value ")
            starttime = datetime(1970, 1, 1)

    return starttime


def get_ascii_timestep_period(times, usedatetime=True):
    """return the timestep and the period for an ascii """
    if usedatetime:
        timestep = times[1] - times[0]
        period = times[-1] - times[0]
    else:
        timestep = hhmm_to_hours(times[1]) - hhmm_to_hours(times[0])
        period = hhmm_to_hours(times[-1]) - hhmm_to_hours(times[0])
    return timestep, period


def get_ascii_header_variables(filename, gz=False):
    """return the header and variables of an ascii file"""
    if gz:
        with gzip.open(filename, 'rt') as fname:
            header = fname.readline().split()
            fname.readline()
            variables = fname.readline().split()
    else:
        with open(filename) as fname:
            header = fname.readline().split()
            fname.readline()
            variables = fname.readline().split()
    return header, variables


def from_ascii(filename, usedatetime=True, msv=-999.999, gz=False):
    """ Load trajectories from an ascii file

        Parameters:

        usedatetime: bool, default True
               If true return the dates as datetime object
        msv: float, default -999.999
               Change <msv> value into np.nan
        gzip: bool, default False
              If true read from gzip file
    """
    header, variables = get_ascii_header_variables(filename, gz=gz)

    startdate = header_to_date(header)

    dtypes = ['f8']*(len(variables))
    converters = None
    if usedatetime:
        dtypes[variables.index('time')] = 'datetime64[s]'
        t_to_d = partial(time_since_start_to_datetime, startdate)
        converters = {0: t_to_d}

    array = np.genfromtxt(filename, skip_header=5, names=variables,
                          missing_values=msv, dtype=dtypes,
                          converters=converters, usemask=True)
    for var in variables:
        if (var == 'time') and usedatetime:
            continue
        array[var] = array[var].filled(fill_value=np.nan)
    timestep, period = get_ascii_timestep_period(array['time'], usedatetime)

    # period/timestep gives strange offset (related to precision??)
    # so use scipy.around
    ntime = int(1 + np.around(period / timestep))
    ntra = int(array.size / ntime)

    array = array.reshape((ntra, ntime))
    return array, startdate

