#!/usr/bin/perl

# Rev 0.1
#
# tiny Url for Cairo-Dock / Glx-Dock
#
# Require : 
#	LWP::Simple
#	Clipboard
#	
#	To Install them :
#		#cpan -i LWP
#		#cpan -i Clipboard
#
# Todo :
#	Learn English
#	Create a GUI for external link
#	Use all the dnd2share link ( not the last )
#
# Copyright : (C) 2010 by ours_en_pluche
# E-mail : ours_en_pluche at hotmail ! fr
# Site : http://www.glx-dock.org
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# http://www.gnu.org/licenses/licenses.html#GPL

use strict;
use warnings;
use LWP::Simple;
use Clipboard;

my $db_showdialog = "org.cairodock.CairoDock /org/cairodock/CairoDock/ShortUrl org.cairodock.CairoDock.applet.ShowDialog";
my $db_asktext = "org.cairodock.CairoDock /org/cairodock/CairoDock/ShortUrl org.cairodock.CairoDock.applet.AskText";
my $db_populatemenu = "org.cairodock.CairoDock /org/cairodock/CairoDock/ShortUrl org.cairodock.CairoDock.applet.PopulateMenu";

my (%conf);
my ($c,$tiny,$title,$link,$menu) = ("","","","","");

sub load {
	open(FIC,"/home/".$ENV{USER}."/.config/cairo-dock/current_theme/plug-ins/ShortUrl/ShortUrl.conf") or print "can't read ShortUrl.conf";
	while(<FIC>) {
		if ( $_ =~ /^site_de_shortyurl=(.*)$/ ) {
			$conf{'url'} = $1;
		} elsif ( $_ =~ /^choix_clic_gauche=(.*)$/ ) {
			$conf{'left_clic'} = $1;
		} elsif ( $_ =~ /^choix_clic_milieu=(.*)$/ ) {
			$conf{'middle_clic'} = $1;
		}
	}
	close(FIC);
}

&load;

sub shorturllastdnd2share {
	open(FIC,"/home/".$ENV{USER}."/.config/cairo-dock/dnd2share/history.conf") or &errordnd2share;
	while(<FIC>) {
		if ( $_ =~ /^url0=(.*)$/ ) {
			$c = $1;
		}
	}
	&uploadurl($c);
	close(FIC);
	if ( $c eq "" ) {
		&errordnd2share
	}	
}

sub errordnd2share {
	`dbus-send --session --dest=$db_showdialog string:"Can't the history file of DND2Share applet" int32:2`;
	die "erreur, adresse web introuvable";
}

sub geturl {
	my $urlaminut = `dbus-send --session --dest=$db_asktext string:"Please write here your URL
in order to shorten it:" string:"http://"`;
}

sub uploadurl {
	my ($url) = @_;
	if ( $conf{'url'} eq "0" ) {
		&tinyurl($url);
	} elsif ( $conf{'url'} eq "1" ) {
		&shorterlink($url);
	}
}

sub createmenu {
	my $file = "/home/".$ENV{USER}."/.config/cairo-dock/third-party/ShortUrl/ShortyUrl.db";
	`rm -rf $file`;
	open(FIC,"/home/".$ENV{USER}."/.config/cairo-dock/dnd2share/history.conf") or &errordnd2share;
	while(<FIC>) {
		if ( $_ =~ /^url0=(.*)$/ ) {
			$link = $1;
		} elsif ( $_ =~ /^local\spath=(.*)$/ ) {
			$title = $1;
			$title =~ s/.*\///g;
		}
		if ( $link ne "" && $title ne "" ) {
			$menu = $menu.",\"".$title."\"";
			($link,$title) = ("","");
		}
	}
	close(FIC);
	`echo "$menu" | tee -a $file`;
	`dbus-send --session --dest=$db_populatemenu array:string:$menu`;
}

sub tinyurl {
	my ($url) = @_;
	my $d = $url;
	$url =~ s/:/%3A/g;
	$url =~ s/\//%2F/g;
	my $a = get("http://tinyurl.com/create.php?source=homepage&url=".$url."&submit=Make+TinyURL\!&alias=");
	my @tmp = split(/\n/,$a);
	foreach my $b (@tmp) {
		if ( $b =~ /.*<blockquote><b>(.*)<\/b><br><small>.*Open\sin\snew\swindow.*/ && $b !~ /.*preview.*/ ) {
			$tiny = $1;
			Clipboard->copy($tiny);
			my $mess = "Your tiny URL: $tiny
You can do a middle clic to paste it everywhere";
			`dbus-send --session --dest=$db_showdialog string:"$mess" int32:5`;
		}
	}
}

sub shorterlink {
	my ($url) = @_;
	my $d = $url;
	$url =~ s/:/%3A/g;
	$url =~ s/\//%2F/g;
	my $a = get("http://shorterlink.org/createlink.php?url=".$url);
	if ( $a =~ /.*<html><h3>Here\sis\syour\sshorter\slink:<\/h3><br><a href="(.*)">.*<\/><br><br><br><\/html>.*/ ) {
		$tiny = $1;
		print $tiny."\n";
		Clipboard->copy($tiny);
		my $mess = "Your tiny URL: $tiny
You can do a middle clic to paste it everywhere";
		`dbus-send --session --dest=$db_showdialog string:"$mess" int32:5`;
	}
}

if (defined($ARGV[0])) {
	if ( $ARGV[0] =~ /^action_on_click$/ ) {
		if ( $conf{'left_clic'} eq "0") {
			&shorturllastdnd2share;
		} else {
			&geturl;
		}
	} elsif ( $ARGV[0] =~ /^action_on_middle_click$/ ) {
		if ( $conf{'left_clic'} eq "0") {
			&geturl;
		} else {
			&shorturllastdnd2share;
		}
	} elsif ( $ARGV[0] =~ /^action_on_scroll_icon$/ ) {
		if ( $ARGV[1] eq "0" ) {			
			`dbus-send --session --dest=$db_showdialog string:"Up !" int32:2`;
		} else {
			`dbus-send --session --dest=$db_showdialog string:"Down !" int32:2`;
		}
	} elsif ( $ARGV[0] =~ /^action_on_drop_data$/ ) {
		if ( $ARGV[1] =~ /^http.*/ ) {
			&uploadurl($ARGV[1]);
		} else {
			`dbus-send --session --dest=$db_showdialog string:"Error, your URL can't be shorten (is your URL valid?)" int32:2`;
		}
	} elsif ( $ARGV[0] =~ /^action_on_init$/ ) {
		&load;
	} elsif ( $ARGV[0] =~ /^action_on_stop$/ ) {
	} elsif ( $ARGV[0] =~ /^action_on_reload$/ ) {
		&load;
	} elsif ( $ARGV[0] =~ /^action_on_build_menu$/ ) {
		&createmenu
	} elsif ( $ARGV[0] =~ /^action_on_menu_select$/ ) {
		my $file = "/home/".$ENV{USER}."/.config/cairo-dock/third-party/ShortUrl/ShortyUrl.db";
		open(FIC,$file);
		my @sort = <FIC>;
		close (FIC);
		$menu = $sort[0];
		my $menu2 = $ARGV[1] + 1;
		my @sort2 = split(/,/,$menu);
		$link = "";
		$title = "";
		open(FIC,"/home/".$ENV{USER}."/.config/cairo-dock/dnd2share/history.conf") or &errordnd2share;
		while(<FIC>) {
			if ( $_ =~ /^url0=(.*)$/ ) {
				$link = $1;
			} elsif ( $_ =~ /^local\spath=(.*)$/ ) {
				$title = $1;
				$title =~ s/.*\///g;
			}
			if ( $title eq $sort2[$menu2] ) {
				&uploadurl($link);
				$link = "";
				$title = "";
			}
		}
		close(FIC);
	} elsif ( $ARGV[0] =~ /^action_on_answer$/ ) {
		if ( $ARGV[1] =~ /^http.*/ ) {
			&uploadurl($ARGV[1]);
		} else {
			`dbus-send --session --dest=$db_showdialog string:"Error, your URL can't be shorten (is your URL valid?)" int32:2`;
		}		
	}
} else {
	die "\n\tDoit Etre Utilisé Uniquement Avec Cairo-Dock ( http://www.glx-dock.org/ ) ...\n"
}

1;
