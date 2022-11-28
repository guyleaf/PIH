#!/bin/bash

# Network hyperparameters
device=6
lr=2e-5
lrd=2e-5
batch_size=8
date=202206161_a100_4
inputdim=3
reconweight=10
name=iharmony_compositegan_7layerD_unet_test_with_mask_no_mask_input_${inputdim}_reconloss_$reconweight

model_name=exp_${date}_batch_size_$((batch_size))_lr_${lr}_${name}_device_${device}

# Set folder names
dir_data=/mnt/localssd/Ihd_real_composite/train/
dir_log=/home/kewang/sensei-fs-symlink/users/kewang/projects/PIH/PIH_ResNet/results/$model_name



CUDA_VISIBLE_DEVICES=$device python PIH_train_compositeGAN.py --datadir $dir_data \
                       -g 0 \
                       --logdir $dir_log \
                       --bs $batch_size \
                       --lr $lr \
                       --lrd $lrd \
                       --force_train_from_scratch \
                       --tempdir \
                       $model_name \
                       --workers 16 \
                       --unet \
                       --inputdim $inputdim \
                       --reconloss \
                       --reconweight $reconweight \

