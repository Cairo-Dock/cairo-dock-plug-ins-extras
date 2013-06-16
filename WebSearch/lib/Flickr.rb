# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module fetch results from Flickr, including thumbnails - www.flickr.com

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
		flickr = Nokogiri::HTML(open(URI.encode("#{self.query_url}#{query}#page=#{page}"), "User-Agent" => self.user_agent))
		(flickr/"div[@class^='thumb']").each do |res|
		  photo = res.at("a[@class='rapidnofollow photo-click']")
	    url = photo['href']
	    description = photo['title']
	    thumb_url = photo.at("img")['data-defer-src']
			self.links << ThumbnailedLink.new("#{self.base_url}#{url}", description, thumb_url, self.name)
		end
		self.links
	end

end								
