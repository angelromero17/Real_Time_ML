# -*- coding: utf-8 -*-
"""HW2_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lJYG4uq6Rqj2yzzWW7Z08dKUF7EvYitm
"""

#Import necesseray libraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import torch
import torch.optim as optim
import torch.nn as nn 
import seaborn as sns

#Give access to the google drive
from google.colab import drive
drive.mount('/content/drive')

#Import and display Housing.csv from the google drive
housing = pd.DataFrame(pd.read_csv("/content/drive/MyDrive/Colab Notebooks/Housing.csv")) 
housing.head()

map = len(housing) 
map

housing.shape

#Display the information from the Housing.csv file
housing.info()

housing.describe()

#Some of the column values are strings and not numbers so the values need to be converted
var_list =  ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning',] 
 
#Map function from string to number value
def binary_map(x): 
    return x.map({'Yes': 1, "No": 0}) 
 
#Use function on list
housing[var_list] = housing[var_list].apply(binary_map) 
housing.head()

#Training and testing data splits 
from sklearn.model_selection import train_test_split 
 
#Split the training to 80% and testing to 20%
np.random.seed(0) 
df_train, df_test = train_test_split(housing, train_size = 0.8, test_size = 0.2, random_state = 42)
df_train.shape

#Determine test shape
df_test.shape

#Train data set given variables below
numVars = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking','price'] 
df_Newtrain = df_train[numVars] 
df_Newtest = df_test[numVars] 
df_Newtrain.head()

df_Newtrain.shape

#Data needs to be standersied or normalized so that it can be comperable
import warnings 
warnings.filterwarnings('ignore') 
from sklearn.preprocessing import MinMaxScaler, StandardScaler 
 
#Define standard scaler 
scaler = MinMaxScaler() 
df_Newtrain[numVars] = scaler.fit_transform(df_Newtrain[numVars]) 
df_Newtrain.head(20) 
df_Newtest[numVars] = scaler.fit_transform(df_Newtest[numVars])
df_Newtest.head(20)

#Pops the values for price
y_Newtrain = df_Newtrain.pop('price') 
x_Newtrain = df_Newtrain 
y_Newtest = df_Newtest.pop('price')
x_Newtest = df_Newtest

#Training the dataset
y_Newtrain = torch.tensor(y_Newtrain.values).float()
y_Newtrain = y_Newtrain[:,None]
x_Newtrain = torch.tensor(x_Newtrain.values).float()
y_Newtest = torch.tensor(y_Newtest.values).float()
y_Newtest = y_Newtest[:,None]
x_Newtest = torch.tensor(x_Newtest.values).float()

#Creating a loop with layers to train for the given number of epochs
def training_loop(n_epochs, optimizer, model, loss_fn, t_u_train, t_u_val,
                  t_c_train, t_c_val):
    for epoch in range(1, n_epochs + 1):
        t_p_train = model(t_u_train)
        loss_train = loss_fn(t_p_train, t_c_train)

        t_p_val = model(t_u_val) 
        loss_val = loss_fn(t_p_val, t_c_val)
        
        optimizer.zero_grad()
        loss_train.backward()
        optimizer.step()

        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch}, Training loss {loss_train.item():.4f},"
                  f" Validation loss {loss_val.item():.4f}")

#Sequential model 1
seq_model_0 = nn.Sequential(
            nn.Linear(5, 8), #1
            nn.Tanh(),
            nn.Linear(8, 5)) #1
seq_model_0

#Sequential model 1 with the number of layers
seq_model_1 = nn.Sequential(
            nn.Linear(5, 8), # <1>
            nn.Tanh(),
            nn.Linear(8, 4), # <2>
            nn.Tanh(),
            nn.Linear(4, 2), # <2>
            nn.Tanh(),
            nn.Linear(2, 1)) # <2>
seq_model_1

#Training and displaying the results of the model for 200 epochs
optimizer = optim.SGD(seq_model_0.parameters(), lr=1e-3)

training_loop(200,optimizer,seq_model_0,nn.MSELoss(), x_Newtrain, x_Newtest, y_Newtrain, y_Newtest)

#Training and displaying the results of the model for 200 epochs
optimizer = optim.SGD(seq_model_1.parameters(), lr=1e-3)

training_loop(200,optimizer,seq_model_1,nn.MSELoss(), x_Newtrain, x_Newtest, y_Newtrain, y_Newtest)