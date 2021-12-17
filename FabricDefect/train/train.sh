#!/bin/bash
echo $(pwd)
echo '+++ 数据整合开始 +++'
# 疵点图片文件夹defect_Images
mkdir -p ../data/defect_Images
# 模板图片文件夹template_Images
mkdir -p ../data/template_Images
# json文件夹
mkdir -p ../data/json_Files
# 预训练模型
mkdir -p ../data/pretrained

# 拷贝所有模板图片到template_Images
rm -r ../data/template_Images/*.jpg
cp ../fabric_data/temp/*/*.jpg ../data/template_Images/
wait
# 拷贝所有疵点图片到defect_Images
rm -r ../data/defect_Images/*.jpg
cp -r ../fabric_data/trgt/*/*.jpg ../data/defect_Images/
wait
# 拷贝所有json文件到json_Files
rm -r ../data/json_Files/*.json
cp ../fabric_data/label_json/*/*.json ../data/json_Files/
echo '--- 数据整合结束 ---'
sleep 1
# # 转换有瑕疵的样本为coco格式
echo '+++ 开始数据预处理 +++'
python fabric2coco.py
echo '--- 数据预处理结束 ---'

# # 使用mmdetection官方开源的casacde-rcnn-r50-fpn-2x的COCO预训练模型
# wget https://open-mmlab.oss-cn-beijing.aliyuncs.com/mmdetection/models/cascade_rcnn_r50_fpn_20e_20181123-db483a09.pth -O ../data/pretrained
# # 进行转换变为支持CFRCNN模型的预训练模型
# python transorfarm_concatenate_model.py

# CUDA_VISIBLE_DEVICES=0,1,2,3 ./dist_train.sh ../config/cascade_rcnn_r50_fpn_70e.py 4
# CUDA_VISIBLE_DEVICES=0,1,2,3 ./dist_train.sh ../config/cascade_rcnn_r50_fpn_400.py 4
# python publish_model.py ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest.pth ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest-submit.pth
# python publish_model.py ../data/work_dirs/cascade_rcnn_r50_fpn_400/latest.pth ../data/work_dirs/cascade_rcnn_r50_fpn_400/latest-submit.pth




