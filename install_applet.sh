#!/bin/bash
DIR=$(pwd)/..
NORMAL="\\033[0;39m"
BLEU="\\033[1;34m"
VERT="\\033[1;32m" 
ROUGE="\\033[1;31m"

CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH="cairo-dock-plug-ins-extras"
CAIRO_DOCK_PLUG_INS_EXTRAS_USR="/usr/share/cairo-dock/plug-ins/Dbus/third-party"
CAIRO_DOCK_PLUG_INS_EXTRAS_HOME="$HOME/.config/cairo-dock/third-party"

	mkdir -p $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME

	rm -rf $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif
	mkdir $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif
	rm -rf $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/po

	# cd $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH
	./make_locale.sh 0

	for i in `ls --hide=DOWNLOAD --hide=demos --hide=FTP --hide=tmp_last_modif --hide=po $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH`;do
		if test -d $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i; then # only dir dossiers
			if test -f $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i/last-modif ;then # backup of last-modif's files
				mkdir $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif/$i
				cp $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i/last-modif $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif/$i/last-modif
			fi
			rm -rf $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i
			ln -s $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i # symlinks
			# cp ln -s $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i
			if test -f $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif/$i/last-modif ;then # backup of last-modif's files
				cp $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif/$i/last-modif $CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i/last-modif
			fi
		fi
	done
	rm -rf $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/tmp_last_modif

	if [ $? -ne 0 ]; then
		ERROR+=1
		echo -e "$ROUGE""\tError""$NORMAL"
	else
		echo -e "$VERT""\tSuccessfully Installed !""$NORMAL"
	fi
