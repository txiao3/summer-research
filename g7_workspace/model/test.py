import torch
from torchvision import models

# Resnet = models.resnet18(pretrained=True)
# image = torch.zeros(1, 3, 224, 224)
# print(Resnet.conv1(image).shape)
# image = torch.zeros(1, 3, 640, 480)
# conv = torch.nn.Conv2d(3, 64, (20, 15), stride=(5, 4), padding=(6, 4), dilation=(5,3))
# out = conv(image)
# print(out.shape)

# import torch.nn.functional as F
# loss_kl = torch.nn.KLDivLoss(reduction='sum')
# loss_ce=torch.nn.CrossEntropyLoss()
# batch_size = 5
# input=torch.randn(batch_size, 10)
# target=torch.randn(batch_size, 10)
# log_probs1 = F.log_softmax(input, 1)
# probs2 = F.softmax(target, 1)
# print(loss_kl(log_probs1, probs2) / batch_size)
# a=torch.empty(3, dtype=torch.long).random_(5)
# print(loss_ce(input,target))

import misc
a=[0,1,2]
print(misc.one_hot_embedding(a,3))