from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import cv2

#需要改的部分
#-------------------
coco = COCO('coco2/Annotations/coco_info.json')   #存放json文件的路径
img_dir = 'coco2/Images'                    #存放原始图片的路径
save_dir = "PaddleSeg/dataset/labels" #存放分割后图片的路径
if_show=False                              #是否在过程中展示图片,显示会慢一些
#--------------------
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

imgIds = coco.getImgIds() # 获取所有图片的id
print("id:label",coco.loadCats(coco.getCatIds()))

#制作label.txt文件
f=open('PaddleSeg/dataset/label.txt','w',encoding='utf-8')
f.write('background'+'\n')
for i in coco.loadCats(coco.getCatIds()):
    f.write(i['name']+'\n')
f.close()

# print("Total images:", len(imgIds))
for image_id in imgIds:
    #获取图片
    img = coco.imgs[image_id]
    image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
    all_mask=np.zeros([image.shape[0],image.shape[1]],dtype=np.uint8)
    #获取mask
    anns_ids = coco.getAnnIds(imgIds=img['id'],iscrowd=None)        
    anns = coco.loadAnns(anns_ids)
    for i in range(0,len(anns)):
        catid = anns[i]['category_id']   #获取物体类别
        mask = coco.annToMask(anns[i])
        mask[np.where(mask==1)]=catid+1                  
        all_mask[np.where(all_mask!=catid+1)] += mask[np.where(all_mask!=catid+1)]  #同一语义实例不相互叠加
        all_mask[np.where(all_mask>3)]=catid+1                                      #不同语义实例叠加结果后加的实例

    if if_show:
        plt.imshow(all_mask)
        plt.title(img['file_name'])
        plt.show()
    
    cv2.imwrite(os.path.join(save_dir, "{}.png".format(img['file_name'].split('.')[0])),all_mask)
  
#制作剩下的txt文件
img_list=os.listdir('PaddleSeg/dataset/images')
f=open('PaddleSeg/dataset/train.txt','w',encoding='utf-8')
for i in img_list[:int(len(img_list)*0.8)]:
    f.write('images/'+i+' '+'labels/'+i.split('.')[0]+'.png'+'\n')
f.close()

f=open('PaddleSeg/dataset/val.txt','w',encoding='utf-8')
for i in img_list[int(len(img_list)*0.8):int(len(img_list)*0.9)]:
    f.write('images/'+i+' '+'labels/'+i.split('.')[0]+'.png'+'\n')
f.close()

f=open('PaddleSeg/dataset/test.txt','w',encoding='utf-8')
for i in img_list[int(len(img_list)*0.9):len(img_list)]:
    f.write('images/'+i+'\n')
f.close()        
