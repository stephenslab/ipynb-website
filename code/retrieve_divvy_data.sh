#!/bin/bash

# Download and unzip the Divvy data.
cd ../data
wget https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2016_Q1Q2.zip
wget https://s3.amazonaws.com/divvy-data/tripdata/Divvy_Trips_2016_Q3Q4.zip
unzip Divvy_Trips_2016_Q1Q2.zip
unzip Divvy_Trips_2016_Q3Q4.zip

# Arrange the files a bit better and clean up (delete) files that we
# won't need for the data analysis.
mv -f Divvy_Trips_2016_Q1Q2/* .
rmdir Divvy_Trips_2016_Q1Q2
rm -f *.zip
rm -f README_2016_Q3.txt README_2016_Q4.txt
