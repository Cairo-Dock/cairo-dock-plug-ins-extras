#!/bin/bash

# build language tree
NEXT=$1 # 1 = packages => FTP | 2 = tarball => cairo-dock-plug-ins-extras_VERSION
DIR="$2"
f="locale"
name="cairo-dock-plugins-extra"
echo "make $f"

if test -e $f; then
	mv -v $f $f.bak
fi
mkdir $f

for p in po/*.po; do
	pofile=${p:3}
	lang=${pofile/.po/}  # filtrer "en" ?...
	mkdir -p $f/${lang}/LC_MESSAGES
	msgfmt -o $f/${lang}/LC_MESSAGES/${name}.mo $p
done;

if test $NEXT -eq 1; then
	tar cfz "$f.tar.gz" $f
	mkdir "FTP/$f"
	mv "$f.tar.gz" "FTP/$f"
	rm -rf $f
elif test $NEXT -eq 2 -a "$DIR" != ""; then
	mv $f "$DIR"
else
	echo "No end option"
fi
