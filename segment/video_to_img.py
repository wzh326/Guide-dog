#视频转图片
import cv2
import time
import os

img_id = 0
total_img = 0
n=0
single_video=True

def check_video_dir(video_dir):
    if os.path.isdir(video_dir):
        folder = os.listdir(video_dir)
        print(folder)
        video_id = 0
        video_dir_dict = {}
        if folder != []:
            video_id_list =[]
            for i in folder:
                if len(i.split(".")) <= 1: # 文件夹跳过
                    continue
                if i.split(".")[1] != 'avi': # 不是视频文件跳过
                    continue
                video_id = int(i.split(".")[0])
                video_id_list.append(video_id)
                images_save_dir = os.path.join(video_dir, 'images{}'.format(str(video_id))) # 每个视频创建一个文件夹
                every_video_dir = os.path.join(video_dir, i)

                if os.path.isdir(images_save_dir):
                    try:
                        os.rmdir(images_save_dir)
                        os.mkdir(images_save_dir)
                    except OSError:
                        continue
                else:
                    os.mkdir(images_save_dir)
                video_dir_dict[every_video_dir] = images_save_dir
            video_id = max(video_id_list)
            print("There are already {} videos saved.".format(video_id+1))
            return video_dir_dict
    else:
        print("There is no video.")
        return {}

def save_img(img, save_dir):
    global img_id,total_img,n
    #if n%10==0:
    if single_video:
        cv2.imwrite(f'{save_dir}/{img_id}.jpg',img)
    else:    
        dataset_idx = save_dir[-1]
        cv2.imwrite(os.path.join(save_dir, (f'{dataset_idx}_{img_id}.jpg')), img)
    #print("total image:" + str(total_img), f", {img_id} images in {save_dir}")
    img_id+=1
    total_img+=1
    #n+=1


if __name__ == '__main__':
    if single_video:
        video_path='video.avi' # 视频地址
        save_dir='PaddleSeg/imgs'  #保存图片的路径
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)        
        img_id = 0
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, image = cap.read()
            if ret:
                save_img(image,save_dir)
                continue
            break        
    else:
        video_dir = "Dataset_segmentation" # write your videos dir        
        video_dir_dict = check_video_dir(video_dir)  #字典
        print(video_dir_dict)
        key_list = list(video_dir_dict.keys())
        print(key_list)
        if len(key_list) > 0:
            for video in key_list:
                img_id = 0
                cap = cv2.VideoCapture(video)
                while True:
                    ret, image = cap.read()
                    if ret:
                        save_img(image, video_dir_dict[video])
                        continue
                    break
                   
