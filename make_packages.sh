#!/bin/bash

# grab the list of applets to package from the list.conf.
list=`sed -n "/^\[.*\]/p" list.conf | tr -d "[]"`

if test -d FTP; then
	echo "You have to remove FTP directory"
	exit 1
else
	mkdir FTP
	cp list.conf FTP
	for f in $list; do
		test ! -e "$f/auto-load.conf" && continue
		
		echo "make $f"
		# remove unwanted files.
		rm -f "$f/*.pyc" "$f/*~"
		
		# check that the version in noth .conf are identical.
		version1=`grep "^version *= *" "$f/auto-load.conf" | sed "s/.*= *//g"`
		version2=`head -1 "$f/$f.conf" | tr -d "#"`
		if test "$version1" != "$version2"; then
			echo "  Warning: versions mismatch for $f ($version1/$version2)"
		fi
		
		# build the tarball.
		tar cfz "$f.tar.gz" "$f" --exclude="last-modif" --exclude="preview.png"
		
		# place it in its folder.
		mkdir "FTP/$f"
		mv "$f.tar.gz" "FTP/$f"
	done;
	
	# build language tree
	f="locale"
	name="cairo-dock-plugins-extra"
	echo "make $f"
	mkdir $f
	
	for p in po/*.po; do
		pofile=${p:3}
		lang=${pofile/.po/}  # filtrer "en" ?...
		mkdir -p $f/${lang}/LC_MESSAGES
		msgfmt -o $f/${lang}/LC_MESSAGES/${name}.mo $p
	done;
	
	tar cfz "$f.tar.gz" $f
	mkdir "FTP/$f"
	mv "$f.tar.gz" "FTP/$f"
	rm -rf $f
fi

exit 0
