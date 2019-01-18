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

#for dir in ./*/
#do
#    dir=${dir%*/}
#    echo ${dir##*/}
#done

# ALLJPGS=$(find . -type f -name '*.jpg')
# for fn in ${ALLJPGS};
# do
#     echo "${fn}"
# done

find . -type f -name '*.jpg' | while read path
do
    fn=$(basename -- "$path")
    dn=$(dirname "${path}")
    FN=${fn%%.*}
    #OUT="./ocrd/${dn}/${FN}.pdf"
    NEWDIR="./ocrd/${dn}/"
    OUT="${NEWDIR}/${FN}.pdf"
    mkdir -p "${NEWDIR}"
    img2pdf --pagesize A4 "${path}" | ocrmypdf --clean-final --deskew -l eng+deu - "${OUT}"
done
