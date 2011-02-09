#!/bin/sh
list=`sed -n "/\[.*\]/p" list.conf | tr -d "[]"`
if test -d FTP; then
	echo "Please remove FTP directory"
else
	mkdir FTP
	cp list.conf FTP
	for f in $list; do
		echo "make $f"
		rm -f "$f/*.pyc" "$f/*~"
		mkdir "FTP/$f"
		tar cfz --exclude=last-modif "$f.tar.gz" "$f"
		mv "$f.tar.gz" "FTP/$f"
	done;
fi
