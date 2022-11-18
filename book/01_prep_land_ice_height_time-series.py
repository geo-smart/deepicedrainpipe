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
import xarray as xr

# %% [markdown]
# Just to make sure we’re on the same page,
# let’s check that we’ve got compatible versions installed.

# %%
xr.show_versions()
