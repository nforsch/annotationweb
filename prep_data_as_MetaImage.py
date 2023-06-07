# For converting dicom to MetaImage for use with AnnotationWeb

import numpy as np
# import PIL, PIL.Image
from pydicom import dcmread
from pathlib import Path
from common.metaimage import MetaImage
from dtd import autopatch
import cv2

def dcm_to_mhd(path_to_data, subject_id, recording_id=1, upscale=True, f_upscale=2):
    for f in path_to_data.glob('**/[!.]*'):
        print(f)
        frame = f.stem.split('_')[0]
        dc = dcmread(f)
        # data = cv2.normalize(dc.pixel_array, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        data = cv2.convertScaleAbs(dc.pixel_array)
        # data = dc.pixel_array.astype(np.uint8)
        if upscale:
            data = data.repeat(2, axis=0).repeat(2, axis=1)
            dims = [np.divide(1, f_upscale) * ps for ps in dc.PixelSpacing]
        else:
            dims = dc.PixelSpacing

        im = MetaImage(data=data)
        im.set_spacing(dims)
        im.set_attribute("frames", frame)
        out_path = Path(f"data_test_us_2/MAD_{subject_id}/LA_fch_{recording_id:d}/")
        out_path.mkdir(parents=True, exist_ok=True)
        im.write(filename=out_path.joinpath(f"frame_{frame}.mhd"))


def main():
    data_paths = Path("/Users/nick/ProCardio/Projects/mad/data_raw/MAD_OUS_sorted/")
    for subject_path in sorted(data_paths.iterdir()):
        subject = subject_path.stem
        path_4ch = subject_path.joinpath("cine/4ch/")

        if not path_4ch.is_dir():
            print(f"No 4ch data folder for subject {subject}.")
            continue

        if any(f.is_dir() for f in path_4ch.iterdir()):
            # iterate through folders
            folder_count = 1
            for series_path in sorted(path_4ch.iterdir()):
                dcm_to_mhd(series_path, subject, recording_id=folder_count)
                folder_count +=1
        else:
            dcm_to_mhd(path_4ch, subject)

if __name__=='__main__':
    main()


# ds = dcmread(path)
# data = ds.pixel_array
# dims = ds.PixelSpacing
# print(f'The image has {data.shape[0]} x {data.shape[1]} voxels')
# bigger_data = data.repeat(2, axis=0).repeat(2, axis=1)
# im = MetaImage(data=data)
# im.set_spacing(dims)
# im.set_attribute("frames", num_frames)
# im.write(filename="data/test.mhd")
# breakpoint()