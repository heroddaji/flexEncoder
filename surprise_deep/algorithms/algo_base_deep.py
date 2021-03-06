import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim.lr_scheduler import MultiStepLR


class AlgoBaseDeep(nn.Module):
    def __init__(self):
        super().__init__()

    def activation(self, input, kind):
        if kind == 'selu':
            return F.selu(input)
        elif kind == 'relu':
            return F.relu(input)
        elif kind == 'relu6':
            return F.relu6(input)
        elif kind == 'sigmoid':
            return F.sigmoid(input)
        elif kind == 'tanh':
            return F.tanh(input)
        elif kind == 'elu':
            return F.elu(input)
        elif kind == 'lrelu':
            return F.leaky_relu(input)
        elif kind == 'swish':
            return input * F.sigmoid(input)
        elif kind == 'none':
            return input
        else:
            raise ValueError('Unknown activation function')

    def optimizer(self, option):
        # todo: check the momentum value, can it be in the option?
        optimizer = None
        kind = option.mp_optimizer
        if kind == 'adam':
            optimizer = optim.Adam(self.parameters(),
                                   lr=option.mp_learning_rate,
                                   weight_decay=option.mp_weight_decay)
        elif kind == "adagrad":
            optimizer = optim.Adagrad(self.parameters(),
                                      lr=option.mp_learning_rate,
                                      weight_decay=option.mp_weight_decay)
        elif kind == 'sgd':
            optimizer = optim.SGD(self.parameters(),
                                  lr=option.mp_learning_rate,
                                  momentum=0.9,
                                  weight_decay=option.mp_weight_decay)
        elif kind == "rmsprop":
            optimizer = optim.RMSprop(self.parameters(),
                                      lr=option.mp_learning_rate,
                                      momentum=0.9,
                                      weight_decay=option.mp_weight_decay)
        else:
            raise ValueError('Unknown optimizer kind')

        return optimizer

    def MMSEloss(self, inputs, targets, mask_value=0.0, size_average = False):
        mask = targets != mask_value
        num_rating = torch.sum(mask.float())
        size_average = size_average
        criterion = nn.MSELoss(size_average=size_average)

        if size_average:
            num_rating = 1

        loss = criterion(inputs * mask.float(), targets)
        loss = loss / num_rating
        return loss

