import os
import pandas as pd
import zipfile

from shutil import rmtree, copyfile, make_archive
from prepare import prepare
from collections import defaultdict

from Document import Document
from Collection import Collection


folders = {
    'PAGU': 'GARCH_01_PAGU/',
    'EBAL': 'GARCH_02_EBAL/',
    'DBOE': 'GARCH_03_DBOE/',
    'LCOH': 'GARCH_04_LCOH/',
    'LDON': 'GARCH_05_LDON/',
    'FKIL': 'GARCH_06_FKIL/',
    'FPAR': 'GARCH_07_FPAR/',
    'ESAM': 'GARCH_08_ESAM/',
    'ESAm': 'GARCH_08_ESAM/',
    'TSHA': 'GARCH_09_TSHA/',
    'GTHO': 'GARCH_10_GTHO/',
    'RVEN': 'GARCH_11_RVEN/',
    'CWOO': 'GARCH_12_CWOO/'
}


def resetDir(dir):
    if os.path.isdir(dir):
        rmtree(dir)
    os.mkdir(dir)


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


imgs = '../../numerisations/GARCH_dossiers_monographiques/'
src = '../../index/cleaned/cleaned_2018_09_27.csv'
dest= '../../nakala/input/'
data = prepare(src)

imgCount = defaultdict(lambda: 0)
i = 0

for dossier, grp in data.groupby(['dossier', 'dossier_ref']):
    dossier = list(dossier)
    if not dossier[0] in folders:
        continue

    # Create colleciton file
    c = Collection(name=dossier[1],
                   creator='www.archivesdelacritiquedart.fr',
                   provenance="Galerie des Archives",
                   inCollection="11280/8a6bd898")
    cpath = dest + dossier[1] + '/'
    resetDir(cpath)
    c.write(cpath + dossier[1] + '.xml')
    make_archive(cpath, 'zip', cpath)
    rmtree(cpath)
    continue

    # Iterate through all documents in folder
    for _, doc in grp.iterrows():

        if doc['Auteur principal']:
            m = Document(doc, dossier)

        if doc['Nom du photogr.']:
            m = Document(doc, dossier, author=False)

        # Create/empty dir to store files
        outfpath = dest + str(i) + '/'
        resetDir(outfpath)

        # Store metadata in outfpath
        m.write(outfpath)

        # Copy image files in outfpath
        ipath = imgs + folders[dossier[0]]
        for f in m.files:
            s = ipath + f
            if os.path.isfile(s):
                copyfile(s, outfpath+f)
            else:
                e = imgs + f
                print('[ ! ] the following image was not found >', e, '')


        # Compress and remove outfpath
        make_archive(outfpath, 'zip', outfpath)
        rmtree(outfpath)
        i += 1
