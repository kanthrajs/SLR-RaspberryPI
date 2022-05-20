#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import geocoder
import socket
import pandas as pd
import traceback
import time
from waveshare_epd import epd2in13_V2
import logging
import sys
import argparse
import os
picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
datadir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'data')
if os.path.exists(libdir):
    sys.path.append(libdir)


parser = argparse.ArgumentParser(description="boolean value for arguments")
parser.add_argument('-off', '--off', action='store_true')
args = parser.parse_args()
# print(args.off)

if(args.off):
    logging.info("Clear from previous...")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
else:
    def get_ip():  # get IP address from raspberry pi
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    print(get_ip())

    def get_city(ip):  # get city name from IP address
        g = geocoder.ip(ip)
        g = geocoder.ip('me')
        return g.city

    # Read CSV file into DataFrame df
    csv_file = os.path.join(datadir, 'SLR_Zipcode.csv')
    data = pd.read_csv(csv_file, usecols=['city', 'avg_risk_score_all'])

    def risk_value():  # get risk value from detected city 'eg:Boston'
        name = get_city(get_ip())
        new_data = data.loc[data['city'] == name]
        return new_data.max()['avg_risk_score_all']

    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd2in13_V2 Demo with only time")

        epd = epd2in13_V2.EPD()
        logging.info("init and Clear")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing on the image
        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        # welcome text
        logging.info("1.Welcome Text...")
        image = Image.new('1', (epd.height, epd.width),
                          255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        #draw.rectangle([(0,0),(50,50)],outline = 0)

        draw.text((30, 60), 'Welcome CS682', font=font24, fill=0)
        epd.display(epd.getbuffer(image))
        time.sleep(2)

        # # partial update
        logging.info("4.show time...")
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(time_image))

        epd.init(epd.PART_UPDATE)
        num = 0

        time_draw.rectangle((0, 0, 0, 0), fill=255)
        time_draw.text((0, 0), "City: " + get_city(get_ip()),
                       font=font24, fill=0)
        time_draw.rectangle((30, 60, 30, 60), fill=255)
        time_draw.text((30, 60), "Risk Score: " +
                       str(risk_value()), font=font24, fill=0)
        epd.displayPartial(epd.getbuffer(time_image))

        # epd.Clear(0xFF)
        # logging.info("Clear...")
        # epd.init(epd.FULL_UPDATE)
        # epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in13_V2.epdconfig.module_exit()
        exit()
