import numpy as np
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import datasets
from torchvision.datasets.vision import VisionDataset
import PIL


class scut_dataset(torch.utils.data.Dataset):

    def __init__(self, root, transform):
        # super(scut_dataset, self).__init__(root, transform)
        data_dir = root + '/train_test_files/All_labels.txt'
        with open(data_dir, 'r') as f:
            lines = f.readlines()  
            path = []   
            label = [] 
            for line in lines:
                linesplit = line.split('\n')[0].split(' ')
                addr = linesplit[0]
                target = torch.Tensor([float(linesplit[1])])
                path.append(addr)
                if target > 3.0:
                    label.append(1)
                else:
                    label.append(0)
        self.path = path
        self.label = label
        self.transform = transform
        self.root = root


    def __getitem__(self, index):
        sample = PIL.Image.open(os.path.join(self.root, "Images", self.path[index]))
        target = self.label[index]
        if self.transform is not None:
            sample = self.transform(sample)
        return sample, target, index

    def __len__(self):
        return len(self.path)




def main():
    
    # loading data...
    root = '/data2/data/scut_fbp5500/SCUT-FBP5500_v2/'
    
    transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])  
    dataset = scut_dataset(root, transform=transform)
    batch_size = 128
    dataloader_new = torch.utils.data.DataLoader(dataset,
                                              batch_size=min(len(dataset), batch_size),
                                              shuffle=True,
                                              num_workers=1,
                                              drop_last=True)


    for i, (img, target, idx) in enumerate(dataloader_new):
        import pdb
        pdb.set_trace()
        # img = img.unsqueeze(0).cuda(non_blocking=True)
        # target = target.cuda(non_blocking=True)
            

if __name__ == '__main__':
    main()