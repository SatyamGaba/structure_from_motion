import glob
import cv2
import numpy as np
import os.path as osp
import argparse

# Parse command line arguments.
parser = argparse.ArgumentParser(description='PyTorch SuperPoint Demo.' )
parser.add_argument('--input', type=str, required=True,
        help='Image directory or movie file or "camera" (for webcam).' )
parser.add_argument('--first_frame', type=int, default=0,
        help='Image Id of first frame, default 0' )
parser.add_argument('--last_frame', type=int, default=300,
        help='Image Id of last frame, default value=300' )
opt = parser.parse_args()
print(opt)

for n in range(opt.first_frame, opt.last_frame ):
    imName = osp.join(opt.input, '%06d.png' % n )
    print(imName )
    im = cv2.imread(imName )
    if len(im.shape ) == 3:
        im = np.mean(im, axis=2 )
    im = im.astype(np.uint8 )
    sift = cv2.xfeatures2d.SIFT_create()
    points, features = sift.detectAndCompute(im, None )
    points = [np.array([x.pt[0], x.pt[1] ] ).reshape(1, 2) \
            for x in points ]
    points = np.concatenate(points, axis=0 ).astype(np.float32 )
    features = features.astype(np.float32 ) / 255.0
    pfeatures = np.concatenate([points, features], axis=1 )

    newName = imName.split('/')[-1].replace('.png', '_feature.npy')
    np.save(newName, pfeatures )
