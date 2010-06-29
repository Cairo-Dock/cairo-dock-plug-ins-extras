class ImageShack < Engine

	def initialize
		self.name = self.class.to_s
		self.base_url = "http://imageshack.us"
		self.query_url = "#{self.base_url}/new_search.php?q="								# 49 results per page
		super
	end

    # ImageShack does not provide image description
	def retrieve_links(query, page = 1)
		imageshack = Nokogiri::HTML.parse(open(URI.encode("#{self.query_url}#{query}&page=#{page}")))
		(imageshack/"a[@class='search_result']").each do |res|
			url = res['href']
			thumb_url = res.at("img")['src']
			self.links << ThumbnailedLink.new(url, "", thumb_url, self.name)
		end
		self.links
	end

end
