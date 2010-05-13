class Engine 																			# Factory + Inheritance

	require './lib/Link.rb'

	attr_accessor :name, :stats, :links, :base_url, :query_url, :engine

	def initialize
		self.links =[]
	end

	def connect
		WebSearch.log "connecting to #{self.name}"
		self.engine = case self.name
			when "Google"; require './lib/Google.rb'; Google.new						# lazy loading applied to engines libraries
			when "Bing"; require './lib/Bing.rb'; Bing.new
			when "Yahoo!"; require './lib/Yahoo.rb'; Yahoo.new
			when "Teoma"; require './lib/Teoma.rb'; Teoma.new
			when "Wikipedia"; require './lib/Wikipedia.rb'; Wikipedia.new
			when "Youtube"; require './lib/Youtube.rb'; Youtube.new
			when "Webshots"; require './lib/Webshots.rb'; Webshots.new
			when "Flickr"; require './lib/Flickr.rb'; Flickr.new
		end
	end

end
