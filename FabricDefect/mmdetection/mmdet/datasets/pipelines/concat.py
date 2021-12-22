import mmcv
import numpy as np
import cv2

from ..builder import PIPELINES


@PIPELINES.register_module()
class Concat(object):
    """Concat two image.

    Args:
        template_path: template images path
    """

    def __init__(self, template_path):
        self.template_path = template_path

    def __call__(self, results):
        if 'concat_img' not in results or results['concat_img'] is None:
            template_name = 'template_' + results['img_info']['filename'].split('_')[0] + '.jpg'
            template_im_name = self.template_path + results['img_info']['filename']  # .split('.')[0] + '/' + template_name
            # img_temp = mmcv.imread(template_im_name)
            img_temp = cv2.imread(template_im_name)
            print(f'template_im_name={template_im_name}')
            print(f'template shape = {img_temp.shape}')
            print(f'img shape = {img_temp.shape}')
            print('----------------------------')
            results['img'] = np.concatenate([results['img'], img_temp], axis=2)
            print(results['img'].shape)
            results['concat'] = True
        else:
            results['img'] = np.concatenate([results['img'], results['concat_img']], axis=2)
            results['concat'] = True
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__
        repr_str += '(template_path={})'.format(
            self.template_path)
        return repr_str