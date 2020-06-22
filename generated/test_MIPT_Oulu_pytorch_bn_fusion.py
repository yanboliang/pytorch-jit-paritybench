import sys
_module = sys.modules[__name__]
del sys
bn_fusion = _module
test_convert_inference = _module
utils = _module

from _paritybench_helpers import _mock_config
from unittest.mock import mock_open, MagicMock
from torch.autograd import Function
from torch.nn import Module
open = mock_open()
logging = sys = argparse = MagicMock()
ArgumentParser = argparse.ArgumentParser
_global_config = args = argv = cfg = config = params = _mock_config()
argparse.ArgumentParser.return_value.parse_args.return_value = _global_config
sys.argv = _global_config
__version__ = '1.0.0'


import torch


import torch.nn as nn


from torch.nn import functional as F


import numpy as np


import time


class Net(nn.Module):

    def __init__(self, features, classifer):
        super(Net, self).__init__()
        self.features = features
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = classifer

    def forward(self, x):
        out = self.features(x)
        out = self.pool(out).view(x.size(0), -1)
        return self.classifier(out)


class BasicResnetBlock(nn.Module):
    expansion = 1

    def __init__(self, source_block):
        super(BasicResnetBlock, self).__init__()
        self.block1 = nn.Sequential(source_block.conv1, source_block.bn1)
        self.block2 = nn.Sequential(source_block.conv2, source_block.bn2)
        self.downsample = source_block.downsample
        self.stride = source_block.stride
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        residual = x
        out = self.relu(self.block1(x))
        out = self.block2(out)
        if self.downsample is not None:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out


class BottleneckResnetBlock(nn.Module):
    expansion = 4

    def __init__(self, source_block, se=False):
        super(BottleneckResnetBlock, self).__init__()
        self.block1 = nn.Sequential(source_block.conv1, source_block.bn1)
        self.block2 = nn.Sequential(source_block.conv2, source_block.bn2)
        self.block3 = nn.Sequential(source_block.conv3, source_block.bn3)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = source_block.downsample
        self.stride = source_block.stride
        if se:
            self.se_module = source_block.se_module
        else:
            self.se_module = None

    def forward(self, x):
        residual = x
        out = self.relu(self.block1(x))
        out = self.relu(self.block2(out))
        out = self.block3(out)
        if self.downsample is not None:
            residual = self.downsample(x)
        if self.se_module is not None:
            out += self.se_module(out)
        out += residual
        out = self.relu(out)
        return out


import torch
from _paritybench_helpers import _mock_config, _mock_layer, _paritybench_base, _fails_compile

class Test_MIPT_Oulu_pytorch_bn_fusion(_paritybench_base):
    pass
    def test_000(self):
        self._check(Net(*[], **{'features': ReLU(), 'classifer': ReLU()}), [torch.rand([4, 4, 4, 4])], {})

