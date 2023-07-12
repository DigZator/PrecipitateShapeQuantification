from init import *
from reprod2D import *

# Set the original width and height of the image
original_width = 5000
original_height = 5000

# Set the desired reduced width and height
red_wh = [[6000, 6000],
          [5000, 5000],
          [2500, 2500],
          [2000, 2000],
          [1500, 1500],
          [1000, 1000],
          [500, 500],
          [250, 250],
          [100, 100],
          [50, 50]]

# red_wh = [[500, 500]]

reduced_width = 200
reduced_height = 200

# Set the center coordinates and radii of the ellipse in the original image
center_x = original_width // 2
center_y = original_height // 2
radius_x = 2000
radius_y = 200

# Set the color of the ellipse
color = 1

og_img = []

radii = [2000, 400, 200, 100, 50]

with open("outputresolution5.csv", "w", newline="") as f:
    wrt = csv.writer(f)
    wrt.writerow(["X", radius_x, "Y", radius_y, "Aspect Ratio", radius_y/radius_x])
    for radius_y in radii:
        for ang in range(46):
            # Create the original image with the ellipse
            original_image = np.zeros((original_height, original_width), dtype=np.uint8)
            cv2.ellipse(original_image, (center_x, center_y), (radius_x, radius_y), ang, 0, 360, color, -1)
            og_img.append(original_image)
        for rw, rh in red_wh:
            wrt.writerow([f"Resolution - {rw}"])
            wrt.writerow(["Angle", "A", "RM", "RE", "Area", "Exp"])
            for ang in range(46):
                # Resize the original image to the reduced dimensions
                reduced_image = cv2.resize(og_img[ang], (rw, rh), interpolation=cv2.INTER_AREA)
                precipitates, clusters = extract_precipitates(reduced_image, off_set = 0, wkey = False)
                preci = precipitates[0]
                # plt.imshow(preci)
                # plt.show(block = False)
                # plt.pause(1)
                # plt.close()
                A, Re, Rm = get_aspect_ratio(preci = preci, flip = False)
                area = np.sum(preci)
                if ang == 0:
                    m, n = preci.shape
                    Asp = n/m
                print(f"A - {A:.2f}, Re - {Re:.2f}, Rm - {Rm:.2f}, Asp - {Asp:.2f}, Area - {area}")
                wrt.writerow([ang, A, Re, Rm, area, Asp])
            print()