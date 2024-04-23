#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


# In[3]:


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


# In[4]:


train_images.shape


# In[5]:


train_images = train_images / 255.0
test_images = test_images / 255.0


# In[7]:


from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape = (28, 28)),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dense(10)
])

model.compile(optimizer = 'adam', loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True), metrics = ['accuracy'])
model.summary()


# In[8]:


model.fit(train_images, train_labels, epochs = 10)


# In[9]:


test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 2)
print("\n Test accuracy = ", test_acc)


# In[10]:


probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


# In[5]:


predictions = probability_model.predict(test_images)
# print(predictions)


# In[1]:


def plot_image(i, predictions_array, true_label, img):
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    confidence = np.max(predictions_array) * 100
    predicted_class = class_names[predicted_label]
    true_class = class_names[true_label]

    plt.xlabel(f"{predicted_class} {confidence:.0f}% ({true_class})", color=color)


# In[4]:


rows = 5
cols = 5
total_images = rows * cols

plt.figure(figsize=(10, 10))
for i in range(total_images):
    plt.subplot(rows, cols, i + 1)
    plot_image(i, predictions[i], test_labels[i], test_images[i])
plt.tight_layout()
plt.show()


# In[ ]:




