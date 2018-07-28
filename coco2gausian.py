import json
import os

from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab


class Coco2Gaussian():
    '''
    convert coco annotations to our Gaussian Json format
    '''



    def __init__(self, coco_datapath):

        self.__get_basic_info__()

        json_data = {
            "info": self.info,
            "vehicle_info": self.vehicle_info,
            "log_info": self.log_info
        }

        with open(os.path.join(coco_datapath, "Annotations" + "_" + ".json"), 'w') as jsonfile:
            json.dump(json_data, jsonfile, sort_keys=True, indent=4)



    def __get_basic_info__(self, ros_info=False):
        '''
        # get basic info such as description and vehicle/log info .etc
        :param self:
        :param ros_info:
        :return:
        '''

        self.info = {
            "year": 2018,
            "version": 'test_api_v1',
            "description": 'convert  coco2017 to gaussian dataset merging the thing & stuff tasks',
            "contributor": 'gaussian dl team',
            "device": 'coco images',
            "date_created": '2018-07-28'
        }

        self.vehicle_info = [{
            "id": 0,
            "hardware_version": '',
            "software_version": '',
            "sensor_list": [],
            "sensor_frequency": 0
        }]

        self.log_info = [{
            "id": 0,
            "type": '',
            "vehicle_id": 0,
            "location": '',
            "starting time": '',
            "end time": ''
        }]


if __name__ == "__main__":

    coco_datapath = './'
    Coco2Gaussian(coco_datapath)

