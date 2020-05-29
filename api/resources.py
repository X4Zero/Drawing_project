import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import torch.nn.functional as F
import os
from PIL import Image
import cv2
import pandas as pd

# Clases
class_to_idx =  {'0 - zero': 0,
 '1 - one': 1,
 '2 - two': 2,
 '3 - three': 3,
 '4 - four': 4,
 '5 - five': 5,
 '6 - six': 6,
 '7 - seven': 7,
 '8 - eight': 8,
 '9 - nine': 9}

# Dispositivo
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Se define una Red Neuronal Convolucional como una clase para 
# poder usarla como el clasificador
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
		
        # Instantiate the ReLU nonlinearity
        self.relu = nn.ReLU()
        
        # Instantiate two convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=5, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=5, out_channels=10, kernel_size=3, padding=1)
        
        # Instantiate a max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        
        # Instantiate a fully connected layer
        self.fc = nn.Linear(7 * 7 * 10, 10)

    def forward(self, x):

        # Apply conv followd by relu, then in next line pool
        x = self.relu(self.conv1(x))
        x = self.pool(x)

        # Apply conv followd by relu, then in next line pool
        x = self.relu(self.conv2(x))
        x = self.pool(x)

        # Prepare the image for the fully connected layer
        x = x.view(-1, 7*7*10)

        # Apply the fully connected layer and return the result
        return self.fc(x)

# Función para la carga del modelo
def CargarModelo():
    model_sd = CNN()
    print(device)
    model_sd.load_state_dict(torch.load('drawing_model_80e.pth',map_location=torch.device(device)))
    model_sd.eval()
    print('Modelo cargado')
    return model_sd

# Función que permite procesar las imágenes antes de que 
# entren al modelo para su clasificación
def process_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (28,28))
    im_pil = Image.fromarray(image)
    image = np.array(im_pil)
    image = image/255.
                        
    mean = np.array(0.1307)
    sd = np.array(0.3081)

    image = ((image - mean) / sd)

    img_torch = torch.from_numpy(image)
    img_torch = img_torch.unsqueeze_(0)
    img_torch = img_torch.unsqueeze_(0)
    img_torch = img_torch.float()
    return img_torch

# Función que realiza la predicción
def Predict(single_loaded_img, model, topk=10):
  model.to(device)

  output = model.forward(single_loaded_img.to(device))
  probability = F.softmax(output.data,dim=1)
  probs = probability.topk(topk)[0][0].cpu().numpy()

  index_to_class = {val: key for key, val in class_to_idx.items()}

  top_classes = [index_to_class[each] for each in probability.topk(topk)[1][0].cpu().numpy()]
  top_classes = [each for each in probability.topk(topk)[1][0].cpu().numpy()]

  return probs, top_classes

# Función que permite procesar los resultados
#  para una mejor visulización
def Process_results(probs,classes):
  df = pd.DataFrame({'probabilidad':probs, 'clase':classes})
  df.sort_values(by='clase',inplace=True)
  df['probabilidad'] = df['probabilidad'].astype('float')
  df['probabilidad'] = df['probabilidad'] * 100
  df['probabilidad'] = df['probabilidad'].round(2)
  df.set_index('clase',inplace=True)
  return df