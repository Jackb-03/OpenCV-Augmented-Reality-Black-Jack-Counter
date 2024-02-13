## Credit 
First and foremost credit to Edje Electronics with already existing openCV card detector found in this video https://github.com/EdjeElectronics/OpenCV-Playing-Card-Detector
Without it this project would have take me many more hours to complete.
Link to his project: https://github.com/EdjeElectronics/OpenCV-Playing-Card-Detector

## Explanation 
This is a Python program that uses OpenCV to detect and identify playing cards from a PiCamera video or a USB webcam. It then calcualtes the count and streams it 
in a VR compatiable manner to a phone VR headset giving the user an advantage.
![Screenshot (94)](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/87334062-4110-4d41-86cf-a4939191f446)# OpenCV-Playing-Card-Counter


The headset itself is a cheap one where you put your phone through below with a webcam attached as show below.
![image](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/c95c88e4-c840-46db-83cf-676bcaa54688)

To the phone the openCV webcam output is stream to it. 
![image](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/ffe87222-c0e6-432a-9fab-525f00a70d7c)

Which once inserted and viewed through the headset provides the AR hud.
![image](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/a9b25bd1-58f9-4d20-8dec-f22375389235)

To the viewer it looks something like this, 
![Screenshot (94)](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/d414033b-30e6-4f3d-92c0-6e56c787a8e2)
With the counter to the top left corner.

The way the counter works is essentitally the that it keeps a running count on the cards, for instance any card from 2-6 is a +1, 7-9 a 0 and a 10-Ace a -1.
Therefore the higher the count the higher chance of a 10 helping you to decide if you should hit or stand.
For a more detailed explanation of what card counting is follow the tutorial below:
https://www.blackjackapprenticeship.com/how-to-count-cards/ 




## Usage
Download this repository to a directory and run CardDetector.py from that directory. Cards need to be placed on a dark background for the detector to work. Press 'q' to end the program.

The program was originally designed to run on a Raspberry Pi with a Linux OS, but it can also be run on Windows 7/8/10. To run on Windows, download and install Anaconda (https://www.anaconda.com/download/, Python 3.6 version), launch Anaconda Prompt, and execute the program by launching IDLE (type "idle" and press ENTER in the prompt) and opening/running the CardDetector.py file in IDLE. The Anaconda environment comes with the opencv and numpy packages installed, so you don't need to install those yourself. If you are running this on Windows, you will also need to change the program to use a USB camera, as described below.

The program allows you to use either a PiCamera or a USB camera. If using a USB camera, change line 38 in CardDetector.py to:
```
videostream = VideoStream.VideoStream((IM_WIDTH,IM_HEIGHT),FRAME_RATE,2,0).start()
```

The card detector will work best if you use isolated rank and suit images generated from your own cards. To do this, run Rank_Suit_Isolator.py to take pictures of your cards. It will ask you to take a picture of an Ace, then a Two, and so on. Then, it will ask you to take a picture of one card from each of the suits (Spades, Diamonds, Clubs, Hearts). As you take pictures of the cards, the script will automatically isolate the rank or suit and save them in the Card_Imgs directory (overwriting the existing images).

![image](https://github.com/Jackb-03/OpenCV-Playing-Card-Detector-master/assets/94686461/3a601d81-149d-4239-91f2-6e83ef300551)

## Files
CardDetector.py contains the main script

Cards.py has classes and functions that are used by CardDetector.py

PiVideoStream.py creates a video stream from the PiCamera, and is used by CardDetector.py

Rank_Suit_Isolator.py is a standalone script that can be used to isolate the rank and suit from a set of cards to create train images

Card_Imgs contains all the train images of the card ranks and suits

## Dependencies
Python 3.6

OpenCV-Python 3.2.0 and numpy 1.8.2:
See https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
for how to build and install OpenCV-Python on the Raspberry Pi

picamera library:
```
sudo apt-get update
sudo apt-get install python-picamera python3-picamera
```


