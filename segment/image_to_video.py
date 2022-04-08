import cv2
import glob
import os
from tqdm import trange

fps=30   #帧率
save_path='video.mp4'   #视频文件路径
frames_path='output/result/added_prediction/imgs'  #原始图片路径

f = cv2.VideoWriter_fourcc(*'mp4v')
videoWriter = cv2.VideoWriter(save_path,f,fps,(640,480))
imgs = glob.glob(frames_path + "/*.jpg")
for i in trange(len(imgs)):
    frame = cv2.imread("%s/%d.jpg" % (frames_path,i))
    videoWriter.write(frame)
videoWriter.release()
