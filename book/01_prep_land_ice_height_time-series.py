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
# # Pre-processing ICESat-2/ATL11 Land Ice Height time-series
#
# In this tutorial, we'll step through a data pipeline on turning point cloud
# time-series data from the ICESat-2 laser alimeter into an analysis ready
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
# ## Getting started
#
# These are the tools you’ll need.

# %%
import datatree
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
# Let's read a single ICESat-2 ATL11 HDF5 file into an `xarray` data structure!
#
# References:
# - https://nasa-openscapes.github.io/earthdata-cloud-cookbook/how-tos/access/Earthdata_Cloud__Single_File__Direct_S3_Access_NetCDF4_Example.html
# - https://nasa-openscapes.github.io/earthdata-cloud-cookbook/examples/NSIDC/ICESat2-CMR-AWS-S3.html#data-access-using-aws-s3
# - https://nsidc.org/data/user-resources/help-center/nasa-earthdata-cloud-data-access-guide

# %% [markdown]
# ### Providing token credentials
#
# Accessing the cloud data requires you to set some authentication tokens.
# Get it from from https://data.nsidc.earthdatacloud.nasa.gov/s3credentials.
# There should be three keys:
#
# - accessKeyId (20 characters)
# - secretAccessKey (40 characters)
# - sessionToken (408 characters)
#
# Note that an Earthdata login will be required.
# See https://nasa-openscapes.github.io/2021-Cloud-Hackathon/tutorials/04_NASA_Earthdata_Authentication.html#authentication-for-nasa-earthdata

# %%
fs_s3 = s3fs.S3FileSystem(
    anon=False,
    key="ABCDEFGHIJKLMNOPQRST",
    secret="MnOpQrStUvWxYz1a2B3c4D5e6f7G8h9IjKlMnOpQ",
    token="jflpqw0eTngyEVuUL1ExugH4jxibaWJlYYdXvAHKpwKaEMsHmIj2bLScunmonY0R3QpU5DiEy2ScHNBCPmYZExM8sP2CknZa2BKtwpYMhycVRMGFlxCbkmUblvxluQZwKtvwyVNlA9jeqsAp2vEbdKZAZtU9HZwgf8JyjVNaVc4KPsi8L15yDqEj6TYRJ3dfKQwCPsNDyw2uCutMD1H0Rg4BkTOFX0lC7U2QrzRx4gZoPtyL2eVqlN2fWfiqzG09oMOaQGYSY2LUe4LUNMkboWz47oMRqHAHyFj84fvH0xw2GLZImVcWpSYyWRSbZPTNDpHkPrzrKNLAxKqR2gstVEgBACMbACIzhRVQUPrQLFlrjEyDQZioserdF3shlS30j3rQfGmu2ed4ZWQO7W7Qe5Fw",
)

# %% [markdown]
# ## Loading into xarray
#
# Let's first take a quick look at an example of an ATL11 HDF5 file.
# We'll read it using [`xarray.open_dataset`](https://docs.xarray.dev/en/v2022.11.0/generated/xarray.open_dataset.html).

# %%
with fs_s3.open(
    path="s3://nsidc-cumulus-prod-protected/ATLAS/ATL11/005/2019/09/30/ATL11_005411_0315_005_03.h5"
) as h5file:
    ds = xr.open_dataset(h5file, engine="h5netcdf")
ds

# %% [markdown]
# Hmm, so there are a bunch of attributes, but no data variables.
# This is because the ICESat-2 laser altimeter data is stored in 'groups' per laser.
#
# For ATL11, the 6 lasers have been combined into 3 pair tracks (pt1, pt2, pt3).
# To read the nested data structure, we can either loop over each of these groups,
# or use something like [`datatree.open_datatree`](https://xarray-datatree.readthedocs.io/en/latest/generated/datatree.open_datatree.html).

# %%
# TODO, fix the ValueError: malformed variable poly_coeffs has mixing of labeled and unlabeled dimensions.
with fs_s3.open(
    path="s3://nsidc-cumulus-prod-protected/ATLAS/ATL11/005/2019/09/30/ATL11_005411_0315_005_03.h5"
) as h5file:
    is2dt = datatree.open_datatree(h5file, engine="h5netcdf", phony_dims="access")
is2dt

# %%
