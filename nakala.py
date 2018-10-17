import os
import pandas as pd
import xml.etree.cElementTree as ET
import xmltodict

from shutil import rmtree, copyfile, make_archive
from collections import defaultdict

from utils.prepare import prepare
from utils.Document import Document
from utils.Collection import Collection

from settings import fonds_name, fonds_handler, src, imgs

from console.execute import nakalaPush



####################################
#--- HELPERS & GLOBAL VARIABLES ---#
####################################

def resetDir(dir):
    if os.path.isdir(dir):
        rmtree(dir)
    os.mkdir(dir)


def check_logs(logPath='./console/output/'):
    errors = dict()
    for f in os.listdir(logPath):
        if 'report' in f:
            # parse log file
            report = ET.parse(logPath + f).getroot()

            # Get general stats
            nb_valid = report.find('nb_files_valid').text
            nb_invalid = report.find('nb_files_invalid').text
            print('\n------- NAKALA REPORT -------\n')
            print('\t', nb_valid, 'valid file(s)')
            print('\t', nb_invalid, 'invalid file(s)')


            # Go through all invalid files and store error
            # for f in report['files_treated']:
            #     print(f)
            #     print('\n------------\n')



if __name__ == '__main__':

    # Location to store archives created from the archives' index
    dest = 'console/input/'

    # Load the data and clean some stuff
    data = prepare(src)


    ######################################################
    #--- Envoie des collections secondaires (dossier) ---#
    ######################################################

    for dossier, grp in data.groupby('dossier'):
        if dossier == '':
            dossier = 'unknown'

        # Create collection file
        c = Collection(name=dossier,
                        creator='www.archivesdelacritiquedart.fr',
                        provenance=fonds_name,
                        inCollection=fonds_handler)

        # Save the collection as zip archive
        c.write(dest)


    ###########################################
    #--- Envoie des collections sur NAKALA ---#
    ###########################################

    # Push data to NAKALA using jar provided by HumaNum
    nakalaPush()


    #################################################
    #--- Récupération des handler de collections ---#
    #################################################

    # NOTE: needs to deal with partial sending

    log_dir = 'console/output/ok/'
    if os.path.isdir(log_dir):
        collections_hdlr = dict()

        print('[ + ] Retrieved the folling collections')
        for f in [f for f in os.listdir(log_dir) if f.endswith('.xml')]:
            file = log_dir + f

            with open(file) as fd:
                # Parse returned xml files
                xml = xmltodict.parse(fd.read())

                # Retrive collection name and handler. Then store in dict
                c_handler = xml['nkl:Collection']['identifier']['#text']
                c_name = xml['nkl:Collection']['dcterms:title']
                collections_hdlr[c_name] = c_handler

                print('\t* collection: {n}\n\t  handler: {h}\n'.format(
                                                        n=c_name, h=c_handler))
    else:
        # If pushing data to NAKALA failed, no 'ok' directory is created
        print('\n[ ! ] It seems that their was a problem when pushing the data to NAKALA.')
        print('\tNo output data has been found.')
        print('\tSee report for more details.\n')


    ####################
    #--- Verify logs --#
    ####################

    check_logs()

    exit()


    #########################################################
    #--- Création des archives de données et métadonnées ---#
    #########################################################

    # init counter for archive name
    i = 0

    # Iterate through all documents in folder
    for dossier, grp in data.groupby('dossier'):
        for _, doc in grp.iterrows():

            if doc['Auteur principal']:
                m = Document(doc, dossier, imgs)

            if doc['Nom du photogr.']:
                m = Document(doc, dossier, imgs, author=False)

            # Create/empty dir to store files
            outfpath = dest + str(i) + '/'
            resetDir(outfpath)

            # Store metadata and data in nakala console input
            m.write(outfpath)

            i += 1

    nakalaPush()


    ####################
    #--- Verify logs --#
    ####################

    # ...
