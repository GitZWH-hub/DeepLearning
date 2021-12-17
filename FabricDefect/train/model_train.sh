CUDA_VISIBLE_DEVICES=0,1,2,3 ./dist_train.sh ../config/fabric_defect/cascade_rcnn_r50_fpn_70e.py 4
CUDA_VISIBLE_DEVICES=0,1,2,3 ./dist_train.sh ../config/fabric_defect/cascade_rcnn_r50_fpn_400.py 4
python publish_model.py ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest.pth ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest-submit.pth
python publish_model.py ../data/work_dirs/cascade_rcnn_r50_fpn_400/latest.pth ../data/work_dirs/cascade_rcnn_r50_fpn_400/latest-submit.pth
