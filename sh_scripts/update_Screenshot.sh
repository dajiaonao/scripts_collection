#!/bin/bash
# find . -name Screenshot.\*.png 
# for FILE in "$(find  . -type f -name Screenshot\*.png)"
# do
# 	echo $FILE
# x=`echo "$FILE"|sed 's/ /_/g'`
# echo "$FILE->$x"
# done
find . -type f -name 'Screenshot *.png' -print0 | while IFS= read -r -d '' file; do
#     printf '%s\n' "$file"
    echo "$file"
    x=`echo "$file"|sed 's/ /_/g'`
    echo "->$x"
    mv "$file" "$x"

    done
