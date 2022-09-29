#!/usr/bin/env python
# -*- coding:utf-8 -*-
# AUTHOR: Ti Bai
# EMAIL: tibaiw@gmail.com
# AFFILIATION: MAIA Lab | UT Southwestern Medical Center
# DATETIME: 9/29/2022

import os
import json
import random


if __name__ == '__main__':
    testing_size = 40
    num_fold = 5
    data_root = r'D:\data\1_Challenge\AMOS22\AMOS22'
    dataset_json = r'task1_dataset.json'
    output_name = r'./task1_AMOS.json'

    with open(os.path.join(data_root, dataset_json), 'r') as f:
        original_dataset_json = json.load(f)

    original_training_json = original_dataset_json['training']
    random.shuffle(original_training_json)

    new_testing = original_training_json[:40]
    new_training = original_training_json[40:]

    fold_size = len(new_training) // num_fold
    for i, current_training_sample in enumerate(new_training):
        new_training[i]['fold'] = current_fold = min(i // fold_size, num_fold - 1)

    with open(output_name, 'w') as f:
        json.dump({'training': new_training, 'testing': new_testing}, f)
    
    print('Congrats! May the force be with you ...')
