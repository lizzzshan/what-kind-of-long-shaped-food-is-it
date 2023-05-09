# -*- coding: utf-8 -*-
"""Image-classification-springrolls-or-sashimi

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-XIUonnL7kH8ZIoFzVFFV97xPVk6gCKK

# Training a food classifier using fastai

Are you looking at spring rolls or sashimi? This model will tell you!

### Loading and preparing the data

TODO: Change this to run on a GPU
"""

import torch
!pip install -Uqq fastai 
from fastai.vision.all import *

# Downloading the flowers dataset: https://docs.fast.ai/data.external.html
food_path = untar_data(URLs.FOOD)

# Display table using Pandas to look at the categories
pd.read_json('/root/.fastai/data/food-101/test.json')

# Set the labels as the foods we want to classify (in this case sashimi and spring rolls)
sashimi = 'sashimi'
spring_rolls = 'spring_rolls'

"""### Data prep and some cleaning up

This function has 2 main roles:

1.   Remove all the images that don't have *sashimi* or *spring rolls*. 
2.   Rename sashimi or spring roll images to have that in their filename for easier usage.


"""

for img in get_image_files(food_path):
  # rename the correct images to have the label name 
  if sashimi in str(img):
    img.rename(f"{img.parent}/{sashimi}-{img.name}")
  elif spring_rolls in str(img):
    img.rename(f"{img.parent}/{spring_rolls}-{img.name}")
  # If the images don't fit in those categories, remove img
  else:
    os.remove(img)

"""# Training the model"""

def getLabel(fileName):
  return fileName.split('-')[0]

# Testing getLabel function 
# ---------------------------

# getLabel("sashimi-100113.jpg")
#getLabel("spring_rolls-100113.jpg")

dls = ImageDataLoaders.from_name_func(
    food_path, get_image_files(food_path), valid_pct=0.2, seed=420,
    label_func=getLabel, item_tfms=Resize(32))

dls.train.show_batch()

"""# Convolutional neural network

TODO: Add blurb explaining CNN
"""

learn = cnn_learner(dls, resnet34, metrics=error_rate, pretrained=True)
learn.fine_tune(epochs=2)

"""# Verify model

### Test the model using uploaded images
"""

from google.colab import files
input_img = files.upload()

for img in input_img.items():
  uploaded_img = img[0]
img = PILImage.create(uploaded_img)
img.show()

label,_,probs = learn.predict(img)

print(f"This is most likely a {label}.")
print(f"The probability of this being a sashimi is {probs[1].item():.6f}")
print(f"The probability of this being a spring_roll is {probs[0].item():.6f}")

"""# UP NEXT: Test model using images in a dataset 

TODO: Implement test using a dataset
"""

