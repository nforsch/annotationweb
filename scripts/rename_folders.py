from pathlib import Path, PurePath
import shutil
from dtd import autopatch

main_path = Path.home().joinpath("ProCardio/Projects/mad/data_raw/MAD_OUS_4ch")

for subject_path in main_path.iterdir():
    subject = subject_path.stem
    # Path(subject_path, "4ch").mkdir(parents=True, exist_ok=True)
    count = 0
    for series_path in subject_path.iterdir():
        series = series_path.stem
        for dcm_file in series_path.iterdir():
            destination = Path(subject_path, "4ch", f"LA_4ch_{count}", dcm_file.stem)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dcm_file, destination)
        shutil.rmtree(series_path)