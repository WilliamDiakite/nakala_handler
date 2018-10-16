from collections import defaultdict


class Base(object):

    def isAggregatedBy(self, Collection):
        self.props.append({'isAggregatedBy': Collection.uri})

        if self.type == 'dossier' and Collection.type=='fonds':
            self.props.append({'broader': Collection.uri})

        elif self.type == 'dossier' and Collection.type=='scheme':
            self.props.append({'inScheme': Collection.uri})

        elif self.type == 'fonds' and Collection.type=='scheme':
            self.props.append({'hasTopConcept': Collection.uri})


    def aggregates(self, object):
        self.props.append({'aggregates': object.uri})

        if self.type == 'fonds':
            self.props.append({'narrower': object.uri})

        if self.type == 'scheme':
            self.props.append({'isTopConcept': object.uri})


    def fromAgent(self, Agent):
        if self.type == 'scheme':
            self.props.append({'creator': Agent.uri})
        elif self.type == 'resource':
            self.props.append({'publisher': Agent.uri})


    def display(self):
        for k in self.props:
            print(k)

    def write(self, dest):
        fpath = dest + self.fileName
        with open(fpath, 'w') as f:
            f.write('Métadonnée, Valeur\n')
            for prop in self.props:
                key = list(prop.keys())[0]
                value = prop[key]
                f.write('{p},"{v}"\n'.format(p=key, v=value))
