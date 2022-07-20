#!/bin/bash

# Network hyperparameters
device=0
lr=3e-5
lrd=3e-5
batch_size=6
date=202206161_a10g_9_unetD_withoutmask
inputdim=3
reconweight=None
training_ratio=0.2
name=iharmony_compositegan_7layerD_unet_test_with_mask_no_mask_input_${inputdim}_reconloss_${reconweight}_ration_${training_ratio}_patchGAN_3layer

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
                       --workers 6 \
                       --unet \
                       --inputdim $inputdim \
                       --trainingratio ${training_ratio} \
                       --unetd \


