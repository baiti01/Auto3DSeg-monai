# Auto3DSeg-monai
This script is used to automatically generate the command for model training

# Fixed several bugs
- The default train_params is set as {}, instead of NONE. Otherwise the code will raise the error "undefined parameteres" at [here](https://github.com/Project-MONAI/MONAI/blob/52df2baf347809008dbf26dfa6a2f716eb12ae68/monai/apps/auto3dseg/bundle_gen.py#L158).
- Add sys.path.insert(0, os.path.join(algo_path, "algorithm_templates")) to line 328 at [here](https://github.com/Project-MONAI/MONAI/blob/52df2baf347809008dbf26dfa6a2f716eb12ae68/monai/apps/auto3dseg/bundle_gen.py#L328).
- Set Resample=False (here) for segresnet to avoid the out-of-memory issue. (This is NOT a bug. After modification, the default resolution is not (1, 1, 1) anymore.)
- Add the following code block to line 300 (here) to convert all the list-based transform to REAL transform objects
