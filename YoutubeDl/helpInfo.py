class helpMessages:
    downloaderHelp ="""Download videos from youtube.com or other video platforms

DESCRIPTION
  Download videos from youtube.com or any other of the supported video platforms.

Currently supported sites are: CollegeHumor, Comedy Central, Dailymotion, 
Facebook, Metacafe, MyVideo, Photobucket, The Escapist, Vimeo, Yahoo!, YouTube, 
blip.tv, depositfiles.com, video.google.com, xvideos, Soundcloud, InfoQ, 
Mixcloud, OpenClassRoom.

Many YouTube.com videos are in Flash Video format and their extension would
be "flv". Other videos are encoded in H.264 and these usually have the
extension "mp4".  In Linux and other unices, video players using a
recent version of ffmpeg can play them. That includes MPlayer, VLC,
xine, among others.

OPTIONS
  Update:   Update this program to the latest stable version.
  Ignore Errors:  Ignore errors during download and continue processing.
  Username:  Specify the youtube account username. Some videos require an
          account to be downloaded, mostly because they're flagged as mature
          content.
  Password:  Like the username, specifies the account password.
  Format:  Specify the video format (quality) in which to download the video.
          For youtube.com, in particular, the meaning of the format codes is
          given as:
          WebM video at 480p: 43
          WebM video at 720p: 45
          H264 video in MP4 container at 480p: 18
          H264 video in MP4 container at 720p: 22
          H264 video in MP4 container at 1080p: 37
          H264 video in FLV container at 360p: 34
          H264 video in FLV container at 480p: 35
          H263 video at 240p: 5
          3GP video: 17

          Note that not all videos are available in all formats and that
          other sites supported by youtube-dl may have different conventions
          for their video formats.
  Max Quality:  Limit the maximum quality of the videos to download.
  Title:  Use the title of the video in the file name used to download the
          video.
  No Overwrites:  Do no overwrite already existing files.

  Continue:  Resume partially downloaded files.

AUTHOR
       youtube-dl was written by Ricardo Garcia Gonzalez and many contributors
       from all around the internet.
"""

    pluginHelp = """     Youtube Download Applet 

This applet allows a user to drag Youtube links from the Youtube website and 
drop them on the icon to download. The backend downloader is based on 
youtube-dl.py.  If you have python-tk installed on your system saving and 
loading url lists will be done using a graphical dialog box, otherwise you 
need to set the directory path in the configuration and just enter the filename
in the popup box.  If you have pynotify installed on your system you have the 
option of letting the notification area of your desktop handle the alerts, 
otherwise alerts will be done using the cairo-dock popup messages. You can 
turn this feature on or off under the configuration.  Currently the url list 
is not editable from the dock but if you save the list to a file you can edit 
with a text editor then load the list back into the plugin. Downloading can 
be paused from the context menu of the icon and you can choose to have 
downloads start automatically in the configuration area.  The left click button
on the mouse brings up the current url list and the middle button can be 
configured for different actions.
"""
