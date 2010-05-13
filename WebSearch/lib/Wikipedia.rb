class Wikipedia < Engine

	attr_accessor :number_of_fetched_links

	def initialize
		self.number_of_fetched_links = 100
		self.base_url = "http://en.wikipedia.org"
		self.query_url = "#{self.base_url}/w/index.php?title=Special:Search&search="				# parameter "limit" results per page
		super
	end
	
	# Fetch links from english Wikipedia. It is necessary to set user agent, or the connection is Forbidden (403)
	def retrieve_links(query, offset = 0)
		wikipedia = Nokogiri::HTML(open("#{self.query_url}#{query}&offset=#{offset}&limit=#{self.number_of_fetched_links}", 'User-Agent' => 'ruby'))
		self.stats = retrieve_webshots_result_wikipedia(wikipedia, query)
		(wikipedia/"ul[@class='mw-search-results']/li/a").each do |res|
			url = res['href']
			description = res['title']
			self.links << Link.new("#{self.query_url}#{url}", description)
		end
		self.links
	end

	def retrieve_webshots_result_wikipedia (wikipedia, query)
		total = wikipedia.at("div[@class='results-info']/ul/li/b").next.next.inner_text
		"Search for #{query} returned #{total} results"
	end
end
