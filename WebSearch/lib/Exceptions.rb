module Exceptions
	class UnknownEngineException < StandardError
		def initialize(engine)
			@engine = engine
		end
		def message
			"Unknown search engine #{@engine}"
		end
	end
end

