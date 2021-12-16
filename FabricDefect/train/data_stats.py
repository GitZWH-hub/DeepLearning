import json
import os

if __name__ == '__main__':
    image_counter = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0
    }
    defect_info_path = "../data/json_Files"
    files = os.listdir(defect_info_path)
    for file in files:
        with open(defect_info_path + "/" + file) as f:
            defect_json = json.load(f)
            image_counter[defect_json['flaw_type']] += 1
    print(image_counter)
    """
    {
      0: 559, 
      1: 353, 
      2: 387, 
      3: 39, 
      4: 553, 
      5: 21, 
      6: 157, 
      7: 24, 
      8: 210, 
      9: 11, 
      10: 1, 
      11: 154, 
      12: 15, 
      13: 385, 
      14: 711
    }
    """
