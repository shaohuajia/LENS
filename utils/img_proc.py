
# coding: utf-8

# In[1]:


get_ipython().magic(u'matplotlib inline')
from sklearn.model_selection import train_test_split
import numpy as np
import os
from PIL import Image
from scipy import misc
import matplotlib.pyplot as plt

WIDTH  = 256
HEIGHT = 256
NUM_CHANNELS = 1


# In[7]:


def load_images(img_path, img_format):   
    
    im_arrays = []
    # Image from PIL library can read an image file as image, then we can operate the image, like resize and grayscale.
    imfilelist=[os.path.join(img_path, f) for f in os.listdir(img_path) if f.endswith(img_format)]

    for el in imfilelist:
        #print el
        img = Image.open(el)
        #print img.format, img.size, img.mode
        img = img.convert('L')
        img = img.resize((WIDTH, HEIGHT), resample=2)
        im_array = np.array(img)  
        # Normalization: The inputs come in as uint8, we need to convert them to float32 in range [0,1].      
        im_array = im_array / np.float32(255)  
        # The inputs are vectors now, we reshape them to monochrome 2D images,
        # following the shape convention: (rows, columns, channels)
        im_array = im_array.reshape(WIDTH, HEIGHT, NUM_CHANNELS)
        im_arrays.append(im_array)

    return np.array(im_arrays)

#split data into training, validation and testing set
def split_data(inputs_, test_size, val_size, shuffle=False):
    ''' Split arrays or matrices into random train and test subsets
    
        Arguments
        ---------
        inputs: Sequence of indexables with same length
        test_size: If float, should be between 0.0 and 1.0 and represent the proportion of the dataset
                   to include in the test split. If int, represents the absolute number of test samples.
                   If None, the value is set to the complement of the train size
        val_size:  Same as above
        shuffle:   Whether or not to shuffle the data before splitting
    
    '''
    X_train, X_test = train_test_split(inputs_, test_size=test_size, shuffle=shuffle)
    X_train, X_validation = train_test_split(X_train, test_size=val_size, shuffle=shuffle)
    return X_train, X_validation, X_test

#display a few images for sanity check
def check_data(inputs_, nrows=1, ncols=5, figsize=(20,4)):
    
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True, figsize=figsize)
    ax = ax.flatten()
    num = nrows * ncols
    for i in range(num):
        img = inputs_[i]
        if(NUM_CHANNELS == 1):
            ax[i].imshow(np.array(img).reshape(WIDTH, HEIGHT), cmap='Greys_r')
        else:
            ax[i].imshow(np.array(img).reshape(WIDTH, HEIGHT, NUM_CHANNELS))
        ax[i].get_xaxis().set_visible(False)
        ax[i].get_yaxis().set_visible(False)
        fig.tight_layout(pad=0.1)

#get batch data for training
def iterate_minibatches(inputs, batchsize, shuffle=False):
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
            #print(excerpt)
        yield inputs[excerpt]

