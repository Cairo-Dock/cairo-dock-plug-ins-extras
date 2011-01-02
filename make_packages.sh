#!/bin/sh
list=`sed -n "/\[.*\]/p" list.conf | tr -d "[]"`
for f in $list; do
	echo "make $f"
	tar cfz "$f.tar.gz" "$f"
done;
