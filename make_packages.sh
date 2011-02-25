#!/bin/sh

# grab the list of applets to package from the list.conf.
list=`sed -n "/\[.*\]/p" list.conf | tr -d "[]"`

if test -d FTP; then
	echo "You have to remove FTP directory"
	exit 1
else
	mkdir FTP
	cp list.conf FTP
	for f in $list; do
		echo "make $f"
		# remove unwanted files.
		rm -f "$f/*.pyc" "$f/*~"
		
		# check that the version in noth .conf are identical.
		version1=`grep "^version *= *" "$f/auto-load.conf" | sed "s/.*= *//g"`
		version2=`head -1 "$f/$f.conf" | sed "s/.*;//g"`
		if test "$version1" != "$version2"; then
			echo "  Warning: versions mismatch for $f ($version1/$version2)"
		fi
		
		# build the tarball.
		tar cfz "$f.tar.gz" "$f" --exclude="last-modif" --exclude="preview.png"
		
		# place it in its folder.
		mkdir "FTP/$f"
		mv "$f.tar.gz" "FTP/$f"
	done;
fi

exit 0