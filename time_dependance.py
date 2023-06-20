from init import *
from reprod2D import *

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
    mat1_max = np.max(mat1)
    mat[mat != 0] += mat1_max
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

def get_vals(preci, flip = True):
    d = {}
    for k in preci.keys():
        # preci = preci1[k].astype(int)
        hold = preci[k]
        hold[1] = (hold[1]).astype(int)
        A, RM, RE = get_aspect_ratio(hold[1], flip = flip)
        # print(f"Label = {k}, A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(hold[1]):.2f}")
        d[k] = [A, RM, RE, np.sum(hold[1])]
    return d

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