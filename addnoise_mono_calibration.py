# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:02:33 2018
@author: clausmichele
"""
import os
import numpy as np
import cv2
import glob
import random

def crop_center(img,cropx,cropy):
  y,x,c = img.shape
  startx = (x - cropx)//2
  starty = (y - cropy)//2    
  return img[starty:starty+cropy, startx:startx+cropx, :]

def crop_centerrandom(img,cropx,cropy):
  y,x,c = img.shape
  startx = (x - cropx)//2
  starty = (y - cropy)//2

  startx = startx + random.randint(-5,5)
  starty = starty + random.randint(-5,5)
  return img[starty:starty+cropy, startx:startx+cropx, :]

def main():
  
  src_dir='./data/'
  save_dir = './data/train'
  src_dir_test='./data/test'
  save_dir_test = './data/test'
  
  filepaths = glob.glob(src_dir + '/*.png')
  filepaths_test = glob.glob(src_dir_test + '/*.png')
  def sortKeyFunc(s):
    return int(os.path.basename(s)[:-4])
    
  filepaths_test.sort(key=sortKeyFunc)
  filepaths.sort(key=sortKeyFunc)
  
  
  print("[*] Reading train files...")  
  
  if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        #os.mkdir(save_dir_test)
        os.mkdir('./data/train/noisy')
        os.mkdir('./data/train/original')
        os.mkdir('./data/test/noisy')
        os.mkdir('./data/test/original')        

  print("[*] Applying noise...")

  sig = np.linspace(0,50,len(filepaths))
  np.random.shuffle(sig)
  sig_test = np.linspace(0,50,len(filepaths_test))
  np.random.shuffle(sig_test)
  imgcal = cv2.imread("./data/calibration/cali.png")
  variance1 = np.asarray( imgcal )

  for i in xrange(len(filepaths)):
        image = cv2.imread(filepaths[i])
        image = cv2.resize(image,(180,180), interpolation = cv2.INTER_CUBIC)
        row,col,ch = image.shape
        mean = 0
        sigma = sig[i]
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        variance = crop_centerrandom(variance1,180,180)
        variance = variance.astype('uint16')
        noisy = image + gauss + variance
        noisy = np.clip(noisy, 0, 255)
        noisy = noisy.astype('uint8')
        noisy = cv2.cvtColor(noisy,cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(save_dir, "noisy/%04d.png" %i), noisy)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(save_dir, "original/%04d.png" %i), image)
        
  for i in xrange(len(filepaths_test)):
        image = cv2.imread(filepaths_test[i])
        image = cv2.resize(image,(180,180), interpolation = cv2.INTER_CUBIC)
        row,col,ch = image.shape
        mean = 0
        sigma = sig[i]
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        variance = crop_centerrandom(variance1,180,180)
        variance = variance.astype('uint16')
        noisy = image + gauss + variance
        noisy = np.clip(noisy, 0, 255)
        noisy = noisy.astype('uint8')
        noisy = cv2.cvtColor(noisy,cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(save_dir_test, "noisy/%d.png" %i), noisy)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        cv2.imwrite(os.path.join(save_dir_test, "original/%d.png" %i), image)
  
  print("[*] Noisy and original images saved")

if __name__ == "__main__":
  main()