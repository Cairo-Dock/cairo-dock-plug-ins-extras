# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module fetch results from Yahoo! - www.yahoo.com

class Yahoo < Engine

	def initialize
		self.name = self.class.to_s
		self.base_url = "http://search.yahoo.com"
		self.query_url = "#{self.base_url}/search?p="											# 10 results per page
		super
	end
	# Fetch links from Yahoo!. Since Yahoo! does not provide an in-url way to fetch more links than the 10
	# as Google does (&num=amount_to_fetch), this method will be called every time that 10 new results need to be shown
	def retrieve_links(query, offset = 1)
		yahoo = Nokogiri::HTML(open(URI.encode("#{self.query_url}#{query}&b=#{offset}")))
		self.stats = retrieve_yahoo_result_stats(yahoo, query)
		(yahoo/"div[@class~='res']").each do |res|					# divs are usually from 'res' class but some sub-results are 'res_indent' class
			url = (res/"span[@class='url']").inner_text
			description = (res/"h3/a").inner_text
			self.links << Link.new(url, description)
		end
		self.links
	end

	# Retrieve informations from Yahoo! search stats	
	def retrieve_yahoo_result_stats (yahoo, query)
		total = (yahoo/"strong[@id='resultCount']").inner_text
		"Search for #{query} returned #{total} results"
	end
end
