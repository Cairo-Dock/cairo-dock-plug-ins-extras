class PopupTypes:
    (infoDialog, confirmAbort, saveListFilename, getListFilename, delList, showUrlList) = range(0, 6)

class menuEntries:
    (abortDownload, saveURLs, loadURLs, pauseDownload, enableDownload, clearURLs, editURLs) = range(7)

class youtube:
    videoFormats = {"H264 - MP4 at 480p":'18',
                    "H264 - MP4 at 720p":'22',
                    "H264 - MP4 at 1080p":'37',
                    "H264 - FLV at 360p":'34',
                    "H264 - FLV at 480p":'35',
                    "H263 - FLV at 240p":'5',
                    "Webm at 480p":'43',
                    "Webm at 720p":'45',
                    "3GP video":'17'}
