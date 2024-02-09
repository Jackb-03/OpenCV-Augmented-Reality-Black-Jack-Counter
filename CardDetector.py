############## Python-OpenCV Playing Card Detector ###############
#
# Author: Evan Juras
# Date: 9/5/17
# Description: Python script to detect and identify playing cards
# from a PiCamera video feed.
#

# Import necessary packages
import cv2
import numpy as np
import time
import os
import Cards
import VideoStream


### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

## Camera settings
IM_WIDTH = 1920
IM_HEIGHT = 1080
FRAME_RATE = 60
removedCard = 0
totalCount = 0


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_count_value(self):
        low_cards = ["Two", "Three", "Four", "Five", "Six"]
        high_cards = ["Ten", "Jack", "Queen", "King", "Ace"]

        if self.rank in low_cards:
            return +1  # Low cards add to the count
        elif self.rank in high_cards:
            return -1  # High cards subtract from the count
        else:
            return 0  # Neutral cards don't affect the count

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False


class Deck:
    ranks = [
        "Ace",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Jack",
        "Queen",
        "King",
    ]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def remove_card(self, rank, suit):
        card_to_remove = Card(rank, suit)
        if card_to_remove in self.cards:
            self.cards.remove(card_to_remove)
            count_value = (
                card_to_remove.get_count_value()
            )  # Get the count value of the removed card
            print(f"Card {card_to_remove} removed")
            return count_value  # Return the removed card and its count value
        else:
            return 0  # Return None and a count value of 0 if the card is not found

    def get_all_cards(self):
        return self.cards

    def cards_as_string(self, max_length=50):
        # Convert the list of cards to a string
        cards_text = ", ".join(str(card) for card in self.cards)

        # Truncate the string if it exceeds the maximum length
        if len(cards_text) > max_length:
            cards_text = cards_text[:max_length] + "..."

        return cards_text

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"


deck = Deck()

## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
frame_rate_calc = 1
freq = cv2.getTickFrequency()

## Define font to use
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera object and video feed from the camera. The video stream is set up
# as a seperate thread that constantly grabs frames from the camera feed.
# See VideoStream.py for VideoStream class definition
## IF USING USB CAMERA INSTEAD OF PICAMERA,
## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
videostream = VideoStream.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE, 2, 0).start()
time.sleep(1)  # Give the camera time to warm up

# Load the train rank and suit images
path = os.path.dirname(os.path.abspath(__file__))
train_ranks = Cards.load_ranks(path + "/Card_Imgs/")
train_suits = Cards.load_suits(path + "/Card_Imgs/")


### ---- MAIN LOOP ---- ###
# The main loop repeatedly grabs frames from the video stream
# and processes them to find and identify playing cards.

cam_quit = 0  # Loop control variable

# Begin capturing frames
while cam_quit == 0:

    # Grab frame from video stream
    image = videostream.read()

    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Pre-process camera image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)

    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

    # If there are no contours, do nothing
    if len(cnts_sort) != 0:

        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards = []
        k = 0

        # For each contour detected:
        for i in range(len(cnts_sort)):
            if cnt_is_card[i] == 1:

                # Create a card object from the contour and append it to the list of cards.
                # preprocess_card function takes the card contour and contour and
                # determines the cards properties (corner points, etc). It generates a
                # flattened 200x300 image of the card, and isolates the card's
                # suit and rank from the image.
                cards.append(Cards.preprocess_card(cnts_sort[i], image))

                # Find the best rank and suit match for the card.
                (
                    cards[k].best_rank_match,
                    cards[k].best_suit_match,
                    cards[k].rank_diff,
                    cards[k].suit_diff,
                ) = Cards.match_card(cards[k], train_ranks, train_suits)

                # Draw center point and match result on the image.
                image = Cards.draw_results(image, cards[k])
                removedCard = deck.remove_card(
                    cards[k].best_rank_match, cards[k].best_suit_match
                )
                totalCount += removedCard
                k = k + 1

        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if len(cards) != 0:
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
            cv2.drawContours(image, temp_cnts, -1, (255, 0, 0), 2)

    # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
    # so the first time this runs, framerate will be shown as 0.
    cv2.putText(
        image,
        "FPS: " + str(int(frame_rate_calc)),
        (50, 300),
        font,
        0.7,
        (255, 0, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        image,
        str(totalCount),
        (100, 400),
        font,
        2,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        image,
        str(totalCount),
        (1050, 400),
        font,
        2,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    # Finally, display the image with the identified cards!
    cv2.imshow("Card Detector", image)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # Poll the keyboard. If 'q' is pressed, exit the main loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1


# Close all windows and close the PiCamera video stream.
cv2.destroyAllWindows()
videostream.stop()
