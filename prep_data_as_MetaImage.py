# For converting dicom to MetaImage for use with AnnotationWeb

import numpy as np
# import PIL, PIL.Image
from pydicom import dcmread
from pathlib import Path
from common.metaimage import MetaImage
from dtd import autopatch
import cv2
import matplotlib.pyplot as plt
from auto_brightness_and_contrast import auto_bc_cv2, auto_bc_skimage
from skimage import transform, filters, exposure, util
from tqdm import tqdm

def window_data(image, return_mask=False):
    # Return a windowed portion of the data (i.e. bounding box)
    img_size = image.shape
    i0, i1 = int(img_size[0]//4), int(img_size[0]//(4/3))
    j0, j1 = int(img_size[1]//4), int(img_size[1]//(4/3))
    if not all(isinstance(x, int) for x in [i0,i1,j0,j1]):
        raise TypeError("Coordinates are not integers")
    else:
        if return_mask:
            image_mask = np.zeros_like(image, dtype=int)
            image_mask[i0:i1, j0:j1] = int(1)
            return image_mask
        else:
            return image[i0:i1, j0:j1]


def dcm_to_mhd(path_to_data, path_out, subject_id,
               recording_id=1, f_upscale=1, adjust=True):
    count = 0
    for f in path_to_data.glob('**/[!.]*'):
        count +=1
        frame = str(int(f.stem.split('_')[0])-1)
        dc = dcmread(f)
        # data = cv2.normalize(dc.pixel_array, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        data = cv2.convertScaleAbs(dc.pixel_array, alpha=255/dc.pixel_array.max())
        
        if adjust:
            # Automatically adjust contrast and brightness
            data_bb = window_data(data, return_mask=False)
            
            # ~~~~  scikit-image  ~~~~
            # data = util.img_as_ubyte(exposure.equalize_adapthist(data))
            # data = util.img_as_ubyte(exposure.equalize_hist(data, mask=data_bb))
            # data = auto_bc_skimage(data, clip_hist_percent=1)
            
            # ~~~~  OpenCV  ~~~~
            _, alpha, beta = auto_bc_cv2(data_bb, clip_hist_percent=2)
            data = cv2.convertScaleAbs(data, alpha=alpha, beta=beta)

        if np.issubdtype(type(f_upscale), int) and (f_upscale>int(0)):
            if f_upscale >= 2:
                data = util.img_as_ubyte(transform.rescale(data, scale=f_upscale, preserve_range=False, anti_aliasing=False))
                # data = data.repeat(f_upscale, axis=0).repeat(f_upscale, axis=1)
                # data = util.img_as_ubyte(filters.gaussian(data, sigma=1, preserve_range=False, truncate=1.0))
                dims = [np.divide(1, f_upscale) * ps for ps in dc.PixelSpacing]
            else:
                dims = dc.PixelSpacing
        else:
            raise TypeError("Scale factor is not an integer")

        im = MetaImage(data=data)
        im.set_spacing(dims)
        im.set_attribute("frames", frame)
        im.set_attribute("StudyID", dc["StudyID"].value)
        im.set_attribute("SeriesID", str(dc["SeriesNumber"].value))
        im.set_attribute("OriginalFileName", str(Path(*Path(dc.filename).parts[8:])))
        path_out_full = path_out.joinpath(
            f"MAD_{subject_id}/LA_4ch_{recording_id:d}/"
            # f"ProCardio/Projects/mad/data_processed/compare_autohist/{my_name}/MAD_{subject_id}/LA_fch_{recording_id:d}/"
            )
        path_out_full.mkdir(parents=True, exist_ok=True)
        im.write(filename=path_out_full.joinpath(f"frame_{frame}.mhd"))
        # cv2.imwrite(str(out_path.joinpath(f"frame_{int(frame):02d}.png")), data)


def main():
    data_paths = Path.home().joinpath("ProCardio/Projects/mad/data_raw/MAD_OUS_4ch/")
    # ~~~~~~~~~
    # my_name = "data-4ch_raw_us_auto"
    my_name = "test"
    # ~~~~~~~~~
    out_path = Path.home().joinpath(f"ProCardio/Projects/mad/data_processed/{my_name}")
    pbar = tqdm(sorted(data_paths.iterdir()))
    subj_no_4ch = []
    for subject_path in pbar:
        pbar.set_description(f"Processing MAD_{subject_path.stem}")
        subject = subject_path.stem
        path_4ch = subject_path.joinpath("4ch/")

        if not path_4ch.is_dir():
            subj_no_4ch.append(subject)
            # print(f"No 4ch data folder for subject {subject}.")
            continue

        if any(f.is_dir() for f in path_4ch.iterdir()):
            # iterate through folders
            folder_count = 0
            for series_path in sorted(path_4ch.iterdir()):
                dcm_to_mhd(series_path, out_path, subject, recording_id=folder_count, f_upscale=2, adjust=True)
                folder_count +=1
        else:
            dcm_to_mhd(path_4ch, out_path, subject, f_upscale=2, adjust=True)
    if subj_no_4ch:
        print(f"No 4ch data for: {subj_no_4ch}")
    else:
        print("4ch folder found for each subject")


if __name__=='__main__':
    main()
    