opencv_createsamples -img main_img/$1* -bg bg_pos.txt -info info/info.lst -pngoutput info -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1 -num $2
# opencv_createsamples -img main_img/$1* -info bg_pos.txt -num $2 -w 24 -h 24 -vec positives.vec 

# $1 selected main image
# $2 positive number 