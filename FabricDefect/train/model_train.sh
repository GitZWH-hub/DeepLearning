CUDA_VISIBLE_DEVICES=0,1,2,4,5,6 ./dist_train.sh ../config/cascade_rcnn_r50_fpn_70e.py 6
python publish_model.py ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest.pth ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest-submit.pth
