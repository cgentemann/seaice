#import schedule
import time
import os
import logging
from get_masie_file_running import get_extent
from put_masie_file_running import put_extent
from datetime import datetime
from send_email_extent_running import send_email_extent
from plot_ice_extent_running import plot_ice_extent
from pathlib import Path

def main():

    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logfile_name = 'extent'+ str(datetime.now().timetuple().tm_yday)+'.log'

    # Find users home directory
    home = os.path.expanduser('~')

    logging.basicConfig(filename=home+'/logs/'+logfile_name, level=logging.INFO)

    # Append data path to home directory
    data_path = home+"/Project_Data/Arctic_PRIZE/Data/Ice_Extent/current/"
    tools_path = home+"/Project_Data/Arctic_PRIZE/Data/Ice_Extent/Tools/"

    import numpy as np
    logging.info('Started')

    ftp_file = 0

    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    yday_now = datetime.now().timetuple().tm_yday
    yday_now = yday_now - 3 
    yday_now_str = str(yday_now).zfill(3)

    filename = 'masie_all_r00_v01_2017'+yday_now_str+'_4km.tif'
    fig_file = 'masie_all_r00_v01_2017'+yday_now_str+'_4km.png'

    ftp_file_found = Path(data_path+filename)
    fig_file_found = Path(data_path+fig_file)

    if ftp_file_found.is_file():
        logging.info('---file already exist in computer--@'+filename+' '+now)
        if fig_file_found.is_file():
            logging.info('---figure already exist in computer--@'+fig_file+' '+now)
            #put_extent(fig_file,data_path)
            #send_email_extent(filename)
        else:
            plot_ice_extent(filename,data_path,tools_path)
            logging.info(fig_file)
            #put_extent(fig_file,data_path)
            #send_email_extent(filename)
    else:
        logging.info("---no file in computer..."+filename+' '+now+yday_now_str)
        ftp_file = get_extent(filename,data_path)
        if ftp_file == 1:
            #print("---file found in ftp downloaded..."+filename)
             plot_ice_extent(filename,data_path,tools_path)
             logging.info(fig_file)
             #put_extent(fig_file,data_path)
             #send_email_extent(filename)
        else:
            logging.info("---file NOT found in ftp..."+filename) 

    logging.info("___ending processing...@"+now)

if __name__ == "__main__":
    main()
