# ImageAreaProcessing

This is the first attempt of creating a program that can take an image of a grade/driveway/raod and calculate
an area in square footage. Once the area is selected the image is convereted into a binary file and a transform matrix is computed
to warp the image into a top-down view of the area for an accurate measurement accounting for the angle at which the picture
was taken. Countours are selected from the boundary selected and the length of each boundary is used to calculate the area
in pixels. The area is then converted into square footage with a scale factor based on the length of the reference.

To use the program start with changing line 84 to the name of the file you are trying to process. The reference length should be known
in feet and identifiable in the picture. Change the known reference length accordingly. Running the program will prompt you to select all
4 four corners in order (topleft, topright, bottomleft, bottomright) and the refernce point. 6 points in total 4 for the area and 2 for
the reference distance. 

