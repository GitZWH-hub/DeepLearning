#*utf-8*
import os
import json
from typing_extensions import final
import numpy as np
import shutil
import pandas as pd
from tqdm import tqdm
from PIL import Image
import glob

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
                # print(f)
                # get image path
                img_name = f[:-5] + '.jpg'
                img_path = os.path.join(defect_dir, img_name)
                try:
                    image = Image.open(img_path)
                    json_path = os.path.join(json_dir, f)
                except:
                    # 需要删除空白疵点png
                    if os.path.exists(img_path):
                        os.remove(img_path)
                    # 删除模板png
                    os.remove(os.path.join(json_dir, f))
                    # 删除对应的json
                    template_path = os.path.join(template_dir, img_name)
                    if os.path.exists(template_path):
                        os.remove(template_path)
                    continue

                w, h = image.size
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


def ifmatch(defect_dir, template_dir, json_dir):
    
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
            print("数据集不匹配")
            break


if __name__ == "__main__":
    defect_dir = "../data/defect_Images"
    template_dir="../data/template_Images"
    json_dir="../data/json_Files"
    # 1. 获取数据数量
    print('    瑕疵图: {}'.format(len(glob.glob(defect_dir + '/*.jpg'))))        # 3580
    print('    模板图: {}'.format(len(glob.glob(template_dir + '/*.jpg'))))      # 3580
    print('    JSON文件: {}'.format(len(glob.glob(json_dir + '/*.json'))))         # 3580
    # 2. 判断文件一一对应
    # ifmatch(defect_dir, template_dir, json_dir)        # 结果：对应
    # 3. 疵点布中存在空图片数据，删除  4. json文件中bbox数据是否正确 5. 转coco格式 (另外图片大小也不一样，要怎么处理？)


    fabric2coco = Fabric2COCO()
    train_instance = fabric2coco.to_coco(defect_dir, template_dir, json_dir)
    final_json = '../data/instances_20211214.json'
    if os.path.exists(final_json):
        os.remove(final_json)
    fabric2coco.save_coco_json(train_instance, final_json)


