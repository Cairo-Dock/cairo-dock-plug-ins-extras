class Engine 																			# Factory + Inheritance

	require './lib/Engines.rb'
	require './lib/Link.rb'
	require './lib/Exceptions.rb'

	attr_accessor :name, :stats, :links, :base_url, :query_url

	def initialize
		self.links =[]
		self.stats = ""
	end

	def connect
		WebSearch.log "trying to connect to #{self.name} lib"
		# The Yahoo! "!" signal was removed
		if Engines.exists? self.name
			require "./lib/#{self.name}.rb"; Kernel.const_get(self.name).new			# lazy loading, e.g, require "./lib/Google.rb"; Google.new
		else
			raise Exceptions::UnknownEngineException.new(self.name)
		end
	end

end
