class Webshots < Engine
	
	def initialize
		self.name = self.class.to_s
		self.base_url = "http://www.webshots.com"
		self.query_url = "#{self.base_url}/search?querySource=community&query="								# 36 results per page
		super
	end

	# url, e.g, http://good-times.webshots.com/photo/2500137270102572130
	# thumb_url, e.g, http://thumb10.webshots.net/t/24/665/1/37/27/2500137270102572130SmNoHt_th.jpg"
	def retrieve_links(query, offset = 0)
		webshots = Nokogiri::HTML(open("#{self.query_url}#{query}&start=#{offset}"))
		self.stats = retrieve_webshots_result_stats(webshots, query)
		(webshots/"a[@class='searchListItemLink']").each do |res|
			url = res['href']
			description = res['title']
			thumb_url = res.at("img[@class='searchListItemImg']")['src']
			self.links << ThumbnailedLink.new(url, description, thumb_url, self.name)
		end
		self.links
	end

	def retrieve_webshots_result_stats(webshots, query)
		total = webshots.at("span[@class='resultsNo']/strong").inner_text
		"Search for #{query} returned #{total} results"
	end
end
