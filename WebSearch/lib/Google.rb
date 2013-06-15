# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module fetch results from Google - www.google.com
class Google < Engine

	#attr_accessor :name, :stats, :links, :base_url, :query_url, :number_of_fetched_links
	attr_accessor :number_of_fetched_links

	def initialize
		self.name = self.class.to_s
		self.number_of_fetched_links = 100
		self.base_url = "http://www.google.com"
		self.query_url = "#{self.base_url}/search?q="											# (10,20,30,50,100) results per page"
		super
	end
	
	# Fetch a user-defined number links from Google with just one query. The parameter offset is the index of the first link.
    # It is better to fetch a higher amount of links in order to minimize the number of queries to be sent to google
	def retrieve_links (query, offset)
		google = Nokogiri::HTML(open(URI.encode("#{self.query_url}#{query}&start=#{offset}&num=#{self.number_of_fetched_links}"), "User-Agent" => self.user_agent))
		self.stats = retrieve_result_stats(google, query)
		(google/"h3[@class='r']").search("a[@href]").each do |raw_link|
			url = raw_link['href']
			# Google "injects" its images results in the backlink-based results, desconsidering it
			unless url.include? "?q=#{query}"
				description = raw_link.inner_text
				self.links << Link.new(url, description)
			end
		end
		self.links
	end
	
	# Retrieve informations from Google search stats
	# The stats array positions "Resultados first - second de aproximadamente third para fourth (fifth segundos)"
	def retrieve_result_stats(google, query)
		stats = (google/"div[@id='resultStats']")
		/^About ([\S]+) results \s\(([\S]+) seconds\)/.match(stats.inner_text)
		total, time = $1, $2
		"Search for #{query} returned #{total} results in #{time} seconds"
	end
end
