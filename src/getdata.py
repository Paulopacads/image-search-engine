import wget
import tarfile
import os
import shutil

print('#### INITIALIZING DATA DOWNLOAD ####')
data = "./static/data/"
URL1 = "ftp://ftp.inrialpes.fr/pub/lear/douze/data/jpg1.tar.gz"
URL2 = "ftp://ftp.inrialpes.fr/pub/lear/douze/data/jpg2.tar.gz"
if os.path.exists(data):
    shutil.rmtree(data)
os.makedirs(data)

print('- Downloading first data pack')
wget.download(URL1, data + "file.tar.gz")

print('\n- Extracting data pack')
file = tarfile.open(data + "file.tar.gz")
file.extractall(data)
file.close()

print('- Removing data pack\n')
os.remove(data + "file.tar.gz")

print('- Downloading second data pack')
wget.download(URL2, data + "file.tar.gz")

print('\n- Extracting data pack')
file = tarfile.open(data + "file.tar.gz")
file.extractall(data)
file.close()

print('- Removing data pack')
os.remove(data + "file.tar.gz")

print('#### DATA DOWNLOADED ####')