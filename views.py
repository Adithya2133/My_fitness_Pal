from io import BytesIO
from django.shortcuts import render,redirect
import requests
from tensorflow.keras.models import load_model
import os
from django.http import JsonResponse

import tensorflow as tf

import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import regularizers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2
from bs4 import BeautifulSoup

from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.applications.inception_v3 import preprocess_input

import cv2
import os
import random
import collections
from collections import defaultdict

from shutil import copy
from shutil import copytree, rmtree

import numpy as np
import json

import matplotlib.pyplot as plt
import matplotlib.image as img




model_best = load_model('C:/Users/pc/food_detection/food_detection/model/bestmodel_4class.hdf5',compile = False)

data_dir = "C:/Users/pc/food_detection/food_detection/dataset/food-101/images"
foods_sorted = sorted(os.listdir(data_dir))

from PIL import Image

food_list = ['Food_Not_Detected','chicken wings','fried rice','pizza']

def food(request):
      message=''
  
      if request.method == "POST":
            
            
            img_bytes = request.FILES['image'].read()
            img = Image.open(BytesIO(img_bytes))
            img = img.resize((299, 299))
            img = np.array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            pred = model_best.predict(img)
            index = np.argmax(pred)
            print(index)
            food_list.sort()
            pred_value = food_list[index]
            print(pred_value)
            if pred_value == 'Food_Not_Detected':
                  message='Oops! It seems like the food image is not valid'
                  return render(request,'home.html' , {'message':message})
                  
                  
            # headers = {
            #       'x-app-id': '71bf42ae',
            #       'x-app-key': 'e9d83b511e54c88fbb19b5cf0d31b4ae',
            # }
            # params = {
            #       'query': pred_value,
            #       'timezone': 'US/Eastern'
            # }
            # endpoint = ' https://trackapi.nutritionix.com/v2/search/item'
            # response = requests.get(endpoint, headers=headers, params=params)
            
            # if response.status_code == 200:
            #       data = response.json(
            #       calories = data['foods'][0]['nf_calories']
            #       return render(request,'result.html',{'pred':pred_value,'cal':calories})
            else:
                  api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
                  query = pred_value
                  response = requests.get(api_url + query, headers={'X-Api-Key': 'rWBa3XITZcYCtb0e7mlS2w==QkXNkP7OBumjvaUl'})
                  if response.status_code == requests.codes.ok:
                        print(response.text)
                        data = json.loads(response.text)
                        calories = data['items'][0]['calories']
                        total_fat=data['items'][0]['fat_total_g']
                        fat_saturated_g=data['items'][0]['fat_saturated_g']
                        protein_g=data['items'][0]['protein_g']
                        sodium_mg=data['items'][0]['sodium_mg']
                        potassium_mg=data['items'][0]['potassium_mg']
                        carbohydrates_total_g=data['items'][0]['carbohydrates_total_g']
                        fiber_g=data['items'][0]['fiber_g']
                        sugar_g=data['items'][0]['sugar_g']
                        
                        print(calories)

                        return render(request,'result.html',{'pred':pred_value,'cal':calories,'fat':total_fat,'satfat':fat_saturated_g,'protein':protein_g,'sodium':sodium_mg,'pottasium':potassium_mg,'choles':carbohydrates_total_g,'fiber':fiber_g,'sugar':sugar_g})
                  else:
                        calories='no calories'
                        return render(request,'result.html',{'pred':pred_value,'cal':calories})
      return render(request, 'home.html',{'message':message})

def bmi(request):
      print(bmi)
      return render(request, 'bmi.html')
  
def recipe(request):
      if request.method=='POST':
            data=request.POST.get("dish")
            app_id = "865083df"
            app_key = "8e1d813ba9007e03ece7c9b5148a8b3c"

            # Set the API endpoint URL and query parameters
            url = "https://api.edamam.com/search"
            query = data
            params = {
            "q": query,
            "app_id": app_id,
            "app_key": app_key
            }

            # Make the API request and get the response data
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:
                  da = response.json()
                  
                  recipies=da['hits']
                  print(recipies)
                  return render(request, 'recipe_result.html',{'recipe':recipies}) 
                  
            else:
                  print("Error:", response.status_code, response.text)
            return redirect('recipe_result')
      return render(request, 'recipe.html')
            
    

def recipe_result(request):
      return render(request, 'recipe_result.html')




