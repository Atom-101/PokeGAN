import cv2
import os
from random import shuffle
import glob
import numpy as np
import h5py
import cv2
from imgaug import augmenters as iaa

addresses = glob.glob("/run/media/atom/Seagate Expansion Drive/Pokemon_Fire_Dataset/*.png")

img = []
for i in range(len(addresses)):

    address = addresses[i]
    try:
        im = cv2.imread(address)
        im = cv2.resize(im, (96, 96), interpolation=cv2.INTER_CUBIC)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)        
    except:
        continue
    
    
    img.append(im)
img = np.asarray(img, dtype = np.uint8)
print(img.shape)


lr = iaa.Fliplr(1.0)
rot45 = iaa.Affine(rotate = 45)
_rot45 = iaa.Affine(rotate = -45)
sharp = iaa.Sharpen(lightness = 1.00)
emboss = iaa.Emboss(strength = 0.5)
gray = iaa.Grayscale(alpha = 0.2)
contrast = iaa.ContrastNormalization(1.2)
shear = iaa.Affine(shear = 20)
_shear = iaa.Affine(shear = -20)
transxy = iaa.Affine(translate_percent ={"x": 0.25,"y": 0.25})
trans_xy = iaa.Affine(translate_percent ={"x": -0.25,"y": 0.25})
transx_y = iaa.Affine(translate_percent ={"x": 0.25,"y": -0.25})
trans_x_y = iaa.Affine(translate_percent ={"x": -0.25,"y": -0.25})



#aug_img = np.asarray([])
lr_applied  = lr.augment_images(img)
rot45_applied = rot45.augment_images(img)
_rot45_applied = _rot45.augment_images(img)
sharp_applied = sharp.augment_images(img)
emboss_applied = emboss.augment_images(img)
gray_applied = gray.augment_images(img)
contrast_applied = contrast.augment_images(img)
shear_applied = shear.augment_images(img)
_shear_applied = _shear.augment_images(img)
transxy_applied = transxy.augment_images(img)
trans_xy_applied = trans_xy.augment_images(img)
transx_y_applied = transx_y.augment_images(img)
trans_x_y_applied = trans_x_y.augment_images(img)
transxy_applied_ = transxy.augment_images(lr_applied)
trans_xy_applied_ = trans_xy.augment_images(lr_applied)
transx_y_applied_ = transx_y.augment_images(lr_applied)
trans_x_y_applied_ = trans_x_y.augment_images(lr_applied)

#check if it worked
print(rot45_applied.shape)
print(_rot45_applied.shape)
print(sharp_applied.shape)
print(emboss_applied.shape)


'''
rot45_applied = np.expand_dims(rot45_applied,axis=0)
_rot45_applied = np.expand_dims(_rot45_applied,axis=0)
sharp_applied = np.expand_dims(sharp_applied,axis=0)
emboss_applied = np.expand_dims(emboss_applied,axis=0))
gray_applied = np.expand_dims(gray_applied,axis=0)
contrast_applied = np.expand_dims(contrast_applied,axis=0)
shear_applied = np.expand_dims(shear_applied,axis=0)
_shear_applied = np.expand_dims(_shear_applied,axis=0)
transxy_applied = np.expand_dims(transxy_applied,axis=0)
trans_xy_applied = np.expand_dims(trans_xy_applied,axis=0)
transx_y_applied = np.expand_dims(transx_y_applied,axis=0)
trans_x_y_applied = np.expand_dims(trans_x_y_applied,axis=0)
'''
    




aug_img = np.concatenate((lr_applied,rot45_applied,_rot45_applied,sharp_applied,emboss_applied,
                          gray_applied,contrast_applied,shear_applied,_shear_applied,
                          transxy_applied,trans_xy_applied,transx_y_applied,
                          trans_x_y_applied,transxy_applied_,trans_xy_applied_,transx_y_applied_,
                          trans_x_y_applied_,img))
'''
idx = np.arange(aug_img.shape[0])
np.random.shuffle(idx)
#aug_img = np.random.shuffle(aug_img)
aug_img_shuffle = []
for i in range(aug_img.shape[0]):
        aug_img_shuffle.append(aug_img[idx[i]])
'''
np.random.shuffle(aug_img)        
print(aug_img.shape)

#Some preprocessing to make displaying images easier, later
aug_img = np.asarray(aug_img, dtype = np.float16)
aug_img = aug_img/127.5 -1


with h5py.File('Pokemon_Fire_Dataset_PNG.h5','w') as f:
    f.create_dataset("Pokemon", aug_img.shape, np.float16)
    f["Pokemon"][...] = aug_img
