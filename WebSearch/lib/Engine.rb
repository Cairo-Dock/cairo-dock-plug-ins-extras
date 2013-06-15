# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module acts as a Factory + Inheritance
# It connects the WebSearch to the right search engine module

class Engine

	require './lib/Engines.rb'
	require './lib/Link.rb'
	require './lib/Exceptions.rb'

	attr_accessor :name, :stats, :links, :base_url, :query_url, :user_agent

	def initialize
		self.links =[]
		self.stats = ""
		self.user_agent = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"
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
