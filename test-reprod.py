from init import *
from reprod2D import *
from reprod3D import *

curr = (os.getcwd())
bm_folders = (os.listdir("benchmark_shapes"))

koffset = 20

for bmf in bm_folders:
    fpath = curr + "\\benchmark_shapes\\" + bmf
    imlist = (os.listdir(fpath))
    
    if bmf[0] == "2a":
        imgs = []
        expectedA = []
        calculatedA = []
        ang = []

        for im in imlist:
            img = plt.imread(fpath + "\\" + im)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = 1 - img
            precipitates, _ = extract_precipitates(img, off_set = 0, wkey = False)
            preci = (precipitates[0]).astype(np.int64)  #As all the image contain only a single precipitate
            
            A, RM, RE = get_aspect_ratio(preci, flip = False)
            area = np.sum(preci)
            # print(im)
            # print(A)
            # print(preci.shape)
            # print()
            m, n = preci.shape
            if bmf == "2D_370px_rotated":
                if im[5:7] == "00": #-5
                    ImpA = (n/m)
                expectedA.append(ImpA)
                ang.append(int(im[5:7]))
            else:
                expectedA.append(n/m)
            calculatedA.append(A)
        # print(expectedA)
        # print(calculatedA)
        if bmf == "2D_370px_rotated":
            data = {}
            for exp, calc, a in zip(expectedA, calculatedA, ang):
                if exp not in data:
                    data[exp] = {'a': [a], 'calc': [calc]}
                else:
                    data[exp]['a'].append(a)
                    data[exp]['calc'].append(calc)
            plt.figure(figsize=(8,6))
            for exp, val in data.items():
                plt.plot(val['a'], val['calc'], label = f"Expected {exp}")
            plt.ylabel('Calculated')
            plt.xlabel("Angle")
            for exp in set(expectedA):
                plt.hlines(y = data[exp]['calc'][0], xmin = min(ang), xmax = max(ang), color = "lightgray", linestyles = '--')
            plt.legend()
            plt.ylim(top = 8)
            plt.show()
        else:
            plt.scatter(expectedA, calculatedA)
            plt.xlabel("Expected")
            plt.ylabel("Calculated")
            plt.title(bmf)
            x = np.linspace(min(expectedA + calculatedA), max(expectedA + calculatedA), 100)
            plt.plot(x, x, color='red', label='x = y') 
            plt.grid(True)
            plt.show()
    elif bmf[0] == "3":
        loc = curr + "\\benchmark_shapes\\" + bmf
        dat_str = np.empty((0,4))
        for fname in os.listdir(loc):
            reader = XMLIDReader()
            reader.SetFileName(loc+ "\\" + fname)
            reader.Update()
            imdat = reader.GetOutput()

            sc = imdat.GetPointData().GetScalars()
            a = vtk_to_numpy(sc)
            r, c, d = imdat.GetDimensions()
            a = a.reshape(r, c, d)
            A, B, Ap, RM, RE, An, Bn = get_aspect_ratio3D(a)
            # print(fname)
            # print(A, B, Ap, RM, RE, An, Bn)
            dat_str = np.vstack((dat_str, np.array([A, B, An, Bn])))
        plt.scatter(dat_str[:,2],dat_str[:,0])
        x = np.linspace(np.min(dat_str[:,[0,2]]), np.min(dat_str[:,[0,2]]), 100)
        plt.plot(x, x, color = 'lightgray')
        plt.grid(True)
        plt.show()

