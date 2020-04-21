#!/usr/bin/env python

import viso2
import numpy as np
import matplotlib.pyplot as plt
#from mayavi import mlab
from skimage.io import imread
import pathlib as pl
import sys

def filter_by_name(name, imgs):
    return sorted(filter(lambda x: str(x).find(name) >= 0, imgs))

LEFT="image_00"
RIGHT="image_01"

if len(sys.argv) < 2:
    print('Usage: ./demo.py /data/kitti/raw/2011_09_26/2011_09_26_drive_0106_sync')
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
# viso = viso2.VisualOdometryStereo(params)
# recon = viso2.Reconstruction()
# recon.setCalibration(params.calib.f, params.calib.cu, params.calib.cv)
matcher_params = viso2.Matcher_parameters()

matcher_params.f = 721.5377
matcher_params.cu = 609.5593
matcher_params.cv = 172.854
matcher_params.base = 0.537
matcher_params.nms_n = 13
matcher_params.nms_tau = 50
matcher_params.match_binsize = 50 
matcher_params.match_radius = 200
matcher_params.match_disp_tolerance = 2
matcher_params.outlier_flow_tolerance = 10
matcher_params.outlier_disp_tolerance = 10
matcher_params.multi_stage = 1
matcher_params.half_resolution = 0
matcher_params.refinement = 1



matcher = viso2.Matcher(matcher_params)
matcher.setIntrinsics(params.calib.f, params.calib.cu, params.calib.cv, params.base)

all_images = [f for f in base_dir.rglob("*.png")]
left_gray = filter_by_name(LEFT, all_images)
right_gray = filter_by_name(RIGHT, all_images)

N = len(left_gray)
assert(len(left_gray) == len(right_gray))

pose = viso2.Matrix_eye(4)
for i in range(N):
    # load the images
    left_img = imread(str(left_gray[i]))
    right_img = imread(str(right_gray[i]))
    assert(len(left_img.shape) == 2) # should be grayscale
    
    print("Processing: Frame:", i)

    matcher.pushBack(left_img, right_img)
    
    if i > 0:
        matcher.matchFeatures(2)
        matches = matcher.getMatches()
        matches_mat = np.empty([8, matches.size()])
        print(matches.size())

        for i,m in enumerate(matches):
            if i == 342:
                print("{}".format([m.u1p, m.v1p]))
                matches_mat[:, i] = (m.u1p, m.v1p, m.u2p, m.v2p,m.u1c,m.v1c,m.u2c,m.v2c)
        

    # if viso.process_frame(left_img, right_img):
    #     motion = viso.getMotion()
    #     est_motion = viso2.Matrix_inv(motion)
    #     pose = pose * est_motion

    #     num_matches = viso.getNumberOfMatches()
    #     num_inliers = viso.getNumberOfInliers()
    #     print('Matches:', num_matches, "Inliers:", 100*num_inliers/num_matches, '%, Current pose:')
    #     print(pose)

    #     matches = viso.getMatches()
    #     matches_mat = np.empty([2, matches.size()])
        
    #     matches_mat

    #     assert(matches.size() == num_matches)
    #     recon.update(matches, motion, 0)
    # else:
    #     print('.... failed!')

# points = recon.getPoints()
# print("Reconstructed", points.size(), "points...")

# pts = np.empty((points.size(),3))
# for i,p in enumerate(points):
#     pts[i,:] = (p.x, p.y, p.z)

#mlab.figure()
#mlab.points3d(pts[:,0], pts[:,1], pts[:,2], colormap='copper')
#mlab.show()

print('Demo complete! Exiting...')
        
