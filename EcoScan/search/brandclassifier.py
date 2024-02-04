# Use a pipeline as a high-level helper
from transformers import pipeline

def get_brand(uploaded_image):
    # Use a pipeline as a high-level helper
    pipe = pipeline("image-classification", model="fsuarez/autotrain-logo-identifier-90194144191")

    # Use the pipeline to classify the image
    result = pipe(uploaded_image)

    # Extract the first value of the result dictionary
    brand = result[0]['label']
    print(brand)

    return brand