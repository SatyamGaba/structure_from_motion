#!/usr/bin/env python

import viso2
from skimage.io import imread
import pathlib as pl
import sys

def filter_by_name(name, imgs):
    return sorted(filter(lambda x: str(x).find(name) >= 0, imgs))

LEFT="image_00"
RIGHT="image_01"

if len(sys.argv) < 2:
    print 'Usage: ./demo.py path/to/2011_09_26_drive_0106_sync'
    sys.exit(0)

base_dir = pl.Path(sys.argv[1])
assert(base_dir.exists() and base_dir.is_dir())

# set the most relevant parameters
params = viso2.Stereo_parameters()
params.calib.f  = 721.5377
params.calib.cu = 609.5593
params.calib.cv = 172.854
params.base     = 0.537

# initialize visual odometry 
viso = viso2.VisualOdometryStereo(params)

all_images = [f for f in base_dir.rglob("*.png")]
left_gray = filter_by_name(LEFT, all_images)
right_gray = filter_by_name(RIGHT, all_images)

N = len(left_gray)
assert(len(left_gray) == len(right_gray))

pose = viso2.Matrix_eye(4)
for i in xrange(N):
    # load the images
    left_img = imread(str(left_gray[i]))
    right_img = imread(str(right_gray[i]))
    assert(len(left_img.shape) == 2) # should be grayscale
    
    print "Processing: Frame:", i

    # compute visual odometry
    if viso.process_frame(left_img, right_img):
        est_motion = viso2.Matrix_inv(viso.getMotion())
        pose = pose * est_motion

        num_matches = viso.getNumberOfMatches()
        num_inliers = viso.getNumberOfInliers()
        print 'Matches:', num_matches, "Inliers:", 100*num_inliers/num_matches, '%, Current pose:'
        print pose
    else:
        print '.... failed!'

print 'Demo complete! Exiting...'
        
