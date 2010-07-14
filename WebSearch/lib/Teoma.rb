# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module fetch results from Teoma - www.teoma.com

class Teoma < Engine

	def initialize
		self.name = self.class.to_s
		self.base_url = "http://www.teoma.com"
		self.query_url = "#{self.base_url}/web?q="										# 10 results per page
		super
	end	
	# Instead of the offset (the index of the first link), Teoma (ask.com) receives the offset with the *page* value
	# The href paremeter has the URL and the tag's content has the description.
	# Teoma results are placed in an <a> tag with id='r(digit)_t'.
	def retrieve_links(query, page = 1)
		teoma = Nokogiri::HTML(open(URI.encode("#{self.query_url}#{query}&page=#{page}")))
		self.stats = retrieve_teoma_result_stats(teoma, query)
		(teoma/"a[@id$='_t']").each do |res|											# any a tag with an id that ends with _t
			url = res['href']
			description = res.inner_text
			self.links << Link.new(url, description)
		end
		self.links
	end

	def retrieve_teoma_result_stats(teoma, query)
		total = teoma.at("//span[@id='indexLast']").next.next.inner_text
		"Search for #{query} returned #{total} results"
	end
end
