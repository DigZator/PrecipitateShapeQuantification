from init import *
from reprod2D_Test import get_aspect_ratio

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
    currvar = 2
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
    currval = 2
    # print(mat)
    hkalg(mat)
    renamecluster(mat)
    mat, clx, cly = connect_across(mat)
    return (mat, clx, cly)

def extract_precipitates(img):
    # Making clusters, and identifying clusters at the edge
    clus, clx, cly = (mkcluster(img[:, 1:]/255))
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
            coords = clusterdict[cx]
            coords[:, 1] = (coords[:, 1] + n//2)%n
            clusterdict[cx] = coords
    if len(cly):
        for cy in cly[:,0]:
            coords = clusterdict[cy]
            coords[:,0] = (coords[:,0] + m//2)%m
            clusterdict[cy] = coords
    
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

# def paintd(img, mat):
#     m, n = mat.shape
#     nmat = img.copy()
#     for y in range(m):
#         for x in range(n):
#             if img[m][n] and mat[m][n]:
#                 cv2.floodFill(nmat, (m,n), mat[m][n])
#     return nmat

def comp_mats(mat1, mat2):
    m, n = mat1.shape
    mat = mat2.copy()
    chglist = np.unique(mat1)
    for y in range(m):
        for x in range(n):
            if mat1[y,x] and mat[y,x] and (mat1[y,x] in chglist):
                rep = mat[y,x]
                mat[mat == rep] = mat1[y,x]
                chglist = np.setdiff1d(chglist, mat1[y,x])
    return mat

def get_preci(mat):
    m, n = mat.shape
    preci = {}
    for j, i in it.product(range(m), range(n)):
        if mat[j, i] != 0:
            if mat[j, i] not in preci.keys():
                preci[mat[j, i]] = [(j, i)]
            else:
                preci[mat[j, i]].append((j, i))
    
    for k in preci.keys():
        preci[k] = np.array(preci[k])
        if np.isin(preci[k][:, 1], [0, n-1]).all():
            coords = preci[k]
            coords[:, 1] = (coords[:, 1] + n//2)%n
            preci[k] = coords
        if np.isin(preci[k][:, 0], [0, m-1]).all():
            coords = preci[k]
            coords[:, 0] = (coords[:, 0] + m//2)%m
            preci[k] = coords
        coords = preci[k]
        maxx = np.max(coords[:,1])
        maxy = np.max(coords[:,0])
        minx = np.min(coords[:,1])
        miny = np.min(coords[:,0])

        preci_mat = np.zeros((maxy - miny + 1, maxx - minx + 1))
        coords = coords - np.array([miny, minx])
        
        for a, b in coords:
            preci_mat[a,b] = 1
        
        preci[k] = [preci[k], preci_mat]
    return preci

if __name__ == "__main__":
    # datContent1 = [i.strip().split() for i in open("./Comp1000.dat").readlines()]
    # datContent2 = [i.strip().split() for i in open("./Comp10000.dat").readlines()]

    # img = np.zeros((512,512))
    # img2 = np.zeros((512,512))
    # # print(datContent)
    # for line in datContent1:
    #     if not line:
    #         datContent1.pop(datContent1.index(line))
    #     else:
    #         line[0] = int(line[0])
    #         line[1] = int(line[1])
    #         line[2] = float(line[2])
    #         img[line[0], line[1]] = line[2]
    # for line in datContent2:
    #     if not line:
    #         datContent2.pop(datContent2.index(line))
    #     else:
    #         line[0] = int(line[0])
    #         line[1] = int(line[1])
    #         line[2] = float(line[2])
    #         img2[line[0], line[1]] = line[2]
    
    # cv2.imshow("Comp1000", img)
    # cv2.waitKey()
    # cv2.imshow("Comp10000", img2)
    # cv2.waitKey()

    img1 = cv2.cvtColor(cv2.imread("./T1.png"), cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(cv2.imread("./T2.png"), cv2.COLOR_BGR2GRAY)
    # img1 = (img1/255)
    # img2 = (img2/255)
    img1 = (img1/255).astype(np.uint8)
    img2 = (img2/255).astype(np.uint8)
    # cv2.imshow("Comp1000", img1)
    # cv2.waitKey()
    # cv2.imshow("Comp10000", img2)
    # cv2.waitKey()
    # print(img1.max())
    # plt.imshow(img1)
    # plt.show()
    # plt.imshow(img2)
    # plt.show()

    clusterAliases = {}
    preci1, mat1 = extract_precipitates(img1)
    # plt.imshow(mat1)
    # plt.show()
    preci2, mat2 = extract_precipitates(img2)
    # plt.imshow(mat2)
    # plt.show()
    nmat2 = comp_mats(mat1, mat2)
    # plt.imshow(nmat2)
    # plt.show()
    
    # Create a figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    # Plot each matrix in a separate subplot
    axes[0].imshow(mat1)
    axes[0].set_title('mat1')

    axes[1].imshow(mat2)
    axes[1].set_title('mat2')

    axes[2].imshow(nmat2)
    axes[2].set_title('nmat2')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Display the figure
    plt.show()

    preci1 = get_preci(mat1)
    preci2 = get_preci(nmat2)
    d1, d2 = {}, {}
    for k in preci1.keys():
        # preci = preci1[k].astype(int)
        hold = preci1[k]
        hold[1] = (hold[1]).astype(int)
        A, RM, RE = get_aspect_ratio(hold[1])
        print(f"Label = {k}, A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(hold[1]):.2f}")
        d1[k] = [A, RM, RE, np.sum(hold[1])]

    for k in preci2.keys():
        # preci = preci1[k].astype(int)
        hold = preci2[k]
        hold[1] = (hold[1]).astype(int)
        A, RM, RE = get_aspect_ratio(hold[1])
        print(f"Label = {k}, A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(hold[1]):.2f}")
        d2[k] = [A, RM, RE, np.sum(hold[1])]
    
    # print(d1)
    # print(type(d2)

    uniqlab = list(set(list(d1.keys()) + list(d2.keys())))
    print(uniqlab)

    o1, o2 = [], []
    for k in uniqlab:
        if k in d1.keys():
            o1.append(d1[k][3])
        else:
            o1.append(0)
        if k in d2.keys():
            o2.append(d2[k][3])
        else:
            o2.append(0)
    
    print(o1, o2)

    X_axis = np.arange(len(uniqlab))

    plt.bar(X_axis - 0.2, o1, 0.4, label = "1")
    plt.bar(X_axis + 0.2, o2, 0.4, label = "2")

    plt.xticks(X_axis, uniqlab)
    plt.legend()
    plt.show()