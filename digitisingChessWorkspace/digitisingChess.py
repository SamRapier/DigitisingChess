import gc, os, argparse, utils
from turtle import update

from utils import ImageObject
from config import *
from slid import pSLID, SLID, slid_tendency #== step 1
from laps import LAPS                       #== step 2
from llr import LLR, llr_pad                #== step 3

from cropImage import gridSegmentation

from keras import backend as K

from PIL import Image
import score
from FEN_builder import updateFEN
import numpy as np


import cv2; load = cv2.imread
save = cv2.imwrite

#NC_SCORE = -1

################################################################################

def layer():
    global NC_LAYER, NC_IMAGE#, NC_SCORE
    
    print(utils.ribb("==", sep="="))
    print(utils.ribb("[%d] LAYER " % NC_LAYER, sep="="))
    print(utils.ribb("==", sep="="), "\n")

    # --- 1 step --- find all possible lines (that makes sense) ----------------
    print(utils.ribb(utils.head("SLID"), utils.clock(), "--- 1 step "))
    segments = pSLID(NC_IMAGE['main'])
    raw_lines = SLID(NC_IMAGE['main'], segments)
    lines = slid_tendency(raw_lines)

    # --- 2 step --- find interesting intersections (potentially a mesh grid) --
    print(utils.ribb(utils.head("LAPS"), utils.clock(), "--- 2 step "))
    points = LAPS(NC_IMAGE['main'], lines)
    #print(abs(49 - len(points)), NC_SCORE)
    #if NC_SCORE != -1 and abs(49 - len(points)) > NC_SCORE * 4: return
    #NC_SCORE = abs(49 - len(points))

    # --- 3 step --- last layer reproduction (for chessboard corners) ----------
    print(utils.ribb(utils.head(" LLR"), utils.clock(), "--- 3 step "))
    inner_points = LLR(NC_IMAGE['main'], points, lines)
    four_points = llr_pad(inner_points, NC_IMAGE['main']) # padcrop

    # --- 4 step --- preparation for next layer (deep analysis) ----------------
    print(utils.ribb(utils.head("   *"), utils.clock(), "--- 4 step "))
    print(four_points)
    try: NC_IMAGE.crop(four_points)
    except:
        utils.warn("niestety, ale kolejna warstwa nie jest potrzebna")
        NC_IMAGE.crop(inner_points)

    print("\n")

################################################################################

def detect(args):
    global NC_LAYER, NC_IMAGE, NC_CONFIG

    if (not os.path.isfile(args.input)):
        utils.errn("error: the file \"%s\" does not exits" % args.input)

    NC_IMAGE, NC_LAYER = ImageObject(load(args.input)), 0
    for _ in range(NC_CONFIG['layers']):
        NC_LAYER += 1; layer()
    save("outputs/detected_board.jpg", NC_IMAGE['orig'])

    print("DETECT: %s" % args.input)



def pieceDecider(pieceProbabilityArr, pieceMap):
    # basic pieceDecider picks the piece with the highest probability
    
    index_max = np.argmax(np.asarray(pieceProbabilityArr))
    return pieceMap[index_max]


def createPieceMap():
    labels = []
    root_image_path = 'C:/Users/samra/OneDrive/CompSciUni/Year4/Project/images_chess_pieces/'
    dirs = os.listdir(root_image_path)

    for dir in dirs:
        for i in range(len(os.listdir(root_image_path + str(dir)))):
            labels.append(str(dir))

    d = dict([(y,x) for x,y in enumerate(sorted(set(labels)))])
    inv_map = {v: k for k, v in d.items()}

    return inv_map


if __name__ == "__main__":
    utils.reset()

    # take input image
    p = argparse.ArgumentParser(description= 'Find, crop and create FEN from image.')

    p.add_argument('--input', type=str, help='input image (default: input.jpg)')
    p.add_argument('--output', type=str, help='output path (default: output.jpg)')
    args = p.parse_args()

    # send image to board detection
    detect(args)

    K.clear_session(); gc.collect()


    # use cropImage for grid segmentation
    gridSegmentation("outputs/detected_board.jpg")

    # use model to score each grid square
    chessSquaresPath = "outputs/chessSquares/"
    chessSquares = os.listdir(chessSquaresPath)
    FENcode = '8/8/8/8/8/8/8/8'

    pieceMap = {0: '_', 1: 'b', 2: 'k', 3: 'n', 4: 'p', 5: 'q', 6: 'r', 7: 'B', 8: 'K', 9: 'N', 10: 'P', 11: 'Q', 12: 'R'}

    score.init()

    for imageName in chessSquares:
        image = Image.open(chessSquaresPath + imageName)
        
        # send each image to CNN model 
        # use output of model to evaulate the probability of piece
        pieceProbability = score.run(image)

        pieceDecider(pieceProbability, pieceMap)

        # process each response from CNN model
        # calculate which piece it is from the probability score
        piece = pieceDecider(pieceProbability, pieceMap)


        # build FEN code 
        FENcode = updateFEN(imageName[:2],piece,FENcode)
        
    lichessLink = "https://lichess.org/analysis/" + FENcode
    print("-------------------------------------------")
    print("FEN code: " + FENcode)
    print(lichessLink)
    print("-------------------------------------------")
            
