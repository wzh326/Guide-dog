from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import numpy as np

#需要改的部分
#-------------------
coco = COCO('coco/Annotations/coco_info.json')   #存放json文件的路径
img_dir = 'coco/Images'              #存放原始图片的路径
save_dir = "Mask"                    #存放分割后图片的路径
if_show=False                        #是否在过程中展示图片
#--------------------
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

imgIds = coco.getImgIds() # 获取所有图片的id
print("id:label",coco.loadCats(coco.getCatIds()))

print("Total images:", len(imgIds))
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
        all_mask += mask

    #是否展示
    if if_show:
        plt.imshow(all_mask)
        plt.title(img['file_name'])
        plt.show()

    np.save(os.path.join(save_dir, "mask{}".format(image_id)),all_mask)
