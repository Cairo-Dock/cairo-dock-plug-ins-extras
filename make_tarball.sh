#!/bin/bash

read -p "What's the version? (e.g. 3.0.0) " VERSION
NAME="cairo-dock-plug-ins-extras"

FULLNAME="${NAME}_${VERSION}"

# grab the list of applets to package from the list.conf.
list=`sed -n "/^\[.*\]/p" list.conf | tr -d "[]"`

if test -e "$FULLNAME"; then
	echo "You have to remove this directory: $FULLNAME"
	exit 1
else
	mkdir "$FULLNAME"
	for f in $list; do
		test ! -e "$f/auto-load.conf" && continue

		echo "make $f"
		# remove unwanted files.
		rm -f "$f/*.pyc" "$f/*~"

		# check that the version in both .conf are identical.
		version1=`grep "^version *= *" "$f/auto-load.conf" | sed "s/.*= *//g"`
		version2=`head -1 "$f/$f.conf" | tr -d "#"`
		if test "$version1" != "$version2"; then
			echo "  Warning: versions mismatch for $f ($version1/$version2)"
		fi

		# copy to the directory
		cp -r "$f" "$FULLNAME"

		# remove a few files
		rm -f "$FULLNAME/$f/last-modif" "$FULLNAME/$f/preview.png"
		rm -f "$FULLNAME/$f/*.pyc" "$FULLNAME/$f/*~"
	done

	./make_locale.sh 2 "$FULLNAME"

	tar czf "$FULLNAME".tar.gz "$FULLNAME"

	curr_date=$(date -d "6 months" +%Y%m%d)

	# python2
	cd $FULLNAME
	for i in `cat ../Applets-python2.list`; do 
		if [ -x $i/$i ]; then
			sed --follow-symlinks -i "1s/python/python2/"  $i/$i
		fi
		# avoid update
		echo -n ${curr_date} > $i/last-modif
	done
	cd ..
	tar czf "$FULLNAME"_python2.tar.gz "$FULLNAME"

	# end
	rm -r "$FULLNAME"
	echo -e "These tarballs are available:\n\t* $FULLNAME.tar.gz\n\t* ${FULLNAME}_python2.tar.gz"

	read -p "Do you want to sign these tarballs? (Y/n) " SIGN
	if [ "$SIGN" != "n" ] && [ "$SIGN" != "N" ] ; then
		gpg --armor --sign --detach-sig "$FULLNAME.tar.gz"
		gpg --armor --sign --detach-sig "${FULLNAME}_python2.tar.gz"
	fi
fi

exit 0
