from funcs import *
import numpy as np
CSV = "images/LAB_color_list.csv"

def predict(query_name):
    topn=5
    lab_list, color_name = load_lab_csv_list(CSV)
    print('load image file is ', query_name)
    bgr = cv2.imread(query_name)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    #plt.imshow(rgb),plt.show()
    
    dim2rgb = rgb.reshape(-1,3)
    lab_colors = extract_topN_color(dim2rgb, num_clusters = topn, plot=None)
    
    c1, c2, c3, _, _ = get_topn_lab(lab_colors[0].tolist())
    top1,top2,top3 = get_topn_color(color_name, lab_list, c1, c2, c3)
    print('main_color1 {}, main_color2 {}, main_color3 {}'.format(top1,top2,top3))
    return top1, top2, top3


#if __name__ == '__main__':
    #top1, top2, top3 = predict(query_name)
    #print(top1[0][1], top2, top3)
