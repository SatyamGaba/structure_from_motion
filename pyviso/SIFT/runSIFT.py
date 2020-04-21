import glob
import cv2
import numpy as np
import os.path as osp

root = '../../dataset/sequences/00/image_0/'
imNames = glob.glob(osp.join(root, '*.png') )
imNames = sorted(imNames )
for imName in imNames:
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

    newName = imName.replace('.png', '_sift.npy')
    np.save(newName, pfeatures )

