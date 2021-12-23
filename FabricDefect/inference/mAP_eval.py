from mmdet.core import eval_map
from mmdet.datasets import build_dataset
import mmcv

results_file = 'out_12221650.pkl'
config_file = '../config/cascade_rcnn_r50_fpn_70e.py'


def evaluate(results, dataset):
    annotations = []
    for i in range(len(dataset)):
        ann = dataset.get_ann_info(i)
        annotations.append(ann)
    map_res = eval_map(results, annotations)
    return map_res


if __name__ == '__main__':
    results = mmcv.load(results_file)
    cfg = mmcv.Config.fromfile(config_file)

    dataset = build_dataset(cfg.data.test)

    evaluate(results, dataset)

