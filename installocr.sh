sudo apt install tesseract-ocr gimagereader yagf lios aspell-de hunspell-de-de tesseract-ocr-deu exactimage

#install pdf ocr
#cd /tmp
#wget -O pdfsandwich.deb https://downloads.sourceforge.net/project/pdfsandwich/pdfsandwich%200.1.6/#pdfsandwich_0.1.6_amd64.deb?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fpdfsandwich%2Ffiles%2F&ts=1501595848&use_mirror=kent
#sudo dpkg -i pdfsandwich.deb  # There will be an error message. Ignore it and proceed!

sudo apt install pdfsandwich  #in case 
sudo apt install -y img2pdf ocrmypdf  #preferred solution right now 

