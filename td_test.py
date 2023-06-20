from init import *
from reprod2D import *
from time_dependance import *

if __name__ == "__main__":
    im_folder = "D:\Internship\PrecipitateShapeQuantification\ImageSorted"
    im_list = os.listdir(im_folder)
    im_list = sorted(im_list, key = lambda x: int(x[4:-4]))
    # print(im_list)
    imgs = []
    for iname in im_list:
        ipath = os.path.join(im_folder, iname)
        img = cv2.imread(ipath)
        img = img[74:466, 46:438]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.where(img < np.max(img) / 2, 0, 1)
        imgs.append(img)
    
    # print(imgs[0])
    # 73 466
    # 45 438

    # print(np.max(imgs[0]))
    
    # clusterAliases = {}
    currval = 2
    # plt.imshow(imgs[0])
    # plt.show()
    preci1, mat1 = extract_precipitates(imgs[0])
    # plt.imshow(mat1)
    # plt.show()

    lmat = mat1
    d = {0:get_vals(get_preci(mat1), flip = False)}

    for i in range(1, len(imgs)):
    # temp = [lmat]
    # for i in range(1, 4):
        npreci, nmat = extract_precipitates(imgs[i])
        nmat = comp_mats(lmat, nmat)
        npreci = get_preci(nmat)
        d[i] = get_vals(npreci, flip = False)
        
        # if i <= 4:
        #     fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        #     axes[0].imshow(lmat)
        #     axes[0].set_title('mat' + str(i-1))
        #     axes[1].imshow(nmat)
        #     axes[1].set_title('mat' + str(i))
        #     plt.tight_layout()
        #     plt.show()

        lmat = nmat.copy()
        # temp.append(nmat)
    
    uniqlab = set()
    for imno in d.keys():
        # print(imno, "\n", d[imno], "\n\n")
        for i in d[imno].keys():
            uniqlab.add(i)
    # uniqlab = set(key for dic in d for key in dic.keys())
    # print(uniqlab)

    uniqlab = sorted(uniqlab)
    areamat = np.zeros([len(d.keys()), len(uniqlab)])

    key = {k:i for i, k in enumerate(uniqlab)}
    invkey = {i:k for k, i in key.items()}

    for imno in d.keys():
        for k in d[imno].keys():
            areamat[imno, key[k]] = d[imno][k][3]
    
    key = (np.array(list(key.items())))
    
    areamat = areamat.T
    fig, ax = plt.subplots()
    im = ax.imshow(areamat)
    cbar = plt.colorbar(im)
    ax.set_ylabel("Precipitate Label")
    ax.set_xlabel("ImageNumber")
    ax.set_yticks(key[:,1], key[:,0])
    ax.set_xticks(range(0, 51, 5))
    cbar.set_label("Area of Precipitate (pixels)")
    plt.show()

    x = np.arange(areamat.shape[1])
    y = np.arange(areamat.shape[0])
    X, Y = np.meshgrid(x, y)
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111, projection = '3d')
    # ax3.plot_surface(X, Y, areamat)
    Z = areamat.flatten()
    ax3.bar3d(X.ravel(), Y.ravel(), np.zeros_like(Z), 1, 1, Z)
    ax3.set_ylabel("Precipitate Label")
    ax3.set_xlabel("ImageNumber")
    ax3.set_yticks(key[:,1], key[:,0])
    plt.show()
