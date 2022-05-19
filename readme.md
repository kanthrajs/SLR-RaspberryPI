This file assumes that you have RaspberryPI and succuessfully runs basic python code.   
A brief description of the use of this project is here:

## Basic information:
This demo gets the location ip,city from RaspberryPI and detects sealevel-riskfactor.   
Data to evaluate riskfactor obtained here: https://firststreet.org/data-access/public-access/


## 1.Installation library (from root folder):
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo pip3 install RPi.GPIO
    sudo pip3 install geocoder
    

## 2. Preparing from setup.py file (from root folder):
    pip3 install -r requirements.txt
    pip3 install .

## 3. Basic use:
Since this project is a comprehensive project, you may need to read the following for use:
You can view the test program in the slr\ directory.

      sudo python3 risk_factor.py
