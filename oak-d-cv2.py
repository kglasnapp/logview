import sys
import numpy as np # numpy - manipulate the packet data returned by depthai
import cv2 # opencv - display the video stream
import depthai as dai # access the camera and its data packets
print("Python:", sys.version.split(' ')[0], " CV2:", cv2.__version__)

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.createColorCamera()
xoutVideo = pipeline.createXLinkOut()
xoutPreview = pipeline.createXLinkOut()

xoutVideo.setStreamName("video")
xoutPreview.setStreamName("preview")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(True)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Linking
camRgb.video.link(xoutVideo.input)
camRgb.preview.link(xoutPreview.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    video = device.getOutputQueue('video')
    preview = device.getOutputQueue('preview')
    i = 0
    wk = 0
    while True:
        print("Show Frame", i, wk)
        videoFrame = video.get()
        previewFrame = preview.get()
        # Get BGR frame from NV12 encoded video frame to show with opencv
        cv2.imshow("video", videoFrame.getCvFrame())
        # Show 'preview' frame as is (already in correct format, no copy is made)
        #cv2.imshow("preview", previewFrame.getFrame())
        wk = cv2.waitKey(1)
        if wk == ord('q'):
            quit()
        
        i += 1