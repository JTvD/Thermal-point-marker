# Thermal point marker
Thermal data processing is a complex procedure which usually involves multiple steps.
An example of my typical analysis flows is given in figure 1:
![Themal analysis pipeline](example thermal data processing pipeline.png)

For the data extraction various scripts are available, for example: [flir_thermal](https://github.com/JTvD/flir_thermal/tree/main).
These scripts are used for the follow up step of point temperature extraction.
Which can be done manually, for example to track a leaf through time. Or automated for stationary objects like a mug filled with iceblocks.

Input is a falsecolor thermal image to select the points on and a CSv containing the temperature values.

The image below gives an example of the manual marking process:
![Manual marking](manually mark points.png)

And this is an example output of the automated process (point_temperature.csv):
| Source_file    | 206_74 | 306_100 |
|----------------|--------|---------|
| e8xt2_thermal  | 0.27   | 11.69   |
| e8xt_thermal   | 0.27   | 11.69   |

The first column is the filename. The other colomn names are the X_Y coordinates of the selected points followed by the temperature values of that specific point in the image.
