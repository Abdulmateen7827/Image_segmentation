import tensorflow as tf
import numpy as np
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO

# Initialize the FastAPI app
app = FastAPI(title="My TensorFlow Model API")

class_names = ['Bitterleaf', 'Efirin', 'Ewedu', 'amunututu', 'elegede', 
               'soko ', 'tete ', 'ugu ', 'uziza leave', 'waterleaf']

# Load your trained model
model = tf.keras.models.load_model('notebook/faruqmobtest3000-1.h5')
# img = '/Users/abdulmateen/Downloads/vegetables/amunututu/IMG_7766.JPG'
def predict_single_image(model, image_bytes, class_names):
    """
    Preprocesses an image from bytes and makes a prediction.
    """
    try:
        # Load and preprocess the image
        img = Image.open(BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to target size
        img = img.resize((224,224))
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Get the predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        predicted_class = class_names[predicted_class_idx]
            
        return predicted_class, confidence, predictions[0]
         
    except Exception as e:
        print(f"An error occurred in prediction: {e}")
        return None, None, None

# Define the prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Receive and read the image file
    image_bytes = await file.read()
    
    # 2. Get predictions
    predicted_class, confidence, predictions = predict_single_image(model, image_bytes, class_names)

    if predicted_class is None:
        return {"error": "Could not process the image or make a prediction."}

    # 3. Convert NumPy types to standard Python types for JSON response
    return {
        "predicted_class": predicted_class,
        "confidence": float(confidence),
        # "predictions": predictions.tolist()
    }

@app.get("/")
def root():
    return {"message": "Welcome to veggie vision API!"}