import os
import pandas as pd
import xml.etree.cElementTree as ElementTree

from shutil import rmtree, copyfile, make_archive
from collections import defaultdict

from utils.prepare import prepare
from utils.Document import Document
from utils.Collection import Collection

from settings import fonds_name, fonds_handler, src

from console.execute import nakalaPush



def resetDir(dir):
    if os.path.isdir(dir):
        rmtree(dir)
    os.mkdir(dir)


dest= 'console/input/'
data = prepare(src)


######################################################
#--- Envoie des collections secondaires (dossier) ---#
######################################################

for dossier, grp in data.groupby('dossier'):
    if dossier == '':
        continue
    # Create collection file
    c = Collection(name=dossier,
                    creator='www.archivesdelacritiquedart.fr',
                    provenance=fonds_name,
                    inCollection=fonds_handler)
    c.write(dest)
    break


###########################################
#--- Envoie des collections sur NAKALA ---#
###########################################

nakalaPush()

#################################################
#--- Récupération des handler de collections ---#
#################################################

output_dir = 'console/output/ok/'
if os.path.isdir(output_dir):
    collections_handler = dict()

    print('[ + ] Retrieved the folling collections')
    for f in [f if f.endswith('.xml') for f in os.listdir(output_dir)]:
        e = ElementTree.parse(os.path.join(output_dir, f)).getroot()

        c_handler = e.find('identifier').get()
        c_name = f.replace('.xml', '')
        collections_handler[c_name] = c_handler

        print('\tCollection: {n}\t\tHandler: {h}'.format(n=c_name, h=c_handler))

############################
#--- Envoie des données ---#
############################

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
