import os
from multiprocessing import Pool

from AnalyzePermissions import run


def main(apks):
    with Pool(processes=30) as pool:
        pool.map(run, apks)

if __name__=="__main__":
    apk_dir = "/data/huseyinalecakir_data/Downloads_All"
    apks = []
    for file in os.listdir(apk_dir):
        if file.endswith(".apk"):
            apks.append(os.path.join(apk_dir, file))

    main(apks)
