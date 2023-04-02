from init import *
from reprod2D_Test import get_aspect_ratio

datContent = [i.strip().split() for i in open("./Comp1000.dat").readlines()]
# datContent = [i.strip().split() for i in open("./Comp10000.dat").readlines()]

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
img2 = (img2 * 255).astype(np.uint8)
print(np.max(img))

cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.imshow("Image", img2)
cv2.waitKey(0)


cimg = img2.copy()
# cimg = (np.where(cimg >= 46, 255, 0)).astype(np.uint8)
bin_img = cv2.adaptiveThreshold(cimg,
                                255,
                                cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY,
                                31,
                                4) #5,0.044

# invbin = ~bin_img

cv2.imshow("Image", cimg)
cv2.waitKey(0)

cv2.imshow("Image", bin_img)
cv2.waitKey(0)

contours, _ = cv2.findContours(bin_img,
                               cv2. RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)

img_lis = []
bbox_lis = []

out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
out2 = out.copy()

out = cv2.drawContours(out, contours, -1, (0, 255, 0), 1)

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if (cv2.contourArea(c)) > 100:
        img_lis.append(bin_img[y:(y+h), x:(x+w)])
        bbox_lis.append([x,y,w,h])
        cv2.rectangle(out2, (x,y), (x+w,y+h), (255,0,0), 1)

cv2.imshow("Image", out)
cv2.waitKey(0)

takecon, takebbox, takeimg = [], [], []
for i in range(len(img_lis)):
    cv2.imshow("Precipitate", img_lis[i])
    take = cv2.waitKey(0)
    # take = int(input("Consider this precipitate"))
    if take == ord('y') or take == ord('Y') or take == ord('1'):
        # takecon.append(contours[i])
        takebbox.append(bbox_lis[i])
        takeimg.append(img_lis[i])
    cv2.destroyAllWindows()
    
    Alist, RMlist, RElist = [], [], []

for preci in takeimg:
    A, RM, RE = get_aspect_ratio(preci)
    print(f"A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}")
    Alist.append(A)
    RMlist.append(RM)
    RElist.append(RE)