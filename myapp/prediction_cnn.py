import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json

# Define the image dimensions



# Function to preprocess the image and make predictions
def predict_single_image(image_path):
    img_width, img_height = 100, 100  # Same as your training dimensions

    # Load the model architecture
    with open('alexnew.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)

    # Load the model weights
    model.load_weights("alexnew.weights.h5")

    print("Model loaded successfully.")
    """
    Predicts the class of a single image.

    Args:
        image_path (str): Path to the image file.
        model (Keras Model): Loaded Keras model for prediction.

    Returns:
        Prediction: The predicted class.
    """
    # Load the image
    img = image.load_img(image_path, target_size=(img_width, img_height))

    # Convert the image to array
    img_array = image.img_to_array(img)

    # Expand dimensions to match model input
    img_array = np.expand_dims(img_array, axis=0)

    # Normalize the image (same as during training)
    img_array = img_array / 255.0

    # Predict the class
    predictions = model.predict(img_array)

    # Get the class index with highest probability
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    print(predicted_class, confidence)
    return predicted_class, confidence,predictions

#
# # Path to the test image
# test_image_path = r"C:\Users\Fathima\Downloads\boy.jpg"
#
# # Predict the class
# predicted_class, confidence = predict_single_image(test_image_path, loaded_model)
#
# # Output the result
# print(f"Predicted Class: {predicted_class}, Confidence: {confidence:.2f}")
