import os
import glob
import argparse
import os.path as osp


# Parse command line arguments.
parser = argparse.ArgumentParser(description='PyTorch SuperPoint Demo.')
parser.add_argument('--input', type=str, default='../../dataset/sequences/00/image_0/',
        help='Image directory or movie file or "camera" (for webcam).')
parser.add_argument('--img_format', type=str, default='.png',
        help='Format of images (default: .png).')
parser.add_argument('--first_frame', type=int, default=0,
        help='Image Id of first frame, default 0' )
parser.add_argument('--last_frame', type=int, default=300,
        help='Image Id of last frame, default value=1000')
parser.add_argument('--cuda', action='store_true',
        help='Use cuda GPU to speed up network processing speed (default: False)')
opt = parser.parse_args()
print(opt)


for n in range(opt.first_frame, opt.last_frame):
    imgName1 = osp.join(opt.input, '%06d%s' % (n, opt.img_format) )
    imgName2 = osp.join(opt.input, '%06d%s' % (n+1, opt.img_format) )

    print('%d/%d/%d: %s' % (opt.first_frame, n, opt.last_frame, imgName1 ) )
    cmd = 'python run.py --first %s --second %s --model %s' % \
            (imgName1, imgName2, 'kitti-final')
    os.system(cmd )
