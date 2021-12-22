#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import json
from typing_extensions import final
import numpy as np
import shutil
import pandas as pd
from tqdm import tqdm
from PIL import Image
import glob
from shutil import copy
import random

defect_label2name = {
    0: 'unknown', 
    1: 'escape_printing', 
    2: 'clogging_screen',
    3: 'broken_hole',
    4: 'toe_closing_defects',
    5: 'water_stain',
    6: 'smudginess',
    7: 'white_strip',
    8: 'hazy_printing',
    9: 'billet_defects',
    10: 'trachoma',
    11: 'color_smear',
    12: 'crease',
    13: 'false_positive',
    14: 'no_alignment'
}
defect_dir = "../data/defect_Images"
template_dir="../data/template_Images"
json_dir="../data/json_Files"

# train_defect_dir = "../data/train/defect_Images"
# template_dir="../data/template_Images"
# json_dir="../data/json_Files"
train_path = "../data/train/"
eval_path = "../data/eval/"
test_path = "../data/test/"

class Fabric2COCO:

    def __init__(self, mode="train"):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0
        self.mode = mode

    #                 json文件    疵点数据集 , 
    def to_coco(self, defect_dir, template_dir, json_dir):
        self._init_categories()
        
        # 遍历anno_file all files
        if os.path.exists(json_dir):
            filelist = os.listdir(json_dir)
            for f in tqdm(filelist):
                
                img_name = f[:-5] + '.jpg'
                img_path = os.path.join(defect_dir, img_name)
                json_path = os.path.join(json_dir ,f)
                image = Image.open(img_path)
                w, h = image.size
                # 目前只留（1）400*400（2）瑕疵图和模板图对应大小
                self.images.append(self._image(img_path, h, w))
                
                # open file and get img.size/bbox/defect_name
                json_file = pd.read_json(json_path)
                label = json_file['flaw_type'].to_list()[0]
                bbox = json_file['bbox'].to_dict()
                
                if bbox['y0'] < h and bbox['x0'] < w:
                    annotation = self._annotation(label, bbox, h, w)
                    self.annotations.append(annotation)
                    self.ann_id += 1
                self.img_id += 1
                instance = {}
        instance['info'] = 'fabric defect'
        instance['license'] = ['none']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    def _init_categories(self):
        for k, v in defect_label2name.items():
            category = {}
            category['id'] = k
            category['name'] = v
            category['supercategory'] = 'defect_name'
            self.categories.append(category)

    def _image(self, path, h, w):
        image = {}
        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path)
        return image

    def _annotation(self, label, bbox, h, w):
        area = (bbox['x1'] - bbox['x0']) * (bbox['y1'] - bbox['y0'])
        if area <= 0:
            print(bbox)
            input()
        points=[[bbox['x0'], bbox['y0']], [bbox['x1'], bbox['y0']], [bbox['x1'], bbox['y1']], [bbox['x0'], bbox['y1']]]
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = label
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._get_box(points, h, w)
        annotation['iscrowd'] = 0
        annotation['area'] = area
        return annotation

    def _get_box(self, points, img_h, img_w):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        '''coco,[x,y,w,h]'''
        w = max_x - min_x
        h = max_y - min_y
        if w > img_w:
            w = img_w
        if h > img_h:
            h = img_h
        return [min_x, min_y, w, h]

    def save_coco_json(self, instance, save_path):
        with open(save_path, 'w') as fp:
            json.dump(instance, fp, indent=1, separators=(',', ': '))


def delete(img_path, json_path, template_path):
    # 需要删除空白疵点png
    if os.path.exists(img_path):
        os.remove(img_path)
    # 删除对应的json
    os.remove(json_path)
    # 删除模板png
    if os.path.exists(template_path):
        os.remove(template_path)

def ifmatch():
    
    defectlist = os.listdir(defect_dir)
    defect_file = []
    for f in defectlist:
        defect_file.append(f.split('.')[0])
    
    templatelist = os.listdir(template_dir)
    template_file = []
    for f in templatelist:
        template_file.append(f.split('.')[0])
    
    jsonlist = os.listdir(json_dir)
    json_file = []
    for f in jsonlist:
        json_file.append(f.split('.')[0])

    
    for i in defect_file:
        if i not in template_file or i not in json_file:
            # print("数据集不匹配")
            break

def save400():
    counts = 0
    filelist = os.listdir(json_dir)
    for f in tqdm(filelist):
        img_name = f[:-5] + '.jpg'
        img_path = os.path.join(defect_dir, img_name)
        template_path = os.path.join(template_dir, img_name)
        json_path = os.path.join(json_dir ,f)
        try:
            image = Image.open(img_path)
            template = Image.open(template_path)
            json_path = os.path.join(json_dir, f)
            w, h = image.size
            w_i, h_i = template.size
            # 如果瑕疵图和模板图大小不一致，删除
            if w != w_i or h != h_i or w != 400 or h != 400:
                delete(img_path, json_path, template_path)
                continue
        except: # 图片打不开异常处理，删除
            delete(img_path, json_path, template_path)
            continue
        counts = counts + 1
    # print('    共有 {} 张400*400且瑕疵图和模板图对应的图片'.format(counts))
    return counts

def splitdata(train, eval, test):
    # print('+++ 划分数据集 ', train, ':', eval, ':', test)
    train_len = train/(train + eval + test)
    eval_len = (train + eval)/(train + eval + test)

    filelist = os.listdir(json_dir)
    random.shuffle(filelist)
    train_len = int(len(filelist) * train_len)
    eval_len = int(len(filelist) * eval_len)

    count = 0
    for f in tqdm(filelist):
        count = count + 1
        img_name = f[:-5] + '.jpg'
        img_path = os.path.join(defect_dir, img_name)
        template_path = os.path.join(template_dir, img_name)
        json_path = os.path.join(json_dir ,f)

        # 分别copy
        if count <= train_len:
            copy(img_path, train_path + 'defect_Images')
            copy(template_path, train_path + 'template_Images')
            copy(json_path, train_path + 'json_Files')
        elif count > train_len and count <= eval_len:
            copy(img_path, eval_path + 'defect_Images')
            copy(template_path, eval_path + 'template_Images')
            copy(json_path, eval_path + 'json_Files')
        else:
            copy(img_path, test_path + 'defect_Images')
            copy(template_path, test_path + 'template_Images')
            copy(json_path, test_path + 'json_Files')
    # print('--- 划分结束 --- train:{},eval:{},test:{}'.format(train_len, eval_len - train_len, len(filelist) - eval_len))

if __name__ == "__main__":

    # 1. 获取数据数量
    # print('    瑕疵图: {}'.format(len(glob.glob(defect_dir + '/*.jpg'))))        # 3580
    # print('    模板图: {}'.format(len(glob.glob(template_dir + '/*.jpg'))))      # 3580
    # print('    JSON文件: {}'.format(len(glob.glob(json_dir + '/*.json'))))       # 3580
    # 2. 判断文件一一对应，并且只保留400*400和模板图与瑕疵图大小对应的数据
    ifmatch() 
    # 3. 只保留400*400，且模板和瑕疵大小对应的数据(疵点布中存在空图片数据，删除 )
    counts = save400()
    # 4. 拆分数据集   8:1:1比例拆分
    splitdata(8, 1, 1)
    # json文件中bbox数据是否正确 
    # 5. 转coco格式
    # print('    转coco数据集')
    train_coco = Fabric2COCO()
    train_instance = train_coco.to_coco(train_path+'defect_Images', train_path+'template_Images', train_path+'json_Files')
    final_json = '../data/train/instances_train.json'
    if os.path.exists(final_json):
        os.remove(final_json)
    train_coco.save_coco_json(train_instance, final_json)

    eval_coco = Fabric2COCO()
    eval_instance = eval_coco.to_coco(eval_path+'defect_Images', eval_path+'template_Images', eval_path+'json_Files')
    final_json = '../data/eval/instances_eval.json'
    if os.path.exists(final_json):
        os.remove(final_json)
    eval_coco.save_coco_json(eval_instance, final_json)

    test_coco = Fabric2COCO()
    test_instance = test_coco.to_coco(test_path+'defect_Images', test_path+'template_Images', test_path+'json_Files')
    final_json = '../data/test/instances_test.json'
    if os.path.exists(final_json):
        os.remove(final_json)
    test_coco.save_coco_json(test_instance, final_json)

