from init import *
def preprocess(img):
  # Pass the GRAY image to the function
  image = img.copy()

  # # To make image more suitable to detect contours(to increase or decrease seprartion between two objects)
  # image = cv2.erode(image, None, iterations=4)
  # image = cv2.dilate(image, None, iterations=1)

  # # Convert the image to grayscale and then to binary
  # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # blurred = cv2.GaussianBlur(gray, (7, 7), 0)
  # #Here, Adaptive thresholding is used to handle different lighting conditions
  binary = cv2.adaptiveThreshold(image, 
                            255, 
                            cv2.ADAPTIVE_THRESH_MEAN_C, 
                            cv2.THRESH_BINARY, 
                            31, 
                            10)

  # #Invert the image for contour detection
  inverted_binary = ~binary

  contours, _ = cv2.findContours(inverted_binary,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE)
  
  # Print the total number of contours that were detected
  print('Total number of contours detected: ' + str(len(contours)))

  # Predict bounding boxes around all contours and store the cropped sections of images in a list
  img_lis = []
  bbox_lis = []
  out = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  for c in contours:
    x, y, w, h = cv2.boundingRect(c)
      # To filter out tiny boxes(variable that can be changed)
    if (cv2.contourArea(c)) > 100:
      img_lis.append(img[y:(y+h),x:(x+w)])
      bbox_lis.append([x,y,w,h])
    
      cv2.rectangle(out, (x,y), (x+w,y+h), (255,0,0), 1)
  
  # result,b_values = get_aspect_ratio(img_lis)
  # final_img = post_process(img,bbox_lis,result)
  return out, img_lis

def get_aspect__ratio(preci):
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
  print(bary, barx)
  µ020 = 0
  µ200 = 0
  µ110 = 0
  z = 1
  for y in range(verlen):
    for x in range(horlen):
      µ020 += ((x - barx)**0) * ((y - bary)**2) * (z**0) * preci[y,x]
      µ200 += ((x - barx)**2) * ((y - bary)**0) * (z**0) * preci[y,x] 
      µ110 += ((x - barx)**1) * ((y - bary)**1) * (z**0) * preci[y,x]
  inermat = np.array([[µ200, µ110],
                      [µ110, µ020]])
  w, v = np.linalg.eig(inermat)
  # print(w)
  w.sort()
  print(w)
  A = np.sqrt(w[1]/w[0])
  RM = ((np.sum(sver)/np.pi)*A)**0.5
  RE = RM * (A**(-1/3))
  return A, RM, RE

# dir_path = 'D:\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\2D_370px_rotated\\'
dir_path = 'D:\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\2D_370px\\'
dir_path = 'D:\\Internship\\PrecipitateShapeQuantification\\benchmark_shapes\\2D_5000px\\'

Agive = []
Acalc = []

for filename in os.listdir(dir_path):
  img = cv2.imread(dir_path + filename)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img, img_lis = preprocess(gray)
  # cv2.imshow(filename, img)
  # cv2.waitKey(0)
  iner_val = []
  # cv2.imshow(filename, img_lis[0])
  # cv2.waitKey(0)
  print(filename)
  for i, preci in enumerate(img_lis):
    preci = np.array(preci/255, dtype = int)
    A, RM, RE = get_aspect__ratio(preci)
    print(f"A = {A:.2f}, RM = {RM:.2f}, RE = {RE:.2f}")
    Acalc.append(A)
    # Agive.append(float(filename.split("_")[0]))
    Agive.append(len(preci[0])/len(preci))

plt.figure()
plt.scatter(Agive, Acalc, c = 'blue')
plt.plot([0,20], [0,20])
plt.show()