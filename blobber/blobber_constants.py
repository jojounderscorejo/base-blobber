SORT_IDX = [4, 0, 1, 5, 6, 2, 3, 7]

DEAFULT_PARAMS = {
    'xmin': 0,
    'xmax': 900,
    'ymin': 100,
    'ymax': 'max',
    
    'blob_log_min_sigma': 5,
    'blob_log_max_sigma': 10,   
    'blob_log_overlap': 0.667, # Rayleigh Criterion
    
    'canny_sigma': 2.5,
    'canny_low_threshold': 0.1,
    'canny_high_threshold': 0.3,
    
    'hough_ellipse_accuracy': 20,
    'hough_ellipse_threshold': 20,
    'hough_ellipse_min_size': 100,
    
    'image_thresholding_percentile': 99,
    'blob_thresholding_percentile': 99,
}
