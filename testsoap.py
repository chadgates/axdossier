import logging
import os

from suds.client import Client
from suds.transport.https import WindowsHttpAuthenticated
from suds.sax.text import Raw
import suds

filename = 'DossierTable.xml'
user = os.environ['user']
pw = os.environ['password']

with open(filename, "r") as myfile:
    xmlfilecontent=myfile.read()

logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


ntlm = WindowsHttpAuthenticated(username=user, password=pw)

client = Client(
    'http://srvwinaos01.commodity.loc:8080/MicrosoftDynamicsAXAif60/COMMODAxdDossierImportServiceGroupWEB/xppservice.svc?wsdl',
    transport=ntlm)

client.set_options(port='BasicHttpBinding_COMMODAxdDossierImportService')

try:
    keys = client.service.create(Raw(xmlfilecontent))
    if keys:
        try:
            dossier = client.service.read(keys)
            if len(dossier.dossierTable) == 1:
                print(dossier.dossierTable[0].DossierId)
            else:
                if len(dossier.dossierTable) == 0:
                    print("no dossier created")
                else:
                    print("multiple dossiers created, check AX")

        except suds.WebFault as detailnoread:
            print("HERE IS ANOTHER ERROR THAT I CAUGHT")
            print(detailnoread)

except suds.WebFault as detailnocreate:
    print (detailnocreate)



