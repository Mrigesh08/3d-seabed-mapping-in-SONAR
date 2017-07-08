# 3d-seabed-mapping-in-SONAR
This repository contains python code to convert sound intensity data received from a 8X4 hydrophone array into a 3D map of the seafloor.

# Features
..* Capable of generating a 2D plot of the sound intensity data
..* Capable of generating a 3D plot of the sound intensity data
..* Algorithm can detect objects above the sea surface as well as below

# Anti-Features
..* Since there is no standard format for representing the sound intensity data, all the variables have been hard coded in. This means that if the data file is some other format, The code would generate false plot

# Assumptions
..* Data is according to the format given in the file dataFormat.txt. The hydrophone data is the actual data we are working on.
..* Each ping consists of 1536 samples and each sample will have 32 readings.
..* Water will reflect sound with low intensity(in the range 0-50)
..* Sea Bed will reflect the sound with higher intensity(in the range 100-150)
..* Objects will reflect the sound waves of high intensities(in the range 175-195)