from init import *
from reprod2D import *

datContent = [[float(a) for a in i.strip().split()] for i in open("./Comp1000.dat").readlines()]
koffset = 20


# print(datContent)

datContent = np.array([line for line in datContent if line])

datContent[:, 0:2] = datContent[:, 0:2].astype(np.int64)

m = np.max(datContent[:, 0]).astype(np.int64)
n = np.max(datContent[:, 1]).astype(np.int64)

# print(m, n)

img = np.zeros((m+1, n+1))

img[datContent[:, 0].astype(np.int64), datContent[:, 1].astype(np.int64)] = datContent[:, 2]

plt.imshow(img, cmap = 'gray')
plt.axis("off")
plt.savefig("Results\\Single Input\\Comp1000-A.png", bbox_inches = "tight")
plt.show()


max_val = np.max(img)

img[img < max_val/2] = 0
img[img != 0] = 1

plt.imshow(img, cmap = 'gray')
plt.axis("off")
plt.savefig("Results\\Single Input\\Threshold-A.png", bbox_inches = "tight")
plt.show()

clusterAliases = {}
precipitates, clusters, prewk = extract_precipitates(img, off_set = 0, wkey = True)

clusters[clusters != 0] += koffset
plt.imshow(clusters)
plt.axis("off")
plt.savefig("Results\\Single Input\\Clusters-A.png", bbox_inches = "tight")
plt.show()

op = [["Label", "Aspect Ratio", "Mean Radius", "Equivalent Radius", "Area"]]

for k in prewk.keys():
    preci = prewk[k].astype(int)
    A, RM, RE = get_aspect_ratio(preci, flip = False)
    print(f"Label - {k + koffset}, A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}, Area = {np.sum(preci):.2f}")
    if k in [3,97,202]:
        plt.imshow(1 - preci, cmap = "gray")
        plt.axis("off")
        plt.savefig(f"Results\\Single Input\\Precipitate-{k + koffset}.png", bbox_inches = "tight")
        plt.show()
    op.append([k + koffset, A, RM, RE, np.sum(preci)])

fname = "Results\\Single Input\\Output.csv"

with open(fname, "w", newline="") as f:
    wrt = csv.writer(f)
    wrt.writerows(op)