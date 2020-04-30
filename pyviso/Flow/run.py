#!/usr/bin/env python

import torch

import getopt
import math
import numpy
import os
import PIL
import PIL.Image
import sys
import numpy as np

##########################################################

assert(int(str('').join(torch.__version__.split('.')[0:3])) >= 41) # requires at least pytorch version 0.4.1

torch.set_grad_enabled(False) # make sure to not compute gradients for computational performance

if torch.cuda.is_available():
    torch.cuda.device(1) # change this if you have a multiple graphics cards and you want to utilize them
    torch.backends.cudnn.enabled = True # make sure to use cudnn for computational performance

##########################################################

arguments_strModel = 'sintel-final'
arguments_strFirst = './images/first.png'
arguments_strSecond = './images/second.png'
arguments_strOut = './out.flo'

for strOption, strArgument in getopt.getopt(sys.argv[1:], '', [ strParameter[2:] + '=' for strParameter in sys.argv[1::2] ])[0]:
    if strOption == '--model' and strArgument != '': arguments_strModel = strArgument # which model to use, see below
    if strOption == '--first' and strArgument != '': arguments_strFirst = strArgument # path to the first frame
    if strOption == '--second' and strArgument != '': arguments_strSecond = strArgument # path to the second frame
    if strOption == '--out' and strArgument != '': arguments_strOut = strArgument # path to where the output should be stored
# end

##########################################################

Backward_tensorGrid = {}

def Backward(tensorInput, tensorFlow):
    if str(tensorFlow.size()) not in Backward_tensorGrid:
        tensorHorizontal = torch.linspace(-1.0, 1.0, tensorFlow.size(3)).view(1, 1, 1, tensorFlow.size(3)).expand(tensorFlow.size(0), -1, tensorFlow.size(2), -1)
        tensorVertical = torch.linspace(-1.0, 1.0, tensorFlow.size(2)).view(1, 1, tensorFlow.size(2), 1).expand(tensorFlow.size(0), -1, -1, tensorFlow.size(3))
        if torch.cuda.is_available():
            Backward_tensorGrid[str(tensorFlow.size())] = torch.cat([ tensorHorizontal, tensorVertical ], 1).cuda()
        else:
            Backward_tensorGrid[str(tensorFlow.size())] = torch.cat([ tensorHorizontal, tensorVertical ], 1)
    tensorFlow = torch.cat([ tensorFlow[:, 0:1, :, :] / ((tensorInput.size(3) - 1.0) / 2.0), tensorFlow[:, 1:2, :, :] / ((tensorInput.size(2) - 1.0) / 2.0) ], 1)
    return torch.nn.functional.grid_sample(input=tensorInput, grid=(Backward_tensorGrid[str(tensorFlow.size())] + tensorFlow).permute(0, 2, 3, 1), mode='bilinear', padding_mode='border')
# end

##########################################################

class Network(torch.nn.Module):
    def __init__(self):
        super(Network, self).__init__()

        class Preprocess(torch.nn.Module):
            def __init__(self):
                super(Preprocess, self).__init__()

            def forward(self, tensorInput):
                tensorBlue = (tensorInput[:, 0:1, :, :] - 0.406) / 0.225
                tensorGreen = (tensorInput[:, 1:2, :, :] - 0.456) / 0.224
                tensorRed = (tensorInput[:, 2:3, :, :] - 0.485) / 0.229

                return torch.cat([ tensorRed, tensorGreen, tensorBlue ], 1)

        class Basic(torch.nn.Module):
            def __init__(self, intLevel):
                super(Basic, self).__init__()

                self.moduleBasic = torch.nn.Sequential(
                    torch.nn.Conv2d(in_channels=8, out_channels=32, kernel_size=7, stride=1, padding=3),
                    torch.nn.ReLU(inplace=False),
                    torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=7, stride=1, padding=3),
                    torch.nn.ReLU(inplace=False),
                    torch.nn.Conv2d(in_channels=64, out_channels=32, kernel_size=7, stride=1, padding=3),
                    torch.nn.ReLU(inplace=False),
                    torch.nn.Conv2d(in_channels=32, out_channels=16, kernel_size=7, stride=1, padding=3),
                    torch.nn.ReLU(inplace=False),
                    torch.nn.Conv2d(in_channels=16, out_channels=2, kernel_size=7, stride=1, padding=3)
                )

            def forward(self, tensorInput):
                return self.moduleBasic(tensorInput)

        self.modulePreprocess = Preprocess()

        self.moduleBasic = torch.nn.ModuleList([ Basic(intLevel) for intLevel in range(6) ])

        self.load_state_dict(torch.load('./network-' + arguments_strModel + '.pytorch'))

    def forward(self, tensorFirst, tensorSecond):
        tensorFlow = []

        tensorFirst = [ self.modulePreprocess(tensorFirst) ]
        tensorSecond = [ self.modulePreprocess(tensorSecond) ]

        for intLevel in range(5):
            if tensorFirst[0].size(2) > 32 or tensorFirst[0].size(3) > 32:
                tensorFirst.insert(0, torch.nn.functional.avg_pool2d(input=tensorFirst[0], kernel_size=2, stride=2))
                tensorSecond.insert(0, torch.nn.functional.avg_pool2d(input=tensorSecond[0], kernel_size=2, stride=2))
        tensorFlow = tensorFirst[0].new_zeros([ tensorFirst[0].size(0), 2, int(math.floor(tensorFirst[0].size(2) / 2.0)), int(math.floor(tensorFirst[0].size(3) / 2.0)) ])

        for intLevel in range(len(tensorFirst)):
            tensorUpsampled = torch.nn.functional.interpolate(input=tensorFlow, scale_factor=2, mode='bilinear', align_corners=True) * 2.0

            if tensorUpsampled.size(2) != tensorFirst[intLevel].size(2): tensorUpsampled = torch.nn.functional.pad(input=tensorUpsampled, pad=[ 0, 0, 0, 1 ], mode='replicate')
            if tensorUpsampled.size(3) != tensorFirst[intLevel].size(3): tensorUpsampled = torch.nn.functional.pad(input=tensorUpsampled, pad=[ 0, 1, 0, 0 ], mode='replicate')

            tensorFlow = self.moduleBasic[intLevel](torch.cat([ tensorFirst[intLevel], Backward(tensorInput=tensorSecond[intLevel], tensorFlow=tensorUpsampled), tensorUpsampled ], 1)) + tensorUpsampled
        return tensorFlow

if torch.cuda.is_available():
    moduleNetwork = Network().cuda().eval()
else:
    moduleNetwork = Network().eval()

##########################################################

def estimate(tensorFirst, tensorSecond):
    assert(tensorFirst.size(1) == tensorSecond.size(1))
    assert(tensorFirst.size(2) == tensorSecond.size(2))

    intWidth = tensorFirst.size(2)
    intHeight = tensorFirst.size(1)

    #assert(intWidth == 1024) # remember that there is no guarantee for correctness, comment this line out if you acknowledge this and want to continue
    #assert(intHeight == 416) # remember that there is no guarantee for correctness, comment this line out if you acknowledge this and want to continue

    if torch.cuda.is_available():
        tensorPreprocessedFirst = tensorFirst.cuda().view(1, 3, intHeight, intWidth)
        tensorPreprocessedSecond = tensorSecond.cuda().view(1, 3, intHeight, intWidth)
    else:
        tensorPreprocessedFirst = tensorFirst.view(1, 3, intHeight, intWidth)
        tensorPreprocessedSecond = tensorSecond.view(1, 3, intHeight, intWidth)


    intPreprocessedWidth = int(math.floor(math.ceil(intWidth / 32.0) * 32.0) )
    intPreprocessedHeight = int(math.floor(math.ceil(intHeight / 32.0) * 32.0) )

    tensorPreprocessedFirst = torch.nn.functional.interpolate(input=tensorPreprocessedFirst, size=(intPreprocessedHeight, intPreprocessedWidth), mode='bilinear', align_corners=False)
    tensorPreprocessedSecond = torch.nn.functional.interpolate(input=tensorPreprocessedSecond, size=(intPreprocessedHeight, intPreprocessedWidth), mode='bilinear', align_corners=False)

    tensorFlow = torch.nn.functional.interpolate(input=moduleNetwork(tensorPreprocessedFirst, tensorPreprocessedSecond), size=(intHeight, intWidth), mode='bilinear', align_corners=False)

    tensorFlow[:, 0, :, :] *= float(intWidth) / float(intPreprocessedWidth)
    tensorFlow[:, 1, :, :] *= float(intHeight) / float(intPreprocessedHeight)

    if torch.cuda.is_available():
        return tensorFlow[0, :, :, :].cuda()
    else:
        return tensorFlow[0, :, :, :]
# end

##########################################################

if __name__ == '__main__':
    tensorFirst = torch.FloatTensor(numpy.array(PIL.Image.open(arguments_strFirst) )[:, :, numpy.newaxis].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0))
    tensorSecond = torch.FloatTensor(numpy.array(PIL.Image.open(arguments_strSecond))[:, :, numpy.newaxis].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0))

    if tensorFirst.size(0) == 1:
        tensorFirst = torch.cat([tensorFirst, tensorFirst, tensorFirst], dim=0)
        tensorSecond = torch.cat([tensorSecond, tensorSecond, tensorSecond], dim=0)

    tensorOutput = estimate(tensorFirst, tensorSecond)
    numpyOutput = tensorOutput.cpu().numpy().transpose(1, 2, 0).astype(numpy.float32 )

    flowName = arguments_strSecond.split('/')[-1].replace('.png', '_flow.npy')
    np.save(flowName, numpyOutput )
