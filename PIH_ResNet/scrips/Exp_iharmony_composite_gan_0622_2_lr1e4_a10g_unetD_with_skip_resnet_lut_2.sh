#!/bin/bash

# Network hyperparameters
device=2
lr=1e-4
lrd=1e-4
batch_size=8
date=2022062_a10g_2_unetD_no_skip_resnet_lut
inputdim=6
reconweight=None
training_ratio=1
name=iharmony_compositegan_${inputdim}_reconloss_${reconweight}_ration_${training_ratio}_nomask_noskip

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
                       --workers 8 \
                       --inputdim $inputdim \
                       --trainingratio ${training_ratio} \
                       --unetd \
                       --lut \


