# Precipitate Shape Quantification

The following is an implementation of the Consistent Quantification of Precipitate Shapes and Sizes in Two and Three Dimensions using Central Moments by Schleifer et. al.

## Literature Review and Methodology

The paper discusses the need for quanitification of precipitate particles in the field of Computational Microstructure, and how it can be done. The prior methods had a drawback of depending on the orientation of the precipitate. In order to tackle this issue we make use of Central Moments of the particles.

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