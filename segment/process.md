## 模型训练流程
### 一.PaddleSeg
clone飞桨的PaddleSeg项目:
<br>
`git clone https://github.com/PaddlePaddle/PaddleSeg.git`
<br>
克隆完成后放在segment路径下
### 二.COCO转data
1.下载第三方库

`pip install pycocotools`

2.将标注好的数据放在segment文件夹下

3.运行make_data.py程序：

`python make_data.py`

会自动生成数据文件夹和需要用到的txt文件

**注意事项：**
百度智能标注只支持实例标注，因此得到的数据集是实例分割数据集。在make_data中需要将同一语义下的不同实例分为一类，进行一个实例分割转语义分割的处理

### 三.修改配置
从PaddleSeg/config下选择要使用的模型。以hardnet为例，打开配置文件hardnet_cityscapes_1024x1024_160k.yml

1.查看基础_base_中使用的yml文件，找到并打开

2.将train_dataset修改为：
```
train_dataset:
  type: Dataset   
  dataset_root: dataset    #存储image和labels的路径
  train_path: dataset/train.txt   #存放tain.txt的路径
  num_classes: 4           #总类别，背景也算一类
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
    num_classes: 4
    transforms:
      - type: Normalize
    mode: val
  ```
## 模型预测流程
### 一.视频转图片
使用PaddleSeg预测时，如果预测文件是视频，那么需要将视频帧转换为图片，才能进行预测。
[PaddleSeg官方预测文档](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.4/docs/predict/predict_cn.md)
<br>
我借鉴了大佬的代码，并在此基础上进行了一定的修改。[原代码地址](https://github.com/Irvingao/paddle-inference-deploy-Lib/blob/main/data_tools/videoSpiltSeg.py)
<br>
执行一下命令即可：
<br>
`python video_to_img.py`
### 二.制作预测目录文件
```
%cd PaddleSeg #进到PaddleSeg文件中
img_list=os.listdir('imgs')
f=open('test.txt','w',encoding='utf-8')
for img in img_list:
    f.write('imgs/'+img+'\n')
f.close()
```
**注意：**执行完该步骤之后，路径一直在PaddleSeg下
### 三.进行预测
```
python predict.py \
       --config configs/hardnet/hardnet_cityscapes_1024x1024_160k.yml \
       --model_path output/best_model/model.pdparams \    #模型参数路径
       --image_path  test.txt \                           #待预测文件目录
       --save_dir output/result \                         #结果文件存储路径
       --custom_color 0 0 0 128 0 128 0 255 0 255 255 0   #不同类别自定义颜色，采用RGB颜色空间，顺序与label.txt一致
```
### 四.分割图片还原为视频
运行脚本将推理出的图片还原为视频
```
python img_to_video.py
```
