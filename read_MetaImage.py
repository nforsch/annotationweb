# For analyzing the export of AnnotationWeb (MetaImage)

import numpy
import matplotlib.pyplot as plt

from common.metaimage import MetaImage

fn = "/Users/nick/ProCardio/Projects/mad/code/annotationweb/data_test/MAD_3/LA_fch_1/frame_0.mhd"
# im = MetaImage(filename="/Users/nick/ProCardio/Projects/mad/MAD_demo/MAD2/LA_demo_2/frame_7_gt.mhd")
im = MetaImage(filename=fn)
pixels = im.get_pixel_data()

# mv_insert = pixels == 1

plt.imshow(pixels)
plt.show()
