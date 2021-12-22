#!/usr/bin/env bash

# python -m torch.distributed.launch --nproc_per_node=7 ./test.py ../config/fabric_defect/cascade_rcnn_r50_fpn_70e.py ../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest-submi-3f613116.pth

PYTHON=${PYTHON:-"python"}

CONFIG=../config/fabric_defect/cascade_rcnn_r50_fpn_70e.py
CHECKPOINT=../data/work_dirs/cascade_rcnn_r50_fpn_70e/latest-submi-3f613116.pth
GPUS=7

$PYTHON -m torch.distributed.launch --nproc_per_node=$GPUS \
    $(dirname "$0")/test.py $CONFIG $CHECKPOINT --launcher pytorch ${@:4}
