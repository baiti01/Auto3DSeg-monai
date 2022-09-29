# Introduction
This code is used to automatically generate the command for model training.

See more details from the official [tutorial](https://github.com/Project-MONAI/tutorials/tree/main/auto3dseg).

# Made the following changes before using it
- The default train_params is set as {}, instead of NONE. Otherwise the code will raise the error "undefined parameteres" at [here](https://github.com/Project-MONAI/MONAI/blob/52df2baf347809008dbf26dfa6a2f716eb12ae68/monai/apps/auto3dseg/bundle_gen.py#L158).
- Add sys.path.insert(0, os.path.join(algo_path, "algorithm_templates")) to line 328 at [here](https://github.com/Project-MONAI/MONAI/blob/52df2baf347809008dbf26dfa6a2f716eb12ae68/monai/apps/auto3dseg/bundle_gen.py#L328).
- Set Resample=False [here](https://github.com/baiti01/Auto3DSeg-monai/blob/fa800c72296cb7e37a13758cdc2c74a9f1734988/assets/algorithm_templates/segresnet/scripts/algo.py#L188) for segresnet to avoid the out-of-memory issue. (This is NOT a bug. After modification, the default resolution is not (1, 1, 1) anymore.)
- Add extra code [here](https://github.com/baiti01/Auto3DSeg-monai/blob/fa800c72296cb7e37a13758cdc2c74a9f1734988/assets/algorithm_templates/segresnet/scripts/algo.py#L300) to convert all the list-based transform to REAL transform objects
- Adapt to Windows operation system [here](https://github.com/baiti01/Auto3DSeg-monai/blob/fa800c72296cb7e37a13758cdc2c74a9f1734988/assets/algorithm_templates/segresnet/scripts/train.py#L45)

# LOGS
- Add a small segresnet to assets where the initial_channel is set to 16, the batch size is set as 1.

# Usage
1. Setup the parameters in main.py adapted to your own dataset.
2. Automatically analyze the dataset, generate the model(s), and create the command used for model training by running:
```console
python main.py
```
3. Setup your CUDA device ID, and train the model by running (FOR EXAMPLE):
```console
bash segresnet_small_0.sh
```
