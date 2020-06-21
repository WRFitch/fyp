#!/bin/bash -i
cd /src/fyp
xdg-open 'https://github.com/WRFitch/fyp/'
conda activate fyp_devenv 
jupyter lab 
