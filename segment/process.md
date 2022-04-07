## 模型训练流程
### 一.PaddleSeg
clone飞桨的PaddleSeg项目:
<br>
`git clone https://github.com/PaddlePaddle/PaddleSeg.git`
<br>
克隆完成后放在segment路径下
### COCO转data
1.下载第三方库

`pip install pycocotools`

2.将标注好的数据放在segment文件夹下

3.运行make_data.py程序：

`python make_data.py`

会自动生成数据文件夹和需要用到的txt文件

**注意事项：**
百度智能标注只支持实例标注，因此得到的数据集是实例分割数据集。在make_data中需要将同一语义下的不同实例分为一类，进行一个实例分割转语义分割的处理

### 修改配置
从PaddleSeg/config下选择要使用的模型。以hardnet为例，打开配置文件hardnet_cityscapes_1024x1024_160k.yml

1.查看基础_base_中使用的yml文件，找到并打开

2.将train_dataset修改为：
```
train_dataset:
  type: Dataset   
  dataset_root: dataset    #存储image和labels的路径
  train_path: dataset/train.txt   #存放tain.txt的路径
  num_classes: 3           #总类别，背景也算一类
  transforms:
    - type: ResizeStepScaling
      min_scale_factor: 0.5
      max_scale_factor: 2.0
      scale_step_size: 0.25
    - type: RandomPaddingCrop
      crop_size: [480, 640]
    - type: RandomHorizontalFlip
    - type: RandomDistort
      brightness_range: 0.4
      contrast_range: 0.4
      saturation_range: 0.4
    - type: Normalize
  mode: train
  ```
  3.将val_dataset修改为：
  ```
  val_dataset:
    type: Dataset
    dataset_root: dataset
    val_path: dataset/val.txt
    num_classes: 3
    transforms:
      - type: Normalize
    mode: val
  ```
