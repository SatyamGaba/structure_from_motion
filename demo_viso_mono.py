# Edited by Rui Zhu (rzhu@eng.ucsd.edu)
# For CSE152B Spring 2020 HW1
# Apr 15, 2020

import numpy as np
import viso2
import matplotlib.pyplot as plt
from skimage.io import imread

# parameter settings (for an example, please download
img_dir      = '../dataset/sequences/00/image_0/'
gt_dir       = '../dataset/poses/00.txt'
calibFile    = '../dataset/sequences/00/calib.txt'
border       = 50;
gap          = 15;

# Load the camera calibration information 
with open(calibFile) as fid:
    calibLines = fid.readlines()
    calibLines = [calibLine.strip() for calibLine in calibLines]

calibInfo = [float(calibStr) for calibStr in calibLines[0].split(' ')[1:]]
# param = {'f': calibInfo[0], 'cu': calibInfo[2], 'cv': calibInfo[6]}

# Load the ground-truth depth and rotation
with open(gt_dir) as fid:
    gtTr = [[float(TrStr) for TrStr in line.strip().split(' ')] for line in fid.readlines()]
gtTr = np.asarray(gtTr).reshape(-1, 3, 4)

# param['height'] = 1.6
# param['pitch']  = -0.08
# param['match'] = {'pre_step_size': 64}
first_frame  = 0
last_frame   = 300

# init visual odometry
params = viso2.Mono_parameters()
params.calib.f = calibInfo[0]
params.calib.cu = calibInfo[2]
params.calib.cv = calibInfo[6]
params.height = 1.6
params.pitch = -0.08

matcher_params = viso2.Matcher_parameters()


print(matcher_params.pre_step_size)


