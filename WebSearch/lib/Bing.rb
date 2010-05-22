class Bing < Engine

	def initialize
		self.name = self.class.to_s
		self.base_url = "http://www.bing.com"
		self.query_url = "#{self.base_url}/search?q="											# 10 results per page
		super
	end

	# Fetch links from Bing. Since Bing does not provide an in-url way to fetch more links than the 10
	# as Google does (&num=amount_to_fetch), this method will be called every time that 10 new results need to be shown
	def retrieve_links(query, offset = 1)
		bing = Nokogiri::HTML(open("#{self.query_url}#{query}&first=#{offset}"))
		self.stats = retrieve_bing_result_stats(bing, query)
		(bing/"h3").search("a[@onmousedown]").each do |raw_link|
			url = raw_link['href']
			description = raw_link.inner_text
			self.links << Link.new(url, description)
		end
		self.links
	end

	# Retrieve informations from Bing search stats	
	# The stats array postions "first-second 'of' third 'results'"
	def retrieve_bing_result_stats bing, query
		stats = (bing/"span[@id='count']").inner_text
		total = stats.split.fifth
		"Search for #{query} returned #{total} results"
	end
end
