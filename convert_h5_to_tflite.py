import tensorflow as tf
import keras
from keras.models import load_model

emotion_model = load_model('model/emotion_detection_model_100epochs.h5', compile=False)

converter = tf.lite.TFLiteConverter.from_keras_model(emotion_model)
tflite_model = converter.convert()
open("emotion_detection_model_100epochs_no_opt.tflite", "wb").write(tflite_model)