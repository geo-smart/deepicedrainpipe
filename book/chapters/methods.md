# Machine Learning Methods and Tools

Explain the method and why you think it's suitable for your use case.
Explain the choice of tools/packages/data and the reason for use.

## Machine Learning algorithm - DBSCAN

This project will use the Density-based spatial clustering of applications with
noise (DBSCAN) algorithm, which is clustering technique well-suited for the
point cloud dataset we'll be working with. DBSCAN is able to group together
points that are densely clustered without setting the expected number of
clusters a priori (as in k-means clustering). Specifically, we will be using
[cuML's implementation of DBSCAN](https://docs.rapids.ai/api/cuml/23.02/api.html#cuml.DBSCAN)
that is GPU-accelerated to find dense clusters across millions of points in
minutes.
