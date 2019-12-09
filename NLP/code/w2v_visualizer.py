# -*- coding: utf-8 -*-
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz
@version: 1.0
@license: Apache Licence
@file: w2v_visualizer.py
@time: 2017/7/30 上午9:37
"""
import sys
import os
import pathlib
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector


def visualize(model, output_path):
    
    data_num = 500

    meta_file = "w2x_metadata.tsv"
    placeholder = np.zeros((data_num, model.vector_size))

    with open(os.path.join(output_path, meta_file), 'wb') as file_metadata:
        for i, word in enumerate(model.wv.index2word):
            data_num = data_num - 1
            if data_num == -1:
                break
            placeholder[i] = model[word]
            # temporary solution for https://github.com/tensorflow/tensorflow/issues/9094
            if word == '':
                print("Emply Line, should replecaed by any thing else, or will cause a bug of tensorboard")
                file_metadata.write("{0}".format('<Empty Line>').encode('utf-8') + b'\n')
            else:
                file_metadata.write("{0}".format(word).encode('utf-8') + b'\n')

    # define the model without training
    sess = tf.InteractiveSession()

    embedding = tf.Variable(placeholder, trainable=False, name='w2x_metadata')
    tf.global_variables_initializer().run()

    saver = tf.train.Saver()
    writer = tf.summary.FileWriter(output_path, sess.graph)

    # adding into projector
    config = projector.ProjectorConfig()
    embed = config.embeddings.add()
    embed.tensor_name = 'w2x_metadata'
    embed.metadata_path = meta_file

    # Specify the width and height of a single thumbnail.
    projector.visualize_embeddings(writer, config)
    saver.save(sess, os.path.join(output_path, 'w2x_metadata.ckpt'))
    print('Run `tensorboard --logdir={0}` to run visualize result on tensorboard'.format(output_path))


if __name__ == "__main__":
    """
    Use model.save_word2vec_format to save w2v_model as word2evc format
    Then just run `python w2v_visualizer.py word2vec.text visualize_result`
    """
    try:
        #여기 경로 변경
        model_path = "/home/minheelee/NEWNLP/model/model30000_20_4"
        output_path = './log/'
    except:
        print("Please provice model path and output path")
    model = KeyedVectors.load(model_path)
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
    visualize(model, output_path)