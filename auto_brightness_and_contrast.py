import cv2
import numpy as np
from matplotlib import pyplot as plt
from pydicom import dcmread
from pathlib import Path
from common.metaimage import MetaImage
from skimage import io, exposure, data
from dtd import autopatch

# Automatic brightness and contrast optimization with optional histogram clipping
def auto_bc_cv2(image, clip_hist_percent=1):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = image
    # plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    # cv2.imwrite("original.png", gray)
    
    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    
    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    
    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.figure(figsize=(2,6))
    plt.hist(hist,256,[0,256])
    plt.hist(new_hist,256,[0,256])
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

def auto_bc_skimage(image, clip_hist_percent=1):
    percentiles = np.percentile(image, (clip_hist_percent, 100-clip_hist_percent))
    auto_result = exposure.rescale_intensity(image,
                                             in_range=tuple(percentiles))
    return auto_result


f_mhd = Path(
    "/Users/nick/ProCardio/Projects/mad/data_processed/data-4ch_test_raw/MAD_1/LA_fch_1/frame_0.mhd"
    )
f_dcm = Path(
    "/Users/nick/ProCardio/Projects/mad/data_raw/MAD_OUS_sorted/1/cine/4ch/1_sliceloc_-12.7_triggertime_0.0"
)

# image = dcmread(f_dcm).pixel_array
# image = MetaImage(filename=f_mhd).data[40:150,70:180]

# auto_result, alpha, beta = automatic_brightness_and_contrast(image)
# print('alpha', alpha)
# print('beta', beta)
# plt.imshow(auto_result)
# plt.show()
# cv2.imshow('auto_result', auto_result)
# cv2.imwrite("auto_adjust.png", auto_result)
# cv2.waitKey()