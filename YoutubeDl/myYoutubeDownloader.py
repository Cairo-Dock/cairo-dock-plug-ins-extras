#! /usr/bin/env python
import random
import multiprocessing, Queue
import time, sys, os
from youtubedl import *
from Configuration import Configuration
#from CairoDockPlugin import CairoDockPlugin
from constantTypes import youtube

#gloabal debug option
doDebug = False

class myFileDownloader(FileDownloader):
    def __init__(self, params, result_queue, work_queue):
        super( myFileDownloader, self ).__init__(params)
        self.result_queue = result_queue
        self.work_queue = work_queue
        self.status = "Idle"

    def report_progress(self, percent_str, data_len_str, speed_str, eta_str):
        global doDebug
        reportList = percent_str+";"+data_len_str+";"+speed_str+";"+eta_str
        if not(self.status == "Aborting"):
            try:
                self.result_queue.put_nowait(reportList)
                if doDebug:
                    print "putting report list on the result queue:\n "+reportList
            except Queue.Full:
                #clear the queue if the Plugin has not read it since the last put
                self.result_queue.get_nowait()
                if doDebug:
                    print "Clearing result queue"
                #now go ahead and put information on it
                self.result_queue.put_nowait(reportList)
                if doDebug:
                    print "report list placed on the queue: "+reportList
            try:
                command = self.work_queue.get_nowait()
                if command == 'Abort':
                    if doDebug:
                        print "Download Abort sent to sys.exit : report_progress"
                    print "Download Abort sent to sys.exit : report_progress"
                    sys.exit('Abort')
                    self.status = "Aborting"
                    #clear the queue if the Plugin has not read it since the last put
                    self.result_queue.get_nowait()
                    self.result_queue.get_nowait()
            except Queue.Empty:
                time.sleep(1)

class YoutubeDownloader(multiprocessing.Process):
 
    def __init__(self, work_queue, result_queue):
        global doDebug
 
        # base class initialization
        multiprocessing.Process.__init__(self)
 
        self.name = os.path.basename(os.path.abspath("."))
        self.__config = Configuration(self.name)
        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False

    def run(self):
        global doDebug
        while not self.kill_received:
            if doDebug:
                print "check for next url"
            try:
                url = self.work_queue.get()
                self.__config.refresh()
                videos_directory = self.__config.get('User Interface', 'videos_directory')
                self.useFormat = self.__config.get('Download Options', 'useFormat')
                self.videoFormat = self.__config.get('Download Options', 'videoFormat')
                self.maxVideoFormat = self.__config.get('Download Options', 'maxVideoFormat')
                self.useAuthentication = self.__config.get('Download Options', 'useAuthentication')
                self.userName = self.__config.get('Download Options', 'userName')
                self.userPassword = self.__config.get('Download Options', 'userPassword')
                self.ignoreErrors = self.__config.get('Download Options', 'ignoreErrors')
                self.resumeDownload = self.__config.get('Download Options', 'resumeDownload')
                self.noOverwrites = self.__config.get('Download Options', 'noOverwrites')
                self.useTitle = self.__config.get('Download Options', 'useTitle')

                if not videos_directory:
                    videos_directory = os.path.abspath(os.path.expanduser("~")+"/Videos")
                if not (videos_directory == os.path.abspath('.')):
                    os.chdir(videos_directory)
                if doDebug:
                    print "current video directory is: "+os.path.abspath('.')
                retcode = self.main(url)
            except Queue.Empty:
                time.sleep(1)

    def debug():
        global doDebug
        doDebug = True

    def main(self,url):
        global doDebug
        if doDebug:
            print "In main URL is: "+url
	parser, opts, args = parseOpts()
        #Need to set user options from config file if we can
        if self.useFormat == '0':
            opts.format = youtube.videoFormats.get(self.videoFormat)
        elif self.useFormat == '1':
            opts.format_limit = youtube.videoFormats.get(self.maxVideoFormat)
        if self.useAuthentication == '1':
            opts.username = self.userName
            opts.password = self.userPassword
        opts.continue_dl = self.resumeDownload
        opts.ignoreerrors = self.ignoreErrors
        opts.nooverwrites = self.noOverwrites
        opts.usetitle = self.useTitle

	# Open appropriate CookieJar
	if opts.cookiefile is None:
		jar = cookielib.CookieJar()
	else:
		try:
			jar = cookielib.MozillaCookieJar(opts.cookiefile)
			if os.path.isfile(opts.cookiefile) and os.access(opts.cookiefile, os.R_OK):
				jar.load()
		except (IOError, OSError), err:
                        time.sleep(1)

	# Dump user agent
	if opts.dump_user_agent:
		print std_headers['User-Agent']

	# Batch file verification
	batchurls = []
	if opts.batchfile is not None:
		try:
			if opts.batchfile == '-':
				batchfd = sys.stdin
			else:
				batchfd = open(opts.batchfile, 'r')
			batchurls = batchfd.readlines()
			batchurls = [x.strip() for x in batchurls]
			batchurls = [x for x in batchurls if len(x) > 0 and not re.search(r'^[#/;]', x)]
		except IOError:
                        time.s;eep(1)
	all_urls = batchurls
        all_urls.append(url)

	# General configuration
	cookie_processor = urllib2.HTTPCookieProcessor(jar)
	proxy_handler = urllib2.ProxyHandler()
	opener = urllib2.build_opener(proxy_handler, cookie_processor, YoutubeDLHandler())
	urllib2.install_opener(opener)
	socket.setdefaulttimeout(300) # 5 minutes should be enough (famous last words)

	if opts.verbose:
		print(u'[debug] Proxy map: ' + str(proxy_handler.proxies))

	extractors = gen_extractors()

	if opts.list_extractors:
		for ie in extractors:
			print(ie.IE_NAME)
			matchedUrls = filter(lambda url: ie.suitable(url), all_urls)
			all_urls = filter(lambda url: url not in matchedUrls, all_urls)
			for mu in matchedUrls:
				print(u'  ' + mu)

	# Conflicting, missing and erroneous options
	if opts.usenetrc and (opts.username is not None or opts.password is not None):
		parser.error(u'using .netrc conflicts with giving username/password')
	if opts.password is not None and opts.username is None:
		parser.error(u'account username missing')
	if opts.outtmpl is not None and (opts.useliteral or opts.usetitle or opts.autonumber):
		parser.error(u'using output template conflicts with using title, literal title or auto number')
	if opts.usetitle and opts.useliteral:
		parser.error(u'using title conflicts with using literal title')
	if opts.username is not None and opts.password is None:
		opts.password = getpass.getpass(u'Type account password and press return:')
	if opts.ratelimit is not None:
		numeric_limit = FileDownloader.parse_bytes(opts.ratelimit)
		if numeric_limit is None:
			parser.error(u'invalid rate limit specified')
		opts.ratelimit = numeric_limit
	if opts.retries is not None:
		try:
			opts.retries = long(opts.retries)
		except (TypeError, ValueError), err:
			parser.error(u'invalid retry count specified')
	try:
		opts.playliststart = int(opts.playliststart)
		if opts.playliststart <= 0:
			raise ValueError(u'Playlist start must be positive')
	except (TypeError, ValueError), err:
		parser.error(u'invalid playlist start number specified')
	try:
		opts.playlistend = int(opts.playlistend)
		if opts.playlistend != -1 and (opts.playlistend <= 0 or opts.playlistend < opts.playliststart):
			raise ValueError(u'Playlist end must be greater than playlist start')
	except (TypeError, ValueError), err:
		parser.error(u'invalid playlist end number specified')
	if opts.extractaudio:
		if opts.audioformat not in ['best', 'aac', 'mp3', 'vorbis', 'm4a', 'wav']:
			parser.error(u'invalid audio format specified')

	# File downloader
	fd = myFileDownloader({
		'usenetrc': opts.usenetrc,
		'username': opts.username,
		'password': opts.password,
		'quiet': (opts.quiet or opts.geturl or opts.gettitle or opts.getthumbnail or opts.getdescription or opts.getfilename or opts.getformat),
		'forceurl': opts.geturl,
		'forcetitle': opts.gettitle,
		'forcethumbnail': opts.getthumbnail,
		'forcedescription': opts.getdescription,
		'forcefilename': opts.getfilename,
		'forceformat': opts.getformat,
		'simulate': opts.simulate,
		'skip_download': (opts.skip_download or opts.simulate or opts.geturl or opts.gettitle or opts.getthumbnail or opts.getdescription or opts.getfilename or opts.getformat),
		'format': opts.format,
		'format_limit': opts.format_limit,
		'listformats': opts.listformats,
		'outtmpl': ((opts.outtmpl is not None and opts.outtmpl.decode(preferredencoding()))
			or (opts.format == '-1' and opts.usetitle and u'%(stitle)s-%(id)s-%(format)s.%(ext)s')
			or (opts.format == '-1' and opts.useliteral and u'%(title)s-%(id)s-%(format)s.%(ext)s')
			or (opts.format == '-1' and u'%(id)s-%(format)s.%(ext)s')
			or (opts.usetitle and opts.autonumber and u'%(autonumber)s-%(stitle)s-%(id)s.%(ext)s')
			or (opts.useliteral and opts.autonumber and u'%(autonumber)s-%(title)s-%(id)s.%(ext)s')
			or (opts.usetitle and u'%(stitle)s-%(id)s.%(ext)s')
			or (opts.useliteral and u'%(title)s-%(id)s.%(ext)s')
			or (opts.autonumber and u'%(autonumber)s-%(id)s.%(ext)s')
			or u'%(id)s.%(ext)s'),
		'ignoreerrors': opts.ignoreerrors,
		'ratelimit': opts.ratelimit,
		'nooverwrites': opts.nooverwrites,
		'retries': opts.retries,
		'continuedl': opts.continue_dl,
		'noprogress': opts.noprogress,
		'playliststart': opts.playliststart,
		'playlistend': opts.playlistend,
		'logtostderr': opts.outtmpl == '-',
		'consoletitle': opts.consoletitle,
		'nopart': opts.nopart,
		'updatetime': opts.updatetime,
		'writedescription': opts.writedescription,
		'writeinfojson': opts.writeinfojson,
		'matchtitle': opts.matchtitle,
		'rejecttitle': opts.rejecttitle,
		'max_downloads': opts.max_downloads,
		'prefer_free_formats': opts.prefer_free_formats,
		'verbose': opts.verbose,
		}, self.result_queue, self.work_queue)
	for extractor in extractors:
		fd.add_info_extractor(extractor)

	# PostProcessors
	if opts.extractaudio:
		fd.add_post_processor(FFmpegExtractAudioPP(preferredcodec=opts.audioformat, preferredquality=opts.audioquality, keepvideo=opts.keepvideo))

	# Update version
	if opts.update_self:
		updateSelf(fd, sys.argv[0])

	# Maybe do nothing
	if len(all_urls) < 1:
		if not opts.update_self:
			parser.error(u'you must provide at least one URL')
		else:
                        time.sleep(1)
	
	try:
		retcode = fd.download(all_urls)
                self.result_queue.put("DownloadComplete")
                if doDebug:
                    print "put DownloadComplete on result queue: return from fd.download"
	except MaxDownloadsReached:
		fd.to_screen(u'--max-download limit reached, aborting.')
                self.result_queue.put("DownloadAborted")
                if doDebug:
                    print "put DownloadAborted on result queue: MaxDownloadReached"
		retcode = 101
	except SystemExit:
                self.result_queue.get_nowait()
                self.result_queue.get_nowait()
                self.result_queue.put("DownloadAborted")
                print "put DownloadAborted on result queue: SystemExit"
                if doDebug:
                    print "put DownloadAborted on result queue: SystemExit"

	# Dump cookie jar if requested
	if opts.cookiefile is not None:
		try:
			jar.save()
		except (IOError, OSError), err:
                        time.s;eep(1)

        print "myDownloader has ended"
        if doDebug:
            print "myDownloader has ended"
