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

  # inverted_binary = ~image
  # Find the contours and store them in a list
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

def get_aspect__ratio():
   pass

img = cv2.imread("Untitled.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(type(gray))
cv2.imshow('Hello', gray)
cv2.waitKey(0)

img, img_lis = preprocess(gray)
cv2.imshow('Hello', img)
cv2.waitKey(0)


cv2.imshow('hello', img_lis[0])
cv2.waitKey(0)

barycents = np.zeros((len(img_lis), 6))

for i, preci in enumerate(img_lis):
  shor = np.sum(~preci, axis = 1)
  sver = np.sum(~preci, axis = 0)
  print(i, shor, sver)
  print(preci.shape, len(shor), len(sver))
  barx = 0
  bary = 0
  for k, sh in enumerate(shor):
    bary += k*sh
  bary = bary/np.sum(shor)
  for k, sv in enumerate(sver):
    barx += k*sv
  barx = barx/np.sum(sver)
  print(bary, barx)
  barycents[i, 0] = bary
  barycents[i, 1] = barx

print(barycents)

for i, perci in enumerate(img_lis):
  pass