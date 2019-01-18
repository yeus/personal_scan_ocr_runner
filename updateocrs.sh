#!/bin/sh -x
#convert input.png -trim output.png
#find ./ -name "pattern" -exec convert {} -trim outputfolder/{} \;

#img2pdf --pagesize A4 page*.png | ocrmypdf - myfile.pdf

# for filename in *.jpg; 
# do
#   #echo "running: ocrmypdf --clean-final --deskew -l eng+deu --image-dpi 300 ./${filename#./} ./ocrd/${filename#./}"
#   #ocrmypdf --clean-final --deskew -l eng+deu --image-dpi 300 ./${filename#./} ./ocrd/${filename#./}
#   echo ${filename}
#   FN=${filename%%.*}
#   echo $FN
# #  img2pdf --pagesize A4 ${filename} | ocrmypdf --clean-final --deskew -l eng+deu --image-dpi 300 - "${FN}.pdf"
#   img2pdf --pagesize A4 ${filename} | ocrmypdf --clean-final --deskew -l eng+deu - "${FN}.pdf"
# #  ocrmypdf -c --clean-final --deskew -l eng+deu --image-dpi 300 ${filename} "${FN}.pdf"
# done

find 
