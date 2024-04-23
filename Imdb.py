#!/usr/bin/env python
# coding: utf-8

# In[1]:


from keras.datasets import imdb


# In[2]:


(train_data,train_label),(test_data,test_label) = imdb.load_data(num_words=10000)


# In[3]:


import numpy as np

def vectorize_sequences(sequences,dimensions=10000):
    results = np.zeros((len(sequences),dimensions))
    for i,sequence in enumerate(sequences):
        results[i,sequence]=1
        
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)


# In[4]:


y_train = np.asarray(train_label).astype('float32')
y_test= np.asarray(test_label).astype('float32')


# In[5]:


from keras.models import Sequential
from keras.layers import Dense


# In[6]:


model = Sequential()

model.add(Dense(16,input_shape=(10000,),activation='relu'))
model.add(Dense(16,activation = 'relu'))
model.add(Dense(1,activation = 'sigmoid'))


# In[7]:


model.compile(optimizer='adam',loss='mse',metrics=['accuracy'])


# In[8]:


model.summary()


# In[9]:


history = model.fit(x_train,y_train,validation_split=0.2,epochs=20,verbose=1,batch_size=512)


# In[10]:


mse,mae = model.evaluate(x_test,y_test)

print('MSE ',mse)
print('MAE ',mae)


# In[11]:


y_preds = model.predict(x_test)


# In[12]:


y_preds


# In[13]:


y_test


# In[38]:


tests=[]
for i in y_test:
    tests.append(int(i))


# In[39]:


preds=[]
for i in y_preds:
    if i[0]>0.5:
        preds.append(1)
    else:
        preds.append(0)


# In[41]:


from sklearn.metrics import accuracy_score,precision_score,recall_score

print(accuracy_score(tests,preds))
print(precision_score(tests,preds))
print(recall_score(tests,preds))


# In[14]:


# word_index is a dictionary mapping words to an integer index
word_index = imdb.get_word_index()


# In[15]:


def return_token(tid):
    for k,v in word_index.items():
        # We decode the review; note that our indices were offset by 3
        # because 0, 1 and 2 are reserved indices for "padding", "start of sequence", and "unknown".
        if v==tid-3:
            return k
    return '?'


# In[16]:


def print_review(id_):
    sentence = ' '.join(return_token(i) for i in train_data[id_])
    return sentence


# In[17]:


print_review(0)


# In[18]:


train_label[0] #Positive


# In[19]:


print_review(1)


# In[20]:


train_label[1] # Negaive


# In[21]:


print_review(2)


# In[22]:


train_label[2] # Negaive


# In[ ]:





# In[27]:


def predict_review(model, review, word_index):
    # Tokenize the review
    review = review.lower()
    words = review.split()
    
    # Convert words to indices
    encoded_review = [word_index.get(word, 0) for word in words]
    
    # Vectorize the review
    vectorized_review = vectorize_sequences([encoded_review], dimensions=10000)
    
    # Predict sentiment
    prediction = model.predict(vectorized_review)[0][0]
    return prediction



# Test with sample review
sample_review = "The movie was fantastic! I loved every minute of it."
prediction = predict_review(model, sample_review, word_index)
print("Predicted Sentiment:", "Positive" if prediction > 0.6 else "Negative")


# In[ ]:




