from init import *
from reprod2D_Test import get_aspect_ratio

# datContent = [i.strip().split() for i in open("./Comp1000.dat").readlines()]
datContent = [i.strip().split() for i in open("./Comp10000.dat").readlines()]

# print(datContent)

img = np.zeros((512,512))
img2 = np.zeros((512,512))

for line in datContent:
    if not line:
        datContent.pop(datContent.index(line))
    else:
        line[0] = int(line[0])
        line[1] = int(line[1])
        line[2] = float(line[2])
        img[line[0], line[1]] = line[2]
        img2[line[0], line[1]] = 1 - line[2]


# cv2.imshow("Image", img)
# cv2.waitKey(0)

print(np.max(img))
img = (img * 255).astype(np.uint8)

# cv2.imshow("Image", img)
# cv2.waitKey(0)

cimg = img.copy()
# cimg = (np.where(cimg >= 46, 255, 0)).astype(np.uint8)
thresh, bin_img = cv2.threshold(cimg, (np.max(img)/2), 255, type = cv2.THRESH_BINARY)
# invbin = ~bin_img

# cv2.imshow("Image", cimg)
# cv2.waitKey(0)

# cv2.imshow("Image", bin_img)
# cv2.waitKey(0)

plt.imshow(bin_img)
plt.show()

# print(bin_img)

####### Contours Methods #######

# contours, _ = cv2.findContours(bin_img,
#                                cv2. RETR_TREE,
#                                cv2.CHAIN_APPROX_SIMPLE)

# img_lis = []
# bbox_lis = []

# out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
# out2 = out.copy()

# out = cv2.drawContours(out, contours, -1, (0, 255, 0), 1)

# for c in contours:
#     x, y, w, h = cv2.boundingRect(c)
#     if (cv2.contourArea(c)) > 100:
#         img_lis.append(bin_img[y:(y+h), x:(x+w)])
#         bbox_lis.append([x,y,w,h])
#         cv2.rectangle(out2, (x,y), (x+w,y+h), (255,0,0), 1)

# cv2.imshow("Image", out)
# cv2.waitKey(0)

# takecon, takebbox, takeimg = [], [], []
# for i in range(len(img_lis)):
#     cv2.imshow("Precipitate", img_lis[i])
#     take = cv2.waitKey(0)
#     # take = int(input("Consider this precipitate"))
#     if take == ord('y') or take == ord('Y') or take == ord('1'):
#         # takecon.append(contours[i])
#         takebbox.append(bbox_lis[i])
#         takeimg.append(img_lis[i])
#     cv2.destroyAllWindows()
    
#     Alist, RMlist, RElist = [], [], []

# for preci in takeimg:
#     A, RM, RE = get_aspect_ratio(preci)
#     print(f"A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}")
#     Alist.append(A)
#     RMlist.append(RM)
#     RElist.append(RE)

####### End Method #######

####### HK Algorithm #######

#Dict to store sizes and connections
clusterAliases = {}

# Make and return a new key for clusterAliases 
def createcluster(currvar):
    global clusterAliases
    currvar += 1
    clusterAliases[currvar] = 1
    return currvar

def addtocluster(label):
    clusterAliases[findoriginal(label)] += 1
    return label

def findoriginal(label):
    while clusterAliases[label] < 0:
        label = -clusterAliases[label]
    return label

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

def hkalg(img):
    currvar = 2
    m, n = len(img), len(img[0])
    for i, j in it.product(range(m), range(n)):
        # Background Cell
        if img[i][j] == 0:
            continue
    
        U = False if i == 0 else (img[i-1][j] != 0)
        L = False if j == 0 else (img[i][j-1] != 0)

        if not (U or L):
            currvar = createcluster(currvar)
            img[i][j] = currvar
        elif (U ^ L):
            img[i][j] = addtocluster(img[i-1][j] if U else img[i][j-1])
        elif (U and L):
            U = img[i-1][j]
            L = img[i][j-1]
            img[i][j] = unifycluster(U, L)
    return img
    
    # plt.show()

def renamecluster(mat):
    m, n = len(mat), len(mat[0])
    for i, j in it.product(range(m), range(n)):
        if mat[i][j] != 0:
            mat[i][j] = findoriginal(mat[i][j])

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
    print(clusterdict.keys())

    # Converting to numpy array
    for k in clusterdict.keys():
        clusterdict[k] = np.array(clusterdict[k])
    clx, cly = np.array(clx), np.array(cly)
    
    # Dealing with edge particles, by changing their coordinates. First dealing with the left/right precipitates then the up/down precipitates
    for cx in clx[:,0]:
        coords = clusterdict[cx]
        coords[:, 1] = (coords[:, 1] + n//2)%n
        clusterdict[cx] = coords
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
    return preci

precipitates = extract_precipitates(bin_img)

for preci in precipitates:
    preci = preci.astype(int)
    A, RM, RE = get_aspect_ratio(preci)
    print(f"A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(preci):.2f}")