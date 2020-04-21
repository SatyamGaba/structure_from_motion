import os
import glob
import argparse
import os.path as osp


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


for n in range(opt.first_frame, opt.last_frame):
    imgName1 = osp.join(opt.input, '%06d.png' % n )
    imgName2 = osp.join(opt.input, '%06d.png' % (n+1 ) )

    print('%d/%d/%d: %s' % (opt.first_frame, n, opt.last_frame, imgName1 ) )
    cmd = 'python run.py --first %s --second %s --model %s' % \
            (imgName1, imgName2, 'kitti-final')
    os.system(cmd )
