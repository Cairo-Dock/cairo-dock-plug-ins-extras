module Engines
	
	GOOGLE = "Google"
	BING = "Bing"
	YAHOO = "Yahoo"
	TEOMA = "Teoma"
	WIKIPEDIA = "Wikipedia"
	YOUTUBE = "Youtube"
	WEBSHOTS = "Webshots"
	FLICKR = "Flickr"
	IMAGESHACK = "ImageShack"
	TWITTER = "Twitter"
	List = [GOOGLE, BING, YAHOO, TEOMA, WIKIPEDIA, YOUTUBE, WEBSHOTS, FLICKR, IMAGESHACK, TWITTER]

	def self.exists? (engine)
		List.include? engine
	end

	def self.at (index)
		List.at index
	end
end
