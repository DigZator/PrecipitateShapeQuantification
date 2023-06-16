from init import *
from reprod2D_Test import get_aspect_ratio
from time_dependance import *

# Make and return a new key for clusterAliases 
def createcluster(currvar):
    global clusterAliases
    currvar += 1
    clusterAliases[currvar] = 1
    return currvar

# Increase the size of the cluster and return the label to allot the current pixel
def addtocluster(label):
    clusterAliases[findoriginal(label)] += 1
    return label

# Find the primary cluster that is connect to this cluster
def findoriginal(label):
    while clusterAliases[label] < 0:
        label = -clusterAliases[label]
    return label

# Connect the clusters
def unifycluster(a, l):
    global clusterAliases
    # Cells of same cluster
    if a == l:
        return addtocluster(a)
    OA = findoriginal(a)

    # Cells of different but connected clusters
    if findoriginal(l) == OA:
        clusterAliases[OA] += 1
        return a
    
    # Unconnected clusters to be connected
    clusterAliases[OA] += clusterAliases[findoriginal(l)] + 1

    if clusterAliases.get(l, False):
        prev = clusterAliases[l]
        if prev < 0:
            clusterAliases[-prev] = -OA
    clusterAliases[l] = -OA
    return a

# HK algorithm core
def hkalg(img):
    global currval
    currvar = currval
    m, n = len(img), len(img[0])

    # Search pixel by pixel
    for i, j in it.product(range(m), range(n)):
        # Background Cell
        if img[i][j] == 0:
            continue
        
        # Check if the adjacent cells are part of a cluster (considering edge cases)
        U = False if i == 0 else (img[i-1][j] != 0)
        L = False if j == 0 else (img[i][j-1] != 0)

        # If both of the adjacent cells are unoccupied, create a new cluster
        if not (U or L):
            currvar = createcluster(currvar)
            img[i][j] = currvar
        
        # If only one of them is occupied, add this pixel to the cluster
        elif (U ^ L):
            img[i][j] = addtocluster(img[i-1][j] if U else img[i][j-1])
        
        # If both the cells are part of cluster then unify them if required
        elif (U and L):
            U = img[i-1][j]
            L = img[i][j-1]
            img[i][j] = unifycluster(U, L)

    return img
    
    # plt.show()

# To match the  label of each pixel with the label of the cluster
def renamecluster(mat):
    m, n = len(mat), len(mat[0])
    for i, j in it.product(range(m), range(n)):
        if mat[i][j] != 0:
            mat[i][j] = findoriginal(mat[i][j])

# To connect the precipitates that are on the edge of the image
def connect_across(mat):
    m, n = len(mat), len(mat[0])
    con_listx = []
    con_listy = []
    for i in range(m):
        a, b = mat[i][0], mat[i][-1]
        if (a != 0 and b != 0 and not ([a, b] in con_listx)):
            con_listx.append([a, b])
            # print(a, b)
    for j in range(n):
        a, b = mat[0][j], mat[-1][j]
        if (a != 0 and b != 0 and not ([a, b] in con_listy)):
            con_listy.append([a, b])
    # print(con_listx + con_listy)
    for i,j in it.product(range(m), range(n)):
        for con in (con_listx + con_listy):
            if mat[i][j] == con[1]:
                mat[i][j] = con[0]
    return mat, con_listx, con_listy

# To make clusters and identify the edge cases.
def mkcluster(img):
    global currval
    global clusterAliases

    mat = [[1 if a else 0 for a in line] for line in img]
    clusterAliases.clear()
    # currval = 2
    # print(mat)
    hkalg(mat)
    renamecluster(mat)
    mat, clx, cly = connect_across(mat)
    return (mat, clx, cly)

def extract_precipitates(img):
    # Making clusters, and identifying clusters at the edge
    clus, clx, cly = (mkcluster(img[:, :]/255))
    clus = np.array(clus)
    m, n = clus.shape

    # Dictionary that stores the co-ordinates of the Precipitates
    clusterdict = {}

    # Populating clusterdict
    for i, j in it.product(range(m), range(n)):
        if clus[i,j] != 0:
            if clus[i,j] not in clusterdict.keys():
                clusterdict[clus[i,j]] = [(i, j)]
            else:
                clusterdict[clus[i,j]].append((i, j))
    # print(clusterdict.keys())

    # Converting to numpy array
    for k in clusterdict.keys():
        clusterdict[k] = np.array(clusterdict[k])
    clx, cly = np.array(clx), np.array(cly)
    
    # Dealing with edge particles, by changing their coordinates. First dealing with the left/right precipitates then the up/down precipitates
    if len(clx):
        for cx in clx[:,0]:
            try:
                coords = clusterdict[cx]
                coords[:, 1] = (coords[:, 1] + n//2)%n
                clusterdict[cx] = coords
            except KeyError:
                # print("Check", cx)
                pass
    if len(cly):
        for cy in cly[:,0]:
            try:
                coords = clusterdict[cy]
                coords[:,0] = (coords[:,0] + m//2)%m
                clusterdict[cy] = coords
            except KeyError:
                # print("Check", cx)
                pass
    
    # To store all the precipitates individually
    preci = []

    # Translating the precipitates to origin
    for k in clusterdict.keys():
        coords = clusterdict[k]

        maxx = np.max(coords[:,1])
        maxy = np.max(coords[:,0])
        minx = np.min(coords[:,1])
        miny = np.min(coords[:,0])
        
        preci_mat = np.zeros((maxy - miny + 1, maxx - minx + 1))
        coords = coords - np.array([miny, minx])
        
        for a, b in coords:
            preci_mat[a,b] = 1
        
        # plt.imshow(preci_mat)
        # plt.show()
        
        preci.append(preci_mat)
    return preci, clus

def get_vals(preci):
    d = {}
    for k in preci.keys():
        # preci = preci1[k].astype(int)
        hold = preci[k]
        hold[1] = (hold[1]).astype(int)
        A, RM, RE = get_aspect_ratio(hold[1])
        # print(f"Label = {k}, A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(hold[1]):.2f}")
        d[k] = [A, RM, RE, np.sum(hold[1])]
    return d

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
    
    clusterAliases = {}
    currval = 2
    # plt.imshow(imgs[0])
    # plt.show()
    preci1, mat1 = extract_precipitates(imgs[0])
    # plt.imshow(mat1)
    # plt.show()

    lmat = mat1
    d = {0:get_vals(get_preci(mat1))}

    for i in range(1, len(imgs)):
    # temp = [lmat]
    # for i in range(1, 4):
        npreci, nmat = extract_precipitates(imgs[i])
        nmat = comp_mats(lmat, nmat)
        npreci = get_preci(nmat)
        d[i] = get_vals(npreci)
        
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
