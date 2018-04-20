import os
import numpy as np
import tensorflow as tf
import input_data
import model
import matplotlib.pyplot as plt

#%%

N_CLASSES = 2
IMG_W = 208  # resize the image, if the input image is too large, training will be very slow.
IMG_H = 208
BATCH_SIZE = 16
CAPACITY = 2000
MAX_STEP = 10000 # with current parameters, it is suggested to use MAX_STEP>10k
learning_rate = 0.0001 # with current parameters, it is suggested to use learning rate<0.0001

from PIL import Image
# import matplotlib.pyplot as plt

def get_one_random_image(train):
    '''Randomly pick one image from training data
    Return: ndarray
    '''
    n = len(train)
    ind = np.random.randint(0, n)
    img_dir = train[ind]

    image = Image.open(img_dir)
    plt.show(image)
    image = image.resize([208, 208])
    image = np.array(image)
    return image

def get_image(img_dir):
    image = Image.open(img_dir)
    image = image.resize([208, 208])
    image = np.array(image)
    return image

def evaluate_image(image_array):
    with tf.Graph().as_default():
        BATCH_SIZE = 1
        N_CLASSES = 2

        image = tf.cast(image_array, tf.float32)
        image = tf.image.per_image_standardization(image)
        image = tf.reshape(image, [1, 208, 208, 3])
        logit = model.inference(image, BATCH_SIZE, N_CLASSES)

        logit = tf.nn.softmax(logit)

        x = tf.placeholder(tf.float32, shape=[208, 208, 3])

        # you need to change the directories to yours.
        logs_train_dir = 'logs/train/'

        saver = tf.train.Saver()

        with tf.Session() as sess:

            print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(logs_train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print('Loading success, global_step is %s' % global_step)
            else:
                print('No checkpoint file found')

            prediction = sess.run(logit, feed_dict={x: image_array})
            max_index = np.argmax(prediction)
            if max_index==0:
                result = 'This is a cat with possibility %.6f' %prediction[:, 0]
            else:
                result = 'This is a dog with possibility %.6f' %prediction[:, 1]
            print(result)
            return result
    
    
def evaluate_random_image():
    '''Test one image against the saved models and parameters
    '''
    
    # you need to change the directories to yours.
    train_dir = 'data/train/'
    train, train_label = input_data.get_files(train_dir)
    random_img = get_one_random_image(train)
    evaluate_image(random_img)
