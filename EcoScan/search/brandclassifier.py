# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("image-classification", model="fsuarez/autotrain-logo-identifier-90194144191")

# Define the path to the image
image_path = "ecoscan/search/assets/img/coke.jpg"

# Use the pipeline to classify the image
result = pipe(image_path)

# Extract the first value of the result dictionary
result = result[0]['label']

# Print the result
print(result)