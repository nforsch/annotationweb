import matplotlib.pyplot as plt
from common.metaimage import MetaImage

img = MetaImage(filename="/Users/nick/ProCardio/Projects/mad/code/annotationweb/data_test/MAD_1/LA_4ch_01/frame_00.mhd")
pixels = img.get_pixel_data().reshape(192,256,2)
plt.imshow(pixels[...,0])
plt.imshow(pixels[...,1])
plt.show()