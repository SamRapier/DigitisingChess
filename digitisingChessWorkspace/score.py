import os
import logging
import json
import numpy as np
from tensorflow import keras
from PIL import Image


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # model_path = os.path.join(
    #     os.getenv("AZUREML_MODEL_DIR"), "LeNet5_chess_piece_classifier/"
    #     # "model/LeNet5_chess_piece_classifier"
    # )
    model_path = "model/LeNet5_chess_piece_classifier"
    # deserialize the model file back into a sklearn model
    # model = joblib.load(model_path)
    model = keras.models.load_model("C:/Users/samra/GitHub/DigitisingChess/digitisingChessWorkspace/LeNet5_chess_piece_classifier")
    logging.info("Init complete")


def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("Request received")
    # data = json.loads(raw_data)["data"]
    data = np.array(raw_data)
    data = np.pad(data, ((2,2),(2,2),(0,0)), 'constant')
    data = data.reshape(-1, 154, 154, 3)
    result = model.predict(data)
    logging.info("Request processed")
 
    return result.tolist()

if __name__ == "__main__":
    init()

    # Image.open(imagePath + file)
    # imagePath = "C:/Users/samra/GitHub/DigitisingChess/chessPieces/"
    imagePath = "C:/Users/samra/OneDrive/CompSciUni/Year4/Project/images_chess_pieces/"
    # file = "square_e1.jpg"
    # file = "wP/_board_1353.jpg_450_900.jpg"
    file = "wK/_board2_1655.jpg_1050_600.jpg"
    image = Image.open(imagePath + file)
    # image_2 = np.pad(image, ((2,2),(2,2),(0,0)), 'constant')
    # image_2 = image_2.reshape(-1, 154, 154, 3)
    
    print(run(image))