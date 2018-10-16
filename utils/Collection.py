import shutil
import os


class Collection(object):
    def __init__(self, name, provenance, creator, inCollection):
        if name == '':
            print()
        self.fileName = name + '.xml'
        self.provenance = provenance
        self.creator = creator
        self.name = name
        self.inCollection = inCollection

    def write(self, dest):
        content = """
            <nkl:Collection
            xmlns:nkl="http://nakala.fr/schema#"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xsi:schemaLocation="http://purl.org/dc/terms/
            http://dublincore.org/schemas/xmls/qdc/2008/02/11/dcterms.xsd">
                <dcterms:title>{t}</dcterms:title>

                <dcterms:provenance>{p}</dcterms:provenance>

                <dcterms:creator>{c}</dcterms:creator>

                <nkl:inCollection>{i}</nkl:inCollection>

            </nkl:Collection>
        """.format(t=self.name, p=self.provenance,
                   c=self.creator, i=self.inCollection)


        archive = dest + self.name + '/'
        os.mkdir(archive)

        filename = archive+self.fileName + '.xml'
        with open(filename, 'w') as f:
            f.write(content)

        shutil.make_archive(archive, 'zip', archive)
        shutil.rmtree(archive)
