import dlib
import cv2
from imutils import face_utils
import utils

class NoFaceFoundException(Exception):
   """Exception to raise when there was no face"""
   pass

class ImageProcessor:

    def __init__(self, output_dim, padding, detector=None, predictor=None):
        self.output_dim = output_dim
        self.padding = padding

        self.detector = detector if detector else dlib.get_frontal_face_detector()
        self.predictor = predictor if predictor else dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
        
    def process_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    

        # Get all faces
        rects = self.detector(gray, 0)

        # If there are no faces we return a None image
        if len(rects) == 0:
            raise NoFaceFoundException
        
        # Extract the biggest face
        rect = self.check_rects(rects)
        
        # Get position of key points
        shape = self.predictor(gray, rect)
        # For this shape we have:
        # 0, 1 right eye
        # 2, 3 left eye
        # 4 nose
        # for (x, y) in shape:
        #     cv2.circle(image, (x, y), 20, (0, 255, 0), -1)


        # Implementation by dlib
        # Extract face based on key points
        image = dlib.get_face_chip(image, shape, size=self.output_dim, padding=self.padding)

        # Process Images
        # TODO: Adjust colors 
        # img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        # # equalize the histogram of the Y channel
        # img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        # # convert the YUV image back to RGB format
        # image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # Resize to output dimension --> This step might be unnecessary 
        image = cv2.resize(image, (self.output_dim, self.output_dim))
        return image

    def check_rects(self, rects):
        def rect_size(rect):
            return rect.height() + rect.width()

        # Sort rects by size
        rects = sorted(rects, key=rect_size, reverse=True)

        # Return the biggest rectangle
        return rects[0]