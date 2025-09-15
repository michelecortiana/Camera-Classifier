import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2 as cv
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

class Model:
    def __init__(self, num_classes):
        #Dimensione delle immagini in input (altezza, larghezza, canali)
        self.input_shape = (112, 149, 1)
        self.classes = num_classes  #Numero di classi del modello
        self.is_trained = False     
        self.model = self._build_cnn_model()  

    def _build_cnn_model(self):
        #Modello CNN sequenziale
        model = models.Sequential([
            layers.Input(shape=self.input_shape),            #Layer di input
            layers.Conv2D(32, (3, 3), activation='relu'),    #Convolution + ReLU
            layers.MaxPooling2D((2, 2)),                     #Max pooling per ridurre dimensione feature map

            layers.Conv2D(64, (3, 3), activation='relu'),    #Secondo strato convoluzionale
            layers.MaxPooling2D((2, 2)),                     #Pooling

            layers.Flatten(),                                #Appiattimento per passare ai Dense
            layers.Dense(128, activation='relu'),            #Fully connected layer
            layers.Dropout(0.5),                             #Dropout per ridurre overfitting
            layers.Dense(self.classes, activation='softmax') #Output layer con softmax per classificazione
        ])

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def load_and_preprocess_data(self, counters):
        #Caricamento e preprocessing dei dati dalle cartelle delle classi
        images = []
        labels = []
        
        for class_idx in range(len(counters)):
            for i in range(1, counters[class_idx] + 1):
                path = f'{class_idx+1}/frame{i}.jpg'
                if not os.path.exists(path):
                    continue  
                    
                img = cv.imread(path, cv.IMREAD_GRAYSCALE)  #Lettura l'immagine in scala di grigi
                if img is None:
                    continue
                
                img = cv.resize(img, (self.input_shape[1], self.input_shape[0]))  
                img = img.astype('float32') / 255.0  #Normalizzazione tra 0 e 1
                images.append(img)
                labels.append(class_idx)
                
                #Data augmentation
                augmented = self.augment_image(img)
                for aug_img in augmented:
                    images.append(aug_img)
                    labels.append(class_idx)
        
        if not images:
            return None, None, None, None  
        
        images = np.array(images).reshape(-1, *self.input_shape) 
        labels = to_categorical(labels, num_classes=self.classes)  #One-hot encoding
        #Divisione in training e validation set
        return train_test_split(images, labels, test_size=0.2, random_state=42)

    def augment_image(self, img):
        #Data augmentation
        variants = []
        h, w = img.shape
                                             
        if np.max(img) < 0.01:  
            return variants  
        
        variants.append(cv.flip(img, 1)) 
        variants.append(cv.flip(img, 0)) 
        
        center = (w // 2, h // 2)
        for angle in [10, -10, 5, -5]: 
            M = cv.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv.warpAffine(img, M, (w, h), borderMode=cv.BORDER_REPLICATE)
            variants.append(rotated)
        
        noisy = img.copy()
        noise = np.random.normal(0, 0.03, img.shape).astype('float32')  
        noisy = np.clip(noisy + noise, 0, 1)
        variants.append(noisy)
        
        return variants

    def train_model(self, counters):
        try:
            #Carica e pre-elabora i dati
            X_train, X_val, y_train, y_val = self.load_and_preprocess_data(counters)
            
            if X_train is None or len(X_train) < 10:
                print("Dati insufficienti per il training!")
                return
            
            #Early stopping per fermare il training se non migliora la validazione
            early_stop = tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True,
                mode='max'
            )
            
            batch_size = min(32, len(X_train))  #Dimensione batch adattiva

            #Addestramento del modello
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val) if len(X_val) > 0 else None,
                epochs=50,
                batch_size=batch_size,
                callbacks=[early_stop] if len(X_val) > 0 else None
            )
            
            self.is_trained = True  
            print(f"Modello addestrato con {len(X_train)} campioni!")
            if len(X_val) > 0:
                print(f"Accuracy validazione: {history.history['val_accuracy'][-1]:.2f}")
        except Exception as e:
            print(f"Errore durante l'addestramento: {str(e)}")
            self.is_trained = False

    def predict(self, frame_data):
        #Previsione della classe per un frame dato
        if not self.is_trained:
            return 0  
            
        ret, frame = frame_data
        if not ret:
            return 0  
            
        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)  #Conversione in scala di grigi
        resized = cv.resize(gray, (self.input_shape[1], self.input_shape[0]))  #Ridimensione
        normalized = resized.astype('float32') / 255.0  #Normalizzazione
        input_tensor = normalized.reshape(1, *self.input_shape)  
        
        predictions = self.model.predict(input_tensor, verbose=0)  #Previsione
        confidence = np.max(predictions[0])  #Massima probabilità
        
        #Soglia dinamica per decidere se accettare la previsione
        threshold = 0.6 if predictions[0][np.argmax(predictions)] > 0.9 else 0.7
        if confidence < threshold:
            return 0 
            
        return np.argmax(predictions) + 1  #Ritorna la classe 
