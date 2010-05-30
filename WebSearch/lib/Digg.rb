class Digg < Engine

	def initialize
		self.name = self.class.to_s
		self.base_url = "http://digg.com"
		self.query_url = "#{self.base_url}/search?s="													# 9 results per page
		super
	end

    # url, e.g, http://www.susegeek.com/general/cairo-dock-desktop-dock-for-opensuse-linux/
    # thumb_url, e.g, http://digg.com/linux_unix/Cairo_Dock_Desktop_dock_for_openSUSE_Linux/s.png
    # description, e.g, Cairo-Dock - Desktop dock for openSUSE Linux
	def retrieve_links(query, page = 1)
		digg = Nokogiri::HTML.parse(open("#{self.query_url}#{query}&page=#{page}", 'User-Agent' => 'ruby')) # if User-Agent is not defined open hangs
		(digg/"div[@id^='enclosure']").each do |res|
			description = res.at("h3[@id^='title']/a").inner_text										# always present
			url = res.at("h3[@id^='title']/a")['href']													# always present
			raw_thumb_url = res.at("a[@class^='thumb']/img")											# not always exist a thumb
			if raw_thumb_url																			# check if exist a thumb for this news on digg
				thumb_url = raw_thumb_url['src']														# if so, get the url of the thumb
				self.links << ThumbnailedLink.new(url, description, thumb_url, self.name)
			else	
				self.links << Link.new(url, description)
			end
		end
		self.links
	end

end
