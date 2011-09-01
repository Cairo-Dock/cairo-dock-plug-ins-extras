

Copy the CairoBzr folder into ~/.config/cairo-dock/third-party to let the dock register it automatically.

Compile it with (you may have to install valac) :

cd CairoBzr
./compile.sh

SUDO Password
-------------
To remove the popup asking for your password after compilation, you need to edit
the /etc/sudoers file (edit with visudo as root) and add the line (replace
YOUR_USERNAME with your correct username) :

 YOUR_USERNAME           ALL = NOPASSWD: /usr/bin/make

BZR Password
------------
I don't know why bzr ask for your password for basic tasks on public branches
when you have defined a name in it's config, but here is a way to only have to
set it once per session. Just load your ssh ID with ssh-agent :

ssh-add ~/.ssh/id_dsa
# or 
ssh-add ~/.ssh/id_rsa # depends on which key file you use
