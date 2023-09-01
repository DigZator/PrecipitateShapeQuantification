from init import *
from reprod2D import *
from time_dependance import *


# Selecting the Input folder and sorting according to filename
im_folder = "D:\Internship\PrecipitateShapeQuantification\ImageSorted"
im_list = os.listdir(im_folder)
im_list = sorted(im_list, key = lambda x: int(x[4:-4]))

# Accepting images
imgs = []
for iname in im_list:
    ipath = os.path.join(im_folder, iname)
    img = cv2.imread(ipath)

    # Crop required for the given dataset
    img = img[74:466, 46:438]
    # Convert to RGB image to Grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying threshold on the image
    img = np.where(img < np.max(img) / 2, 0, 1)

    imgs.append(img)

plt.imshow(imgs[0])
plt.axis('off')
plt.savefig(f"Results\\Multi Input\\InputImage-{0}.png", bbox_inches = "tight")
plt.show()

plt.imshow(imgs[1])
plt.axis('off')
plt.savefig(f"Results\\Multi Input\\InputImage-{1}.png", bbox_inches = "tight")
plt.show()

# Finding precipitates for the first input image
lpreci, lmat = extract_precipitates(imgs[0])

koffset = 20
lmat[lmat != 0] += koffset

plt.imshow(lmat)
plt.axis('off')
plt.savefig(f"Results\\Multi Input\\InitialLabels.png", bbox_inches = "tight")
plt.show()

d = {0:get_vals(get_preci(lmat), flip = False)}

for i in range(1, len(imgs)):
    npreci, nmat = extract_precipitates(imgs[i])
    nmat = comp_mats(lmat, nmat)
    npreci = get_preci(nmat)
    d[i] = get_vals(npreci, flip = False)
    
    # if i == 1:
    #     fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    #     axes[0].imshow(lmat)
    #     # axes[0].set_title('mat' + str(i-1))
    #     axes[0].axis('off')
    #     axes[1].imshow(nmat)
    #     # axes[1].set_title('mat' + str(i))
    #     axes[1].axis('off')
    #     plt.tight_layout()
    #     # plt.savefig("Results\\Multi Input\\ConsecutiveMat.png", bbox_inches = "tight")
    #     plt.show()

    lmat = nmat.copy()

uniqlab = set()
for imno in d.keys():
    for i in d[imno].keys():
        uniqlab.add(i)

uniqlab = sorted(uniqlab)
areamat = np.zeros([len(d.keys()), len(uniqlab)])

key = {k:i for i, k in enumerate(uniqlab)}
invkey = {i:k for k, i in key.items()}

for imno in d.keys():
    for k in d[imno].keys():
        areamat[imno, key[k]] = d[imno][k][3]

key = (np.array(list(key.items())))

areamat = areamat.T
fig, ax = plt.subplots(figsize=(10,6))
im = ax.imshow(areamat)
cbar = plt.colorbar(im)
ax.set_ylabel("Precipitate Label")
ax.set_xlabel("Image Number (Time)")
ax.set_yticks(key[:,1], key[:,0])
ax.set_xticks(range(0, 51, 5))
cbar.set_label("Area of Precipitate (pixels)")
plt.savefig(f"Results\\Multi Input\\AreaMatrixPlot.png", bbox_inches = "tight")
plt.show()

# x = np.arange(areamat.shape[1])
# y = np.arange(areamat.shape[0])
# X, Y = np.meshgrid(x, y)
# fig3 = plt.figure()
# ax3 = fig3.add_subplot(111, projection = '3d')
# # ax3.plot_surface(X, Y, areamat)
# Z = areamat.flatten()
# ax3.bar3d(X.ravel(), Y.ravel(), np.zeros_like(Z), 1, 1, Z)
# ax3.set_ylabel("Precipitate Label")
# ax3.set_xlabel("ImageNumber")
# ax3.set_yticks(key[:,1], key[:,0])
# plt.show()

x = np.arange(areamat.shape[1])
plt.figure(figsize=(8, 6))
for i in range(areamat.shape[0]):
    plt.plot(x, areamat[i], label= key[i][0])

plt.xlabel('Image Number')
plt.ylabel('Precipitate Area')
plt.legend(loc = "upper left", ncol = 2)
plt.grid(True)
plt.savefig(f"Results\\Multi Input\\AreavsTime.png", bbox_inches = "tight")
plt.show()

fname = "Results\\Multi Input\\output.csv"

with open(fname, 'w', newline = '') as f:
    cols = ["Image Number", "Label", "Aspect Ratio", "Mean Radius", "Equivalent Radius", "Area"]
    w = csv.writer(f)
    w.writerow(cols)
    for imno in d.keys():
        for k in d[imno].keys():
            w.writerow([imno, k] + d[imno][k])

def derivate(areamat):
    deri = []
    for row in areamat:
        der = []
        for i in range(len(row) - 1):
            der.append(row[i+1] - row[i])
        deri.append(der)
    return deri

deri = derivate(areamat)
deri = np.array(deri)

x = np.arange(deri.shape[1])
plt.figure(figsize=(8, 6))
for i in range(deri.shape[0]):
    plt.plot(x, deri[i], label= key[i][0])

plt.xlabel('Image Number')
plt.ylabel('Precipitate Area')
plt.legend(loc = "upper left", ncol = 2)
plt.grid(True)
plt.savefig(f"Results\\Multi Input\\DAreavsTime.png", bbox_inches = "tight")
plt.show()

labs = ["Label"] + list(key[:, 0])
labs = np.array(labs)

r, c = areamat.shape
areamat = np.vstack((np.zeros((1, c)), areamat))
labs = labs.reshape((r+1, 1))

areamat = np.hstack((labs, areamat))

for i in range(1, c+1):
    areamat[0, i] = str(i)

with open("Results\\Multi Input\\Areamat.csv", "w", newline = "") as f:
    wrt = csv.writer(f)
    wrt.writerows(areamat)