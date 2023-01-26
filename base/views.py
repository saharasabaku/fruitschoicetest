from django.shortcuts import render
import datetime
import os
from PIL import Image
import numpy as np
from pathlib import Path


import tensorflow
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation,Dropout,Flatten,Dense
from tensorflow import keras

import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials

gsjson =os.path.join(os.path.expanduser('~'),'client_secret.json')


BASE_DIR = Path(__file__).resolve().parent

class gsset:

    def pull():
        item = []
        scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(gsjson, scope)
        client = gs.authorize(creds)
        sheet = client.open("test").sheet1
        
        item.append(sheet.cell(4,5).value) #hakensaki
        item.append(sheet.cell(5,5).value) #name
        return item

    def add(item):
        scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(gsjson, scope)
        client = gs.authorize(creds)
        sheet = client.open("test").sheet1

        sheet.update_cell(1, 5, item[0])
        sheet.update_cell(1, 9, item[1])
        sheet.update_cell(4, 5, item[2])
        sheet.update_cell(5 ,5, item[3])


def index(request):
    fruits = ""
    accuracy =""
    img = ""
    
    if request.method == "POST":
        request.FILES["inputimg"]

    if request.method == "POST":

        img = request.FILES["inputimg"]


        labels = ["grape","apple","orange"]
        resize_settings = (50,50)
        X     = []                               # 推論データ格納
        image = Image.open(img) # 画像読み込み
        image = image.convert("RGB")             # RGB変換
        image = image.resize(resize_settings)    # リサイズ
        data  = np.asarray(image)                # 数値の配列変換
        X.append(data)
        X     = np.array(X)

        # モデル呼び出し
        model = predict()
        
        # numpy形式のデータXを与えて予測値を得る
        model_output = model.predict([X])[0]
        # 推定値 argmax()を指定しmodel_outputの配列にある推定値が一番高いインデックスを渡す
        predicted = model_output.argmax()
        # アウトプット正答率
        accuracy = int(model_output[predicted] *100)
        fruits = labels[predicted]


    request.POST
    today = datetime.datetime.now()
    context = {
        'today':today,
        'fruits':fruits,
        'accuracy':accuracy,
        'img':img
    }
    return render(request, 'base/fruits.html',context)


#def newuser(request):





def predict():
    #インスタンス
    model = Sequential()
    # 1層目 (畳み込み）
    #model.add(Conv2D(32,(3,3),padding="same", input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    # 2層目（Max Pooling)
    model.add(Conv2D(32,(3,3)))
    model.add(Activation('relu'))
    # 3層目 (Max Pooling)
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.3))
    # 4層目 (畳み込み)
    model.add(Conv2D(64,(3,3),padding="same"))
    model.add(Activation('relu'))
    # 5層目 (畳み込み)
    model.add(Conv2D(64,(3,3))) 
    model.add(Activation('relu'))
    # 6層目 (Max Pooling)
    model.add(MaxPooling2D(pool_size=(2,2)))
    # データを1列に並べる
    model.add(Flatten())
    # 7層目 (全結合層)
    model.add(Dense(512))                                       
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    # 出力層(softmaxで確率を渡す：当てはまるものを1で返す)
    model.add(Dense(3)) 
    model.add(Activation('softmax'))
    # 最適化の手法
    opt = tensorflow.keras.optimizers.legacy.RMSprop(lr=0.005, decay=1e-6)
    # 損失関数
    model.compile(loss="categorical_crossentropy",
    optimizer=opt,
    metrics=["accuracy"]
    ) 

    # モデル学習(推論では不要のためコメントアウト)
    # model.fit(X_train,y_train,batch_size=10,epochs=150) 
    
    # モデルを読み込み
    model = keras.models.load_model(os.path.join(BASE_DIR,"cnn_h5"))
    
    return model