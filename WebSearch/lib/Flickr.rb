class Flickr < Engine
	
	def initialize
		self.name = self.class.to_s
		self.base_url = "http://www.flickr.com"
		self.query_url = "#{self.base_url}/search/?q="								# 28 results per page
		super
	end

	# url, e.g., /photos/21078069@N03/2780732654/
	# thumb_url, e.g., http://farm4.static.flickr.com/3255/2780732654_b7cbb2fb98_t.jpg"
	def retrieve_links(query, page = 1)
		flickr = Nokogiri::HTML(open("#{self.query_url}#{query}#page=#{page}"))
		(flickr/"span[@class='photo_container pc_t']/a").each do |res|
			url = res['href']
			description = res['title']
			thumb_url = res.at("img")['src']
			self.links << ThumbnailedLink.new("#{self.base_url}#{url}", description, thumb_url)
		end
		self.links
	end

end								
