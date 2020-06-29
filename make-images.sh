#!/usr/bin/env bash

set -ex

for size in {400..2400..100}
do
  magick af_gang_mail/static/background.original.jpg -resize "$size" -quality 25% "af_gang_mail/static/background-w-$size.jpg"
done

for size in {500..3000..100}
do
  magick af_gang_mail/static/background.original.jpg -resize "x$size" -quality 25% "af_gang_mail/static/background-h-$size.jpg"
done

find . -iname "*.original.jpg" -o -iname "*.original.png"|while read -r infile; do
  outfile=${infile/.original/}
  outfile=${outfile/.png/.jpg}
  magick "$infile" -quality 70% "$outfile"
done
