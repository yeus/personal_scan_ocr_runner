#!/bin/sh
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

#search for multiple fil extensions:
#find . -type f \( -name "*.shtml" -or -name "*.css" \)

#user parallel

find . -type f -name '*.pdf' -not -path "*/ocrd/*" | while read path
do
    fn=$(basename -- "$path")
    dn=$(dirname "${path}")
    FN=${fn%%.*}
    #OUT="./ocrd/${dn}/${FN}.pdf"
    NEWDIR="./ocrd/${dn}/"
    OUT="${NEWDIR}/${FN}.pdf"
    mkdir -p "${NEWDIR}"
    echo "Filename: ${path}"
    if [ ! -f "${OUT}" ]; then
        echo "File not found! starting ocr process!"
        ocrmypdf --clean-final --deskew -l eng+deu "${path}" "${OUT}"
    else
        echo "File exists already!"
    fi
done

find . -type f -name \( -name "*.jpg" -or -name "*.JPG" -or -name "*.png" -or -name "*.PNG"\) -not -path "*/ocrd/*" | while read path
do
    fn=$(basename -- "$path")
    dn=$(dirname "${path}")
    FN=${fn%%.*}
    #OUT="./ocrd/${dn}/${FN}.pdf"
    NEWDIR="./ocrd/${dn}/"
    OUT="${NEWDIR}/${FN}.pdf"
    mkdir -p "${NEWDIR}"
    echo "Filename: ${path}"
    if [ ! -f "${OUT}" ]; then
        echo "File not found! starting ocr process!"
        img2pdf --pagesize A4 "${path}" | ocrmypdf --clean-final --deskew -l eng+deu - "${OUT}"
    else
        echo "File exists already!"
    fi
done


N=4
(
for thing in a b c d e f g; do 
   ((i=i%N)); ((i++==0)) && wait
   task "$thing" & 
done
)
