# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Accessing ICESat-2/ATL11 Land Ice Height time-series
#
# In this tutorial, we'll step through a data pipeline on turning point cloud
# time-series data from the ICESat-2 laser altimeter into an analysis ready
# format. By the end of this lesson, you should be able to:
#
# - Access ICESat-2 data in a Hierarchical Data Format (HDF5) from the cloud
# - Construct a data pipeline that combines multiple ICESat-2 tracks and laser
#   beams into a flat data structure
# - Store the pre-processed data in a cloud-optimized, analysis ready data
#   format
#
# References:
# - https://github.com/weiji14/deepicedrain/blob/v0.4.2/atl06_to_atl11.ipynb
# - https://github.com/weiji14/deepicedrain/blob/v0.4.2/atl11_play.ipynb

# %% [markdown]
# ## About ICESat-2
#
# The Ice, Cloud, and land Elevation Satellite-2 ([ICESat-2](https://www.nasa.gov/content/goddard/about-icesat-2)) was launched in 2018.
# The Advanced Topographic Laser Altimeter System, or ATLAS, is the only instrument on board.
# ATLAS has a single green laser that is split into six beams, arranged in three pairs.
# The 10,000 laser pulses emited each second reach the earth and reflect off the surface before returning to the satellite,
# where their travel time is recorded and ultimately used (in combination with information about the satellite's location)
# used to determine the height of the surface they reflected off of.
#
# ### Data Products
#
# The photon travel times collected by ATLAS are ultimately processed into a series of [ICESat-2 data products](https://nsidc.org/data/icesat-2/products).
# The data products are produced with multiple levels of processing, from geolocated photons (ATL03) to gridded time series (e.g. ATL11).
# For this analysis, we use one of the highest level (3B) products: ATL11 Slope-Corrected Land Ice Height Time Series product {cite:p}`ATL11.003`.
#
# ### Data Access
#
# ICESat-2 data access is available from NSIDC through several mechanisms, including for local download and in the cloud.
# A compilation of resources for accessing and working with ICESat-2 data is available in [this resource guide](https://icepyx.readthedocs.io/en/latest/community/resources.html)
# and through the [NSIDC website](https://nsidc.org/data/icesat-2/tools).
# Here we will access data in the cloud by getting the appropriate s3urls using [icepyx](https://icepyx.readthedocs.io/en/latest/), a Python software library and community of ICESat-2 data users, developers, and data managers.
# %% [markdown]
# ## Getting started
#
# These are the tools you’ll need.

# %%
import datatree
import icepyx
import s3fs
import xarray as xr

# %% [markdown]
# Just to make sure we’re on the same page,
# let’s check that we’ve got compatible versions installed.

# %%
xr.show_versions()


# %% [markdown]
# ## Cloud access to ICESat-2 ATL11 files
#
# For more details on accessing ICESat-2 data in the cloud, please check out the references below!
#
# References:
# - https://github.com/icesat2py/icepyx/blob/development/doc/source/example_notebooks/IS2_cloud_data_access.ipynb
# - https://nsidc.github.io/earthaccess/tutorials/demo/
# - https://nasa-openscapes.github.io/earthdata-cloud-cookbook/examples/NSIDC/ICESat2-CMR-AWS-S3.html#data-access-using-aws-s3
# - https://nsidc.org/data/user-resources/help-center/nasa-earthdata-cloud-data-access-guide
# - https://book.cryointhecloud.com/tutorials/IS2_ATL15_surface_height_anomalies/IS2_ATL15_surface_height_anomalies.html

# %% [markdown]
# ### Providing credentials
#
# Accessing NASA data requires you to have an Earthdata Login.
# You can sign up for one free at https://data.nsidc.earthdatacloud.nasa.gov/
# and learn more about NASA authentication and managing your credentials [via Earthaccess](https://nsidc.github.io/earthaccess/) and 
# [here](https://nasa-openscapes.github.io/2021-Cloud-Hackathon/tutorials/04_NASA_Earthdata_Authentication.html#authentication-for-nasa-earthdata).
#
# By obtaining your s3 urls via [icepyx](https://icepyx.readthedocs.io/en/latest/), you are also able to authenticate for cloud data access (note: Earthaccess is used under the hood to do this).
# %%
# First we must let icepyx know where (and when) we would like data from.

short_name = 'ATL11'  # The data product we would like to query
spatial_extent = [-85.0511287, -60.0, -180.0, 180.0] # bounding box for Antarctica
date_range = ['2018-09-15','2023-05-15'] # entire satellite record
# %%
# Setup the Query object
region = ipx.Query(short_name, spatial_extent, date_range)
# %%
# Get the granule IDs and cloud access urls (note that due to some missing ICESat-2 product metadata, icepyx is still working to provide s3 urls for some products)
gran_ids = region.avail_granules(ids=True, cloud=True)
print(gran_ids)

# %%
# Authenicate using your NASA Earth Data login credentials; enter your user id and password when prompted
region.earthdata_login(s3token=True)

# %%
# set up our s3 file system using our credentials
fs_s3 = earthaccess.get_s3fs_session(daac='NSIDC', provider=region._s3login_credentials)

# %% [markdown]
# ## Loading into xarray
#
# Let's read a single ICESat-2 ATL11 HDF5 file into an `xarray` data structure!
# 
# Let's first take a quick look at an example of an ATL11 HDF5 file.
# We'll read it using [`xarray.open_dataset`](https://docs.xarray.dev/en/v2022.11.0/generated/xarray.open_dataset.html).

# %%
s3_url = gran_ids[1][3]

with fs_s3.open(path=s3_url) as h5file:
    ds = xr.open_dataset(h5file, engine="h5netcdf")
ds

# %% [markdown]
# Hmm, so there are a bunch of attributes, but no data variables.
# This is because the ICESat-2 laser altimeter data is stored in 'groups' per laser.
#
# For ATL11, the 6 lasers have been combined into 3 pair tracks (pt1, pt2, pt3).
# To read the nested data structure, we can either loop over each of these groups,
# and/or use something like [`datatree.open_datatree`](https://xarray-datatree.readthedocs.io/en/latest/generated/datatree.open_datatree.html).
#
# References:
# - https://medium.com/pangeo/easy-ipcc-part-1-multi-model-datatree-469b87cf9114

# %%
with fs_s3.open(path=s3_url) as h5file:
    pair_track_dict = {}
    for pair_track in ["pt1", "pt2", "pt3"]:
        h5file.seek(0)  # https://github.com/pydata/xarray/pull/7304
        pair_track_dict[pair_track] = xr.open_dataset(
            filename_or_obj=h5file, engine="h5netcdf", group=pair_track
        )
    dt = datatree.DataTree.from_dict(d=pair_track_dict)
dt

# %%
