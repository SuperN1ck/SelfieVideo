import os
import cv2
from tqdm import tqdm

from image_processing import ImageProcessor, NoFaceFoundException

# TODO Get config by arparse?
folder_path = "/data/Pictures/Selfies_Everyday_Jun_Sep_2019/"
output_dim = 1000
padding = 1.2
video_name = 'video_{}_fps.avi'
fps_options = [1, 5, 10, 15, 25, 30, 59, 60]
file_type = ".jpg"

image_processor = ImageProcessor(output_dim, padding)

# Get all files in the folder sorted by time and filtered by file_type
file_names = sorted(os.listdir(folder_path), 
    key=lambda file_name: os.path.getmtime(os.path.join(folder_path, file_name)))
image_names = [img for img in file_names if img.endswith(file_type)]

video_writters = []

# Prepare all video writers
for fps in fps_options:
    video_writters.append(cv2.VideoWriter(video_name.format(fps), 0, fps, (output_dim, output_dim)))
    
for image_name in tqdm(image_names):
    image = cv2.imread(os.path.join(folder_path, image_name))

    try:
        image_processor.process_image(image)
    except NoFaceFoundException:
        continue

    for video_writter in video_writters:
        video_writter.write(image)
        
for video_writter in video_writters:
    video_writter.release()

cv2.destroyAllWindows()

# Code for displaying a single image
# image_name = "IMG_20190607_020523.jpg"
# image_name = "IMG_20190715_162030.jpg"
# image_name = "IMG_20190706_140033_1.jpg"
# image = cv2.imread(os.path.join(folder_path, image_name))

# image = image_processor.process_image(image)

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow("image", image)
# cv2.resizeWindow('image', 600,600)
# cv2.waitKey(0)

# cv2.destroyAllWindows()