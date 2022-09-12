import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.feature import canny, blob_log
from skimage.transform import hough_ellipse
from skimage.draw import ellipse, ellipse_perimeter
from joblib import Parallel, delayed
from .blobber_constants import SORT_IDX, DEAFULT_PARAMS


def initiateUserParams():
    return DEAFULT_PARAMS


def openImage(file_name):
    return np.array(Image.open(file_name))


def normaliseImage(data):
    return (data-np.min(data))/(np.max(data)-np.min(data))


def removeBoarder(data, global_params=DEAFULT_PARAMS):
    xmin = global_params['xmin']
    xmax = global_params['xmax']
    ymin = global_params['ymin']
    ymax = global_params['ymax']
    if xmax == 'max':
        xmax = data.shape[0]
    if ymax == 'max':
        ymax = data.shape[1]
    return data[xmin:xmax, ymin:ymax] 


def imageSplit(image):
    images_stack = []
    x_sep       = int(np.round(image.shape[0]/2))
    y_sep       = int(np.round(image.shape[1]/4))
    for i in range(2):
        for j in range(4):
            x_min = i*x_sep
            x_max = (i+1)*x_sep
            y_min = j*y_sep
            y_max = (j+1)*y_sep
            frame = image[x_min:x_max, y_min:y_max]
            images_stack.append(frame)
    return np.array(images_stack)[SORT_IDX]


def getPercentileValue(data, percentile=99):
    return np.percentile(data.flatten(), percentile)


def thresholdingImage(data, threshold):
    data_copy = data
    data_copy[data_copy < threshold] = 0
    return data_copy


def detectBlobs(data, blob_threshold, global_params=DEAFULT_PARAMS):
    dB_min_sigma     = global_params['blob_log_min_sigma']
    dB_max_sigma     = global_params['blob_log_max_sigma']
    dB_overlap       = global_params['blob_log_overlap']
    
    out = blob_log(data, min_sigma=dB_min_sigma, max_sigma=dB_max_sigma,\
                        threshold=blob_threshold, overlap=dB_overlap)
    return np.int32(out[:,1]), np.int32(out[:,0])    


def extractEllipseROI(image, global_params=DEAFULT_PARAMS):
    c_sigma             = global_params['canny_sigma']
    c_low_threshold     = global_params['canny_low_threshold']
    c_high_threshold    = global_params['canny_high_threshold']
    he_accuracy         = global_params['hough_ellipse_accuracy']
    he_threshold        = global_params['hough_ellipse_threshold']
    he_min_size         = global_params['hough_ellipse_min_size']
    
    edges = canny(image, sigma=c_sigma, low_threshold=c_low_threshold,\
                                        high_threshold=c_high_threshold)
    result = hough_ellipse(edges, accuracy=he_accuracy,\
                            threshold=he_threshold, min_size=he_min_size)
        
    result.sort(order='accumulator')
    best            = list(result[-1])
    yc, xc, a, b    = [int(round(x)) for x in best[1:5]]
    orientation     = best[5]
    return [yc, xc, a, b, orientation]


def parallelExtractEllipseROI(images_stack, global_params=DEAFULT_PARAMS):
    print("""
          Extracting ellipse from image, this process might take 1 to 10 minutes
          depending on your computer's performence. Please be patient. The estimated
          time will show soon.
          """)
    return Parallel(n_jobs=-1, verbose=10)(delayed(extractEllipseROI)\
                (images_stack[i,:,:], global_params) for i in range(8))

    
def getEllipseArea(ellipse_params):
    yc, xc, a, b, orientation = ellipse_params
    # imshow x, y are flipped
    y_imshow, x_imshow = ellipse(yc, xc, a, b, rotation=orientation)
    return np.array([x_imshow, y_imshow]).T


def generateMask(raw_image, global_params=DEAFULT_PARAMS):
    image = removeBoarder(raw_image, global_params)
    image = normaliseImage(image)
    images_stack = imageSplit(image)
    ellipse_params = parallelExtractEllipseROI(images_stack, global_params)
    masks_stack = []
    for i in range(8):
        pos  = getEllipseArea(ellipse_params[i])
        mask = np.zeros(images_stack[i,:,:].shape)
        x_im = pos[:,0]
        y_im = pos[:,1]
        mask[y_im, x_im] = 1
        masks_stack.append(mask)
    return masks_stack, ellipse_params


def showMaskedBlobs(raw_image, masks_stacks, ellipse_params,\
                                global_params=DEAFULT_PARAMS):
    
    param_ITP = global_params['image_thresholding_percentile']
    param_BTP = global_params['blob_thresholding_percentile']
    
    image = removeBoarder(raw_image, global_params)
    images_stack = imageSplit(image)
    
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True,\
                                    dpi=150, tight_layout=True)
    for i in range(8):
        yc, xc, a, b    = np.int16(ellipse_params[i][:-1])
        frame           = normaliseImage(images_stack[i])
        threshold_val   = getPercentileValue(frame, param_ITP)
        frame           = thresholdingImage(frame, threshold_val)
        blob_threshold  = getPercentileValue(frame, param_BTP)
        x, y            = detectBlobs(frame, blob_threshold, global_params)
        blob_pos        = np.zeros(frame.shape)
        blob_pos[y, x]  = 1
        blob_masked     = blob_pos*masks_stacks[i]
        in_y, in_x      = np.nonzero(blob_masked)
        
        orientation     = ellipse_params[i][-1]
        cy, cx          = ellipse_perimeter(yc, xc, a, b, orientation)
        
        if i <= 3:
            axes[0, i].plot(cx, cy, 'p', markersize=0.05)
            axes[0, i].imshow(frame, 'hot')
            axes[0, i].plot(in_x, in_y, marker='o', markersize=7,\
                            linestyle="None", fillstyle='none', color='green')
            axes[0, i].plot(x, y, 'bx', markersize=1)
            axes[0, i].axis('off')
            axes[0, i].text(0, 30, f'Frame {i}', color='white')
        elif 3 < i <=7:
            j = i-4
            axes[1, j].plot(cx, cy, 'p', markersize=0.05)
            axes[1, j].imshow(frame, 'hot')
            axes[1, j].plot(in_x, in_y, marker='o', markersize=7,\
                            linestyle="None", fillstyle='none', color='green')
            axes[1, j].plot(x, y, 'bx', markersize=1)
            axes[1, j].axis('off')
            axes[1, j].text(0, 30, f'Frame {i}', color='white')
    plt.show()        


def showBlobsWithFrame(raw_image, framing_image, global_params=DEAFULT_PARAMS):
    param_ITP = global_params['image_thresholding_percentile']
    param_BTP = global_params['blob_thresholding_percentile']
    
    image           = removeBoarder(raw_image, global_params)
    images_stack    = imageSplit(image)
    frame           = removeBoarder(framing_image, global_params)
    frames_stack    = imageSplit(frame)
    
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True,\
                                    dpi=150, tight_layout=True)
    for i in range(8):
        frame           = normaliseImage(images_stack[i])
        threshold_val   = getPercentileValue(frame, param_ITP)
        frame           = thresholdingImage(frame, threshold_val)
        blob_threshold  = getPercentileValue(frame, param_BTP)
        x, y            = detectBlobs(frame, blob_threshold, global_params)
        blob_pos        = np.zeros(frame.shape)
        blob_pos[y, x]  = 1
        
        if i <= 3:
            axes[0, i].imshow(frames_stack[i], 'gray')
            axes[0, i].imshow(images_stack[i], 'hot', alpha=0.6)
            axes[0, i].plot(x, y, marker='o', markersize=7,\
                            linestyle="None", fillstyle='none', color='green')
            axes[0, i].axis('off')
            axes[0, i].text(0, 30, f'Frame {i}', color='white')
        elif 3 < i <=7:
            j = i - 4
            axes[1, j].imshow(frames_stack[i], 'gray')
            axes[1, j].imshow(images_stack[i], 'hot', alpha=0.6)
            axes[1, j].plot(x, y, marker='o', markersize=7,\
                            linestyle="None", fillstyle='none', color='green')
            axes[1, j].text(0, 30, f'Frame {i}', color='white')
            axes[1, j].axis('off')
    plt.show()
    
    
def showPixelHistogram(raw_image, global_params=DEAFULT_PARAMS):
    param_ITP = global_params['image_thresholding_percentile']
    param_BTP = global_params['blob_thresholding_percentile']
    
    image        = removeBoarder(raw_image, global_params)
    images_stack = imageSplit(image)
    
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True,\
                                    dpi=150, tight_layout=True)
    for i in range(8):
        if i <= 3:
            axes[0, i].hist(x=images_stack[i].flatten(), bins=64, log=True,\
                                                            range=[0, 4095])
            axes[0, i].set_title(f'Frame {i}')
        elif 3 < i <=7:
            j = i - 4
            axes[1, j].hist(x=images_stack[i].flatten(), bins=64, log=True,\
                                                            range=[0, 4095])
            axes[1, j].set_title(f'Frame {i}')
    plt.show()