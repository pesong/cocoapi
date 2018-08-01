import json
import os

import yaml
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab

from coco2gaussian.getAnnotation import GetAnn


class GaussianJson():
    '''
    convert coco annotations to our Gaussian Json format
    '''

    def __init__(self, coco_data_dir):
        self.newid = 0
        self.coco_data_dir = coco_data_dir


    def generate_gaussian_json(self):
        self.__get_basic_info__()
        self.__get_categories__()
        self.__get_img_ann_()

        json_data = {
            "info": self.info,
            "vehicle_info": self.vehicle_info,
            "log_info": self.log_info,
            "categories": self.categories,
            "image": self.imgs,
            # "annotation": self.anns_val
        }

        with open(os.path.join(self.coco_data_dir, "Annotations" + "_" + ".json"), 'w') as jsonfile:
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
            "id": '',
            "hardware_version": '',
            "software_version": '',
            "sensor_list": [],
            "sensor_frequency": 0
        }]

        self.log_info = [{
            "id": '',
            "type": '',
            "vehicle_id": 0,
            "location": '',
            "starting time": '',
            "end time": ''
        }]


    def __get_categories__(self):

        self.categories = []
        f = open(r'/media/pesong/e/dl_gaussian/data/coco/cocoapi/coco2gaussian/categories.yml', 'r')
        catseqs = yaml.load(f)
        for super, seqs in catseqs.items():
            for name, id in seqs.items():
                self.categories.append({"supercategory": super, "name": name, "id": id})


    def __get_img_ann_(self):
        coco_ann = GetAnn()
        img_ids_val = coco_ann.get_gaussian_imgIds('val2017')
        anns_list, img_list = coco_ann.get_img_ann_list(img_ids_val)

        self.anns_val = coco_ann.mask2polys(anns_list)

        # reset img id and note the mapping dict
        img_newid_map = {}


        # get gaussian imgs
        gs_imgs = []
        for img in img_list:
            self.newid += 1
            gs_img = {}

            # convert gaussian dataset and note the mapping
            img_newid_map[self.newid] = img['id']
            # gs_img['id'] = self.newid
            # gs_img['file_name'] = self.newid + '.jpg'

            # for validation
            gs_img['id'] = img['id']
            gs_img['file_name'] = img['file_name']
            gs_img['coco_url'] = img['coco_url']

            gs_img['width'] = img['width']
            gs_img['height'] = img['height']
            gs_img['depth'] = 3
            gs_img['device'] = 'camera'
            gs_img['date_captured'] = img['date_captured']
            gs_img['rosbag_name'] = ''
            gs_img['encode_type'] = 'rgb'
            gs_img['is_synthetic'] = 'no'
            gs_img['vehicle_info_id'] = ''
            gs_img['log_info_id'] = ''
            gs_img['weather'] = ''
            gs_imgs.append(gs_img)

        self.imgs = gs_imgs

        # get the  map between gaussian imgid and coco imgid
        self.img_newid_map = img_newid_map







if __name__ == "__main__":

    coco_datapath = './'
    gs_json = GaussianJson(coco_datapath)
    gs_json.generate_gaussian_json()






