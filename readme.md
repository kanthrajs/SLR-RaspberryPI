This file assumes that you have RaspberryPI and succuessfully runs basic python code.   
A brief description of the use of this project is here:

## Basic information:
This demo gets the location ip,city from RaspberryPI and detects sealevel-riskfactor.   
Data to evaluate riskfactor obtained here: https://firststreet.org/data-access/public-access/

Install from root folder of your project.   

## 1.Installation library:
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo pip3 install RPi.GPIO
    sudo pip3 install geocoder
    

## 2. Preparing from setup.py file:
    sudo pip3 install -r requirements.txt
    sudo pip3 install .

## 3. Basic use:
    cd slr/
    sudo python3 risk_factor.py
