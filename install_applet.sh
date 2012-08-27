#!/bin/bash
DIR=$(pwd)/..
NORMAL="\\033[0;39m"
BLEU="\\033[1;34m"
VERT="\\033[1;32m" 
ROUGE="\\033[1;31m"

CURR_DATE=$((`date +%Y%m%d`+1))

CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH="cairo-dock-plug-ins-extras"
CAIRO_DOCK_PLUG_INS_EXTRAS_USR="/usr/share/cairo-dock/plug-ins/Dbus/third-party"
CAIRO_DOCK_PLUG_INS_EXTRAS_HOME="$HOME/.config/cairo-dock/third-party"

	mkdir -p "$CAIRO_DOCK_PLUG_INS_EXTRAS_HOME"

	# cd $DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH
	./make_locale.sh 0
	rm -rf locale.bak

	for i in `ls --hide=DOWNLOAD --hide=demos --hide=FTP "$DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH"`;do
		if test -d "$DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i"; then # only dir dossiers
			if test -e "$CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i" -a ! -L "$CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i" -a "$i" != "locale"; then
				echo -e "$ROUGE""This applet already exists on your third-party dir: $i"
				read -p "Do you want to use the latest version? (if you're using a custom version, please anwser 'n') [Y/n] " RM
				echo -e "$NORMAL"
				if [ "$RM" = "n" ] || [ "$RM" = "N" ] ; then
					continue
				fi
			fi
			echo -n $CURR_DATE > "$DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i/last-modif"
			rm -rf "$CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i"
			ln -s "$DIR/$CAIRO_DOCK_PLUG_INS_EXTRAS_LP_BRANCH/$i" "$CAIRO_DOCK_PLUG_INS_EXTRAS_HOME/$i" # symlinks
		fi
	done
