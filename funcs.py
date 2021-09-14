import collections
import pandas as pd
import os
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage.color import rgb2lab
import cv2

def load_lab_csv_list(lab_list_name):
    dic = OrderedDict()
    color = pd.read_csv(lab_list_name).drop("Unnamed: 0", axis=1)
    for i,v in color.iterrows():
        dic[v[0],v[1]]=np.array([v['L'],v['A'],v['B']])
    lab_list, color_name =list(dic.values()), list(dic.keys())
    return lab_list, color_name


def extract_topN_color(two_dim_img, num_clusters = 5, plot=None):
    def centroid_histogram(clt):
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins = numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()
        return hist
  
    def plot_colors(hist, centroids):
        bar = np.zeros((50, 300, 3), dtype = "uint8")
        startX = 0
        for (percent, color) in zip(hist, centroids):
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX
        return bar
    clt = KMeans(n_clusters = num_clusters)
    clt.fit(two_dim_img)
    hist = centroid_histogram(clt)
    main_rgb_colors = plot_colors(hist, clt.cluster_centers_)
    if plot:
        plt.figure()
        plt.imshow(main_rgb_colors),plt.show()
    return rgb2lab(main_rgb_colors), main_rgb_colors

def get_topn_lab(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]


def get_topn_color(color_name, lab_list, c1, c2, c3):
    def lab_distance_dic(n_color):
        dics = OrderedDict()
        for name,lab_value in zip(color_name, lab_list):
            dics[name]=np.linalg.norm(lab_value - n_color)
        return dics

    def return_topn_color(n_color):
        dic_n = lab_distance_dic(n_color)
        return [k for k, v in dic_n.items() if v == min(dic_n.values())]

    top1_color = return_topn_color(c1)
    top2_color = return_topn_color(c2)
    top3_color = return_topn_color(c3)
    return top1_color, top2_color, top3_color
