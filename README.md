# Precipitate Shape Quantification

The following is an implementation of the Consistent Quantification of Precipitate Shapes and Sizes in Two and Three Dimensions using Central Moments by Schleifer et. al.

## Literature Review and Methodology

The paper discusses the need for quantification of precipitate particles in the field of Computational Microstructure, and how it can be done. The prior methods had a drawback of depending on the orientation of the precipitate. In order to tackle this issue we make use of Central Moments of the particles.

The moments $\mu_{klm}$ are defined as the integral over the particle V
$$
\mu_{klm} = \int_V x^k y^l z^z dV
$$
Here x,y and z are the cartesian coordinates. The integer exponents k, l, and m decide the order of the moment as $(k+l+m)$

The central moments $\bar\mu_{klm}$ are defined as
$$
\bar\mu_{klm} = \int_V\bar x^k\bar y^l\bar z^m dV
$$

where $\bar x, \bar y, \bar z$ are the coordinates relative to the barycenter of each particle.

A interia matrix $\Lambda$ from the second-order central moments as

$$
\Lambda = 
\begin{bmatrix} 
\bar\mu_{020} + \bar\mu_{002} & -\bar\mu_{110} & -\bar\mu_{101}\\
-\bar\mu_{110} & \bar\mu_{200} + \bar\mu_{002} & -\bar\mu_{011}\\
-\bar\mu_{101} & -\bar\mu_{011} & \bar\mu_{200} + \bar\mu_{020}
\end{bmatrix} 
$$

Using the eigenvalues of this matrix the aspect ratio is caluclated.

$$
A = \sqrt{\frac{\lambda_2 + \lambda_3 - \lambda_1}{\lambda_1 + \lambda_2 - \lambda_3}}, B = \sqrt{\frac{\lambda_2 + \lambda_3 - \lambda_1}{\lambda_1 + \lambda_3 - \lambda_2}}
$$

For a 2D precipitate the interia matrix is defined in [MacSleyne et. al](https://doi.org/10.1016/j.actamat.2007.09.039)

## Code File Overview

### `init.py`

- This file is called by the other files to import all the required libraries together.

### `reprod2D.py`

- Objective - Accept an Image, detect the precipitates and report their Aspect ratio.
- Method
  - First the image is accepted and converted to grayscale.
  - The `preprocess` function performs the following tasks - 
    - Converts the image to a binary image using adaptive thresholding which decides the value for threshold for each pixel on the basis of its neighbours.
    - Draws contours using the Suzuki Algorithm, that follows the boundary of an object, and generates a sequence of pixels that approximate the contours.
    - Using the contours a bounding box is generated around the precipitate and it is sliced out of the image.
    - The method then returns a sequence of such slices.
  - The `get_aspect__ratio` function calculates the aspect ratio of the precipitate by applying the above mentioned formula.
- Drawbacks - Precipitates that are cut due to the boundary are not considered.

### `reprod2D_Test.py`

- Objective - To test the functions from `reprod2D.py` on the daataset provided with the paper.
- Graphs are poltted which show that the calculated aspect ratio is equal to the expected aspect ratio. The graphs shows a minor deviation at higher values.
- Drawbacks - Precipitates that are cut due to the boundary are not considered.

### `reprod2D-2.py`

- Objective - To accept an image, calculate the aspect ratio and overcome the drawbacks of the predecessor.
- Methods
  - Contours
    - This method is already explained in the above sections.
    - In this implementation the user is shown a precipitate and asked whether they want to consider it.
    - This requires manual inputs.
  - Hoshen-Kopelman Algorithm
    - This is an algorithm that is used to find connected components, in this case it is used to find clusters.
    - The algorithm checks the value of each pixel, and its neighbours and determines whether it is a part of cluster or not.
    - Further if the input image is a periodic image then a modification is made in the algorithm to connect the two parts of a precipitate that is divided by the border.