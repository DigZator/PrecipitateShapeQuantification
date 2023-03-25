import numpy as np
import os
import matplotlib.pyplot as plt
import vtkmodules.numpy_interface.dataset_adapter as dsa
from vtk import vtkXMLImageDataReader as XMLIDReader
import pandas as pd
from vtk.util.numpy_support import vtk_to_numpy

# dir_path = 'E:\\Seagate Drive\\OM\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\3D_5500px\\'
dir_path = 'D:\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\3D_5500px\\'

def get_data_size(fn):
    fn_data = sm.Fetch(fn)
    fn_data = dsa.WrapDataObject(fn_data)
    data = fn_data.PointData[0]
    return data.shape[0]

# print(get_data_size(samp))
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

iner_val = []

for filename in os.listdir(dir_path):
    reader = XMLIDReader()
    # samp = XMLIDReader(FileName=[dir_path + filename])
    # samp.PointArrayStatus = ['data']
    reader.SetFileName(dir_path + filename)
    reader.Update()
    imdat = reader.GetOutput()
    # print(type(imdat))
    # print(imdat.GetPointData().GetScalars())
    sc = imdat.GetPointData().GetScalars()
    a = vtk_to_numpy(sc)
    rows, cols, _ = imdat.GetDimensions()
    # print(a.reshape(rows, cols, -1))
    a = a.reshape(rows, cols, -1)
    # xapp, yapp, zapp = [], [], []
    # for x in range(rows):
    #     for y in range(cols):
    #         for z in range(cols):
    #             if a[x,y,z] == 1:
    #                 xapp.append(x)
    #                 yapp.append(y)
    #                 zapp.append(z)
    # ax.scatter(xapp, yapp, zapp, marker = 'o')
    # plt.show()
    # break
    µ100 = 0
    µ010 = 0
    µ001 = 0
    for x in range(rows):
        for y in range(cols):
            for z in range(cols):
                µ100 += x * a[x,y,z]
                µ010 += y * a[x,y,z]
                µ001 += z * a[x,y,z]
    
    tot = np.sum(a)
    x0, y0, z0 = [µ100/tot, µ010/tot, µ001/tot]
    µ002 = 0
    µ020 = 0
    µ200 = 0
    µ011 = 0 
    µ110 = 0
    µ101 = 0
    for x in range(rows):
        for y in range(cols):
            for z in range(cols):
                µ002 += ((x - x0)**0) * ((y - y0)**0) * ((z - z0)**2) * a[x,y,z]
                µ020 += ((x - x0)**0) * ((y - y0)**2) * ((z - z0)**0) * a[x,y,z]
                µ200 += ((x - x0)**2) * ((y - y0)**0) * ((z - z0)**0) * a[x,y,z]
                µ011 += ((x - x0)**0) * ((y - y0)**1) * ((z - z0)**1) * a[x,y,z]
                µ101 += ((x - x0)**1) * ((y - y0)**0) * ((z - z0)**1) * a[x,y,z]
                µ110 += ((x - x0)**1) * ((y - y0)**1) * ((z - z0)**0) * a[x,y,z]
    iner_val.append([µ002,
                    µ020,
                    µ200,
                    µ011,
                    µ101,
                    µ110])
    inermat = np.array([[µ020 + µ002, -µ110, -µ101],
                        [-µ110, µ200 + µ002, -µ001],
                        [-µ101, -µ001, µ200 + µ020]])
    w, v = np.linalg.eig(inermat)
    w.sort()
    A = np.sqrt((w[1] + w[2] - w[0])/(w[0] + w[1] - w[2]))
    B = np.sqrt((w[1] + w[2] - w[0])/(w[0] + w[2] - w[1]))
    Ap = np.sqrt(A**2/B)
    print(filename)
    print(A, B, Ap)
    print(x0, y0, z0)
print(iner_val)
