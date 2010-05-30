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
	DIGG = "Digg"
	
	# All the engines. Help to create the list of strings controlled by mouse scroll to be shown in the icon
	List = [GOOGLE, BING, YAHOO, TEOMA, WIKIPEDIA, YOUTUBE, WEBSHOTS, FLICKR, IMAGESHACK, TWITTER, DIGG]
    
    # some engines use the concept of offset which is the first index of an interval of links/images to be shown
	# but there is those that use a sequential page (1,2,3, ...) which has an amount of links/images, etc
    PaginatedByPage = [TEOMA, YOUTUBE, FLICKR, IMAGESHACK, TWITTER, DIGG]
#	PaginatedByOffset = [GOOGLE, BING, YAHOO, WEBSHOTS, WIKIPEDIA]

	def self.exists? (engine)
		List.include? engine
	end

	def self.at (index)
		List.at index
	end

    # since there is just pagination by page or offset, only one of the following
    # methods would solve, but for readability I choose write both
    def self.paginated_by_page?(engine)
        PaginatedByPage.include?(engine)
    end

#	def self.paginated_by_offset?(engine)
#		PaginatedByOffset.include?(engine)
#	end
end
