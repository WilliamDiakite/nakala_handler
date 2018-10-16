import pandas as pd
import datetime
import os

from ..settings import imgs


otherProps = {
    'Référence Num'                          : 'identifier',
    'Cote dossier /document Agate'           : 'identifier',
    "Identifiant Base des fds d'archives"    : 'identifier',
    'Auteurs secondaires'                    : 'contributor',
    'Editeur'                                : 'provenance',
    'Edition / lieu'                         : 'spatial',
    'Sujet / Nom Artiste princip.'           : 'subject',
    'Sujet / Autre nom artiste'              : 'subject',
    'Sujet / Titre expo.'                    : 'subject',
    'Sujet autre'                            : 'subject',
    'Support'                                : 'format',
    'Support  (titre per, cat…)'             : 'isPartOF'
}


class Document(object):

    def __init__(self, data, dossier, author=True):
        self.props = [
            {'title': data["Titre du doc. ou de l'œuvre"]},
            {'creator': None},
            {'created': data['Date ou chrono.']},
            {'type': None},
            {'nkl:dataFormat': 'JPEG'},
            {'format': data['Typologie doc']},
            {'issued': datetime.datetime.now().strftime('%Y-%m-%d')},
            {'modified': datetime.datetime.now().strftime('%Y-%m-%d')},
            {'nkl:inCollection': dossier[1]},
            {'publisher': 'www.archivesdelacritiquedart.org'}
        ]
        if author:
            otherProps['Nom du photogr.'] = 'contributor'
            self.props[1] = {'creator': data['Auteur principal']}
        else:
            otherProps['Auteur principal'] = 'contributor'
            self.props[1] = {'creator': data['Nom du photogr.']}

        if data['Typologie doc'] == 'Œuvre':
            self.props[3] = {'type': 'StillImage'}
        else:
            self.props[3] = {'type': 'Text'}


        self._getOtherProps(data, otherProps)
        self.files = self.__getFiles__(data)
        # self._getExtent(data, dossier)


    def write(self, dest):
        # Make archive as directory
        archive = dest + self.fileName + '/'
        os.mkdir(archive)

        # Write csv file
        fileName = archive + self.fileName + '.csv'
        with open(fileName, 'w') as f:
            f.write('Métadonnée, Valeur\n')
            for prop in self.props:
                key = list(prop.keys())[0]
                value = prop[key]
                f.write('{p},"{v}"\n'.format(p=key, v=value))

        # Add data files (.png) to directory
        for f in m.files:
            s = imgs + f
            if os.path.isfile(s):
                copyfile(s, outfpath+f)
            else:
                e = imgs + f
                print('[ ! ] the following image was not found >', e, '')

        shutil.make_archive(archive, 'zip', archive)
        shutil.rmtree(archive)


    def __getFiles__(self, data):
        return [f.strip() + '.jpg' for f in data['Référence Num'].split('/')]


    def _getOtherProps(self, data, otherProps):
        for p in otherProps:
            if pd.notnull(data[p]):

                if p == 'Référence Num':
                    # Add all refeencies as identifiers
                    for i in data['Référence Num'].split('/'):
                        self.props.append({'identifier': i.strip()})

                    # Construct metadata fileName from references
                    filename = data['Référence Num'].split('/')[0]
                    filename = filename.split('_')[:4]
                    filename = '_'.join(filename)
                    self.fileName = filename


                elif (otherProps[p] == 'subject' or otherProps[p] == 'contributor'):
                    if ';' in data[p]:
                        for s in data[p].split(';'):
                            self.props.append({otherProps[p]: s.strip()})
                    elif '-' in data[p] :
                        for s in data[p].split('-'):
                            self.props.append({otherProps[p]: s.strip()})

                else:
                    self.props.append({otherProps[p]: data[p]})






    # def _getExtent(self, data, dossier):
    #     '''
    #     Ajout du tag extent (taille de la ressource)
    #     '''
    #     folder = '../../numerisations/GARCH_dossiers_monographiques/'
    #     folder = folder + dossier[1] + '/'
    #
    #     if dossier == 'unknownFolder':
    #         self.props.append({'extent': 'unknownFolder'})
    #         return
    #
    #     extent = 0
    #     for file in data['Référence Num'].split('/'):
    #         fileName = file.strip() + '.jpg'
    #         filePath = folder + fileName
    #
    #         if os.path.isfile(filePath):
    #             extent += os.path.getsize(filePath)
    #         else:
    #             self.props.append({'extent': 'FileNotFound'})
    #
    #         self.props.append({'hasPart': fileName})
    #     self.props.append({'extent': extent})
