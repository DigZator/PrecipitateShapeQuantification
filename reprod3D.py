import numpy as np
import os
import matplotlib.pyplot as plt
from paraview import servermanager as sm
import vtk.numpy_interface.dataset_adapter as dsa
import pandas as pd

dir_path = 'E:\\Seagate Drive\\OM\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\3D_5500px\\'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

def get_data_size(fn):
    fn_data = sm.Fetch(fn)
    fn_data = dsa.WrapDataObject(fn_data)
    data = fn_data.PointData[0]
    return data.shape[0]

print(get_data_size(samp))

for filename in os.listdir(dir_path):
    samp = XMLImageDataReader(registrationName=filename, FileName=[dir_path + filename])
    samp.PointArrayStatus = ['data']
    samp_data = sm.Fetch(samp)
    samp_data = dsa.WrapDataObject(samp_data)
    data = samp_data.PointData[0]
    # e = int(np.cbrt(data.shape[0]))
    e = 103
    print(e)
    data = data.reshape(e,e,-1)
    print(data)
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(data)

    break

print()