from typing import Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from tensorflow import keras
from tensorflow.keras import layers


class LRClassifier:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000, n_jobs=1)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


def build_cnn(input_shape: Tuple[int, int], num_classes: int) -> keras.Model:
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv1D(128, 5, activation='relu', padding='same'),
        layers.MaxPooling1D(2),
        layers.Conv1D(128, 5, activation='relu', padding='same'),
        layers.GlobalMaxPooling1D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def build_lstm(input_shape: Tuple[int, int], num_classes: int) -> keras.Model:
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Bidirectional(layers.LSTM(128, return_sequences=False)),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def build_cnn_lstm(input_shape: Tuple[int, int], num_classes: int) -> keras.Model:
    inputs = layers.Input(shape=input_shape)
    x = layers.Conv1D(128, 5, activation='relu', padding='same')(inputs)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Conv1D(128, 3, activation='relu', padding='same')(x)
    x = layers.Bidirectional(layers.LSTM(128))(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
