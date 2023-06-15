# import os
from pathlib import Path
from dtd import autopatch

p = Path("data").glob('**/[!.]*')
files = [x for x in p if x.is_file()]
breakpoint()

for subject_path in Path("data").iterdir():
    subject = subject_path.stem
    for sequence_path in subject_path.iterdir():
        sequence = sequence_path.stem
        img_list = sorted(list(sequence_path.iterdir()))
        # seq_int = range(len(img_list))
        for idx, img in enumerate(img_list):
            img.rename(img.parent.joinpath(f"frame_{idx}.png"))
breakpoint()