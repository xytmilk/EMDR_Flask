import cv2 

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Video resoulation 
        VIDEO_WIDTH = 1080
        VIDEO_HEIGHT = 1440
    
    def __del__(self):
        self.video.release()
    
    def getFrame(self):
        ret, frame = self.video.read()
        #print("ret 1 ", ret)
        ret, jepg = cv2.imencode(".jpg", frame)
        #print("ret 2 ",ret)
        return jepg.tobytes()

        