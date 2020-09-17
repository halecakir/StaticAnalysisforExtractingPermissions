import os
import sys
from multiprocessing import Pool
import itertools

from AnalyzePermissions import run


def main(apks, out_dir):
    with Pool(processes=60) as pool:
        pool.starmap(run, itertools.product(apks,[out_dir]))

if __name__=="__main__":
    apk_dir = sys.argv[1]
    out_dir = sys.argv[2]
    apks = []
    for file in os.listdir(apk_dir):
        if file.endswith(".apk"):
            apks.append(os.path.join(apk_dir, file))
    main(apks, out_dir)
