#!/usr/bin/env python
# -*- coding:utf-8 -*-
# AUTHOR: Ti Bai
# EMAIL: tibaiw@gmail.com
# AFFILIATION: MAIA Lab | UT Southwestern Medical Center
# DATETIME: 9/22/2022

# sys
import os
import shutil

# monai
from monai.apps.auto3dseg import (
    DataAnalyzer,
    BundleGen,
    AlgoEnsembleBestN,
    AlgoEnsembleBuilder,
    export_bundle_algo_history,
    import_bundle_algo_history,
)
from monai.auto3dseg import algo_to_pickle
from monai.bundle.config_parser import ConfigParser


if __name__ == '__main__':
    ### setup the experiement parameters
    is_data_analysis = True
    need_customized_train_params = False

    data_root = r'./data'
    datalist_file = r'./dataset.json'
    result_dir = r'result'
    dataset_name = 'OAR'

    num_fold = 5
    model_name = ['segresnet_small'] # choose from ["segresnet_small", "segresnet", "segresnet2d", "dints", "swinunetr"]
    template_path = r'assets/algorithm_templates'
    task = 'segmentation'
    modality = 'CT'
    is_ensemble = False ##### ALWAYS SET IT AS FALSE UNLESS YOU REVISE THIS SCRIPT!!!

    train_param = {}
    if need_customized_train_params:
        train_data_size = 100
        num_iterations = 100000
        num_images_per_batch = 1
        num_iterations_per_validation = 1000
        train_param = {
            "num_iterations": num_iterations,
            "num_iterations_per_validation": num_iterations_per_validation,
            "num_images_per_batch": num_images_per_batch,
            "num_epochs": num_iterations // (train_data_size // num_images_per_batch),
            "num_warmup_iterations": int(0.01 * num_iterations),
        }

    # step 0: prepare the environment
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

    data_src_cfg = {
        "name": dataset_name,
        "task": task,
        "modality": modality,
        "datalist": datalist_file,
        "dataroot": data_root,
    }
    input = os.path.join(result_dir, 'input.yaml')
    ConfigParser.export_config_file(data_src_cfg, input)

    datastats_file = os.path.join(result_dir, 'data_stats.yaml')

    # step 1: Data Analysis
    print('Step 1: Analyzing the dataset and saving the results to {} ...'.format(datastats_file))
    if is_data_analysis:
        analyser = DataAnalyzer(datalist_file, data_root, output_path=datastats_file)
        datastat = analyser.get_all_case_stats()

    # step 2: Algorithm Generation (algo_gen)
    print('Step 2: Generating the algorithm based on template from {} and saving the results to {} ...'.format(template_path, result_dir))
    if not os.path.exists(os.path.join(result_dir, 'algorithm_templates')):
        shutil.copytree(template_path, os.path.join(result_dir, 'algorithm_templates'))
    default_algos = {
        "segresnet_small": dict(_target_="segresnet_small.scripts.algo.SegresnetAlgo",
                          template_path=os.path.join(result_dir, "algorithm_templates", "segresnet_small")),
        "segresnet": dict(_target_="segresnet.scripts.algo.SegresnetAlgo",
                          template_path=os.path.join(result_dir, "algorithm_templates", "segresnet")),
        "segresnet2d": dict(_target_="segresnet2d.scripts.algo.Segresnet2dAlgo",
                            template_path=os.path.join(result_dir, "algorithm_templates", "segresnet2d")),
        "dints": dict(_target_="dints.scripts.algo.DintsAlgo",
                      template_path=os.path.join(result_dir, "algorithm_templates", 'dints')),
        "swinunetr": dict(_target_="swinunetr.scripts.algo.SwinunetrAlgo",
                          template_path=os.path.join(result_dir, "algorithm_templates", 'swinunetr'))
    }

    used_algorithms = {x: default_algos[x] for x in model_name if x in default_algos}

    bundle_generator = BundleGen(
        algo_path=result_dir,
        algos=used_algorithms,
        data_stats_filename=datastats_file,
        data_src_cfg_name=input,
    )

    bundle_generator.generate(result_dir, num_fold=num_fold)

    # Getting and Saving the history to hard drive
    history = bundle_generator.get_history()
    export_bundle_algo_history(history)

    # step 3: generate the train command
    print('Step 3: Generating the training command ...')
    #history = import_bundle_algo_history(result_dir, only_trained=False)
    for task in history:
        current_command = 'python '
        for current_algorithm_name, _ in task.items():
            current_algorithm_folder = os.path.join(result_dir, current_algorithm_name)
            current_train_script = os.path.join(current_algorithm_folder, 'scripts', 'train.py')
            current_command += current_train_script + ' run --config_file='

            all_config_files = []
            for current_config_file in os.listdir(os.path.join(current_algorithm_folder, 'configs')):
                current_config_file = os.path.join(current_algorithm_folder, 'configs', current_config_file)
                all_config_files.append(f"'{current_config_file}'")

            current_command += '"[' + ','.join(all_config_files) + ']"'

            for k, v in train_param.items():
                current_command += f" --{k}={v}"

            with open(f'{current_algorithm_name}.sh', 'w') as f:
                f.write('export CUDA_VISIBLE_DEVICES=your_device_id' + '\n')
                f.write(current_command)

    # step 4: run the command
    print('Step 4: Please set the GPU device id (if necessary) and run the training script ...')

    # step 5: ensemble
    if is_ensemble:
        print('Step 5: Ensembling the result ...')
        history = import_bundle_algo_history(result_dir, only_trained=True)
        builder = AlgoEnsembleBuilder(history, input)
        builder.set_ensemble_method(AlgoEnsembleBestN(n_best=5))
        ensembler = builder.get_ensemble()
        preds = ensembler()

    print('Congrats! May the force be with you ...')
