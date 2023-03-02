# Machine Learning Methods and Tools

Explain the method and why you think it's suitable for your use case.
Explain the choice of tools/packages/data and the reason for use.

## Machine Learning algorithm - DBSCAN

This project will use the Density-based spatial clustering of applications with
noise (DBSCAN) algorithm {cite}`SchubertDBSCANRevisitedRevisited2017`, which is
a clustering technique well-suited for the point cloud dataset we'll be working
with. DBSCAN is able to group together points that are densely clustered
without setting the expected number of clusters a priori (as in k-means
clustering). Specifically, we will be using
[cuML's implementation of DBSCAN](https://docs.rapids.ai/api/cuml/23.02/api.html#cuml.DBSCAN)
that is GPU-accelerated to find dense clusters across millions of points in
minutes.

![DBSCAN animation on Gaussian Mixtures](https://user-images.githubusercontent.com/23487320/162365311-545e7b53-12e3-4411-b923-206b53aa3666.gif)

Animation sourced from
https://dashee87.github.io/data%20science/general/Clustering-with-Scikit-with-GIFs.
See also https://www.naftaliharris.com/blog/visualizing-dbscan-clustering for a
nice interactive way of visualizing the DBSCAN algorithm and how the parameters
affect the clustering result.
