from init import *

clusterAliases = {}

def get_aspect_ratio(preci, flip = True):
  if flip:
    preci = np.where((preci==0)|(preci==1), preci^1, preci)
  shor = np.sum(preci, axis = 1)
  sver = np.sum(preci, axis = 0)
  verlen, horlen = len(shor), len(sver)
  # print(i, shor, sver)
  # print(preci.shape, len(shor), len(sver))
  barx = 0
  bary = 0
  sumx = 0
  sumy = 0
  for y in range(verlen):
    for x in range(horlen):
      barx += (x + 1) * preci[y,x]
      bary += (y + 1) * preci[y,x]
      sumx += preci[y,x]
  barx = barx/sumx
  bary = bary/sumx
#   print(bary, barx)
  µ020 = 0
  µ200 = 0
  µ110 = 0
  z = 1
  for y in range(verlen):
    for x in range(horlen):
      µ020 += ((x - barx + 1)**0) * ((y - bary + 1)**2) * (z**0) * preci[y,x]
      µ200 += ((x - barx + 1)**2) * ((y - bary + 1)**0) * (z**0) * preci[y,x] 
      µ110 += ((x - barx + 1)**1) * ((y - bary + 1)**1) * (z**0) * preci[y,x]
  inermat = np.array([[µ200, µ110],
                      [µ110, µ020]])
  w, v = np.linalg.eig(inermat)
  # print(w)
  w.sort()
  # print(w)
  A = np.sqrt(w[1]/w[0])
  RM = ((np.sum(sver)/np.pi)*A)**0.5
  RE = RM * (A**(-1/3))
  return A, RM, RE

####### Contours Methods #######

def CNT(img, bin_img):
    # Finding Contours of the precipitates
    contours, _ = cv2.findContours(bin_img,
                                cv2. RETR_TREE,
                                cv2.CHAIN_APPROX_SIMPLE)
    
    # To store the Slice of the precipitate and the coordinates of the bounding box
    img_lis = []
    bbox_lis = []

    # Converting the Grayscale image to BGR to making the bounding boxes
    out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    out2 = out.copy()

    # Drawing contours on the image
    out = cv2.drawContours(out, contours, -1, (0, 255, 0), 1)

    # Filtering out smaller contours
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (cv2.contourArea(c)) > 100:
            img_lis.append(bin_img[y:(y+h), x:(x+w)])
            bbox_lis.append([x,y,w,h])
            cv2.rectangle(out2, (x,y), (x+w,y+h), (255,0,0), 1)

    cv2.imshow("Image", out)
    cv2.waitKey(0)

    # Appending the precipitate slices
    takecon, takebbox, takeimg = [], [], []
    for i in range(len(img_lis)):
        cv2.imshow("Precipitate", img_lis[i])
        take = cv2.waitKey(0)
        # take = int(input("Consider this precipitate"))
        if take == ord('y') or take == ord('Y') or take == ord('1'):
            # takecon.append(contours[i])
            takebbox.append(bbox_lis[i])
            takeimg.append(img_lis[i]/255)
        cv2.destroyAllWindows()
    return takeimg

####### End Method #######

####### HK Algorithm #######

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
    try:
        clusterAliases.clear()
    except NameError:
        clusterAliases = {}
    currval = 2
    # print(mat)
    hkalg(mat)
    renamecluster(mat)
    mat, clx, cly = connect_across(mat)
    return (mat, clx, cly)

def extract_precipitates(img, off_set = 1, wkey = False):
    # Making clusters, and identifying clusters at the edge
    clus, clx, cly = (mkcluster(img[:, off_set:]/255))
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
                pass
    if len(cly):
        for cy in cly[:,0]:
            try:
                coords = clusterdict[cy]
                coords[:,0] = (coords[:,0] + m//2)%m
                clusterdict[cy] = coords
            except KeyError:
                pass
    
    # To store all the precipitates individually
    preci = []

    preci_wkey = {}

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
        preci_wkey[k] = preci_mat
    
    if wkey:
        return preci, clus, preci_wkey
    return preci, clus

if __name__ == "__main__":
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
    # method = "CNT"
    method = "HK"
    if method == "CNT":
        precipitates = CNT(img, bin_img)

    elif method == "HK":
        #Dict to store sizes and connections
        clusterAliases = {}
        precipitates, _ = extract_precipitates(bin_img, off_set = 1)

    for preci in precipitates:
        preci = preci.astype(int)
        A, RM, RE = get_aspect_ratio(preci)
        print(f"A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(preci):.2f}")