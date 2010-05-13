class Link
	attr_accessor :url, :description, :id, :icon, :shortened_url
	@@next_id = 0																		# sequential id "static"

	def initialize (url = "", description = "", icon = File.expand_path("./icon"))
		self.url = url
		self.description = description
		self.id = @@next_id += 1
		self.icon = icon
		self.shortened_url = shorten url
	end

	def shorten (string, count = 45)													# TODO: count as a parameter in .conf file
		if string.length > count
			shortened = string.slice(0 .. count-1)
			shortened + "..." if shortened
		else
			string
		end
	end

	def self.reset_next_id
		class_variable_set(:@@next_id, 0)												# metaprogramming to reset the instance counter
	end
end

class ThumbnailedLink < Link															# a nice refactoring with the old YoutubeLink class
	attr_accessor :image_id, :thumb_url, :thumb_path, :downloaded_thumb
	@@next_image_id = 0

	def initialize(url = "", description = "", thumb_url = "")
		super(url, description)
		self.thumb_url = thumb_url
		self.image_id = @@next_image_id += 1
		self.thumb_path = define_thumbnail_path
		self.downloaded_thumb = false
	end

	def download_thumbnail																# remember that is being threaded outside
		# download thumb quietly (q), name it (O) '#{image_id}.jpg' and take it to the directory named as engine
		IO.popen("wget -q #{self.thumb_url} -O #{self.thumb_path}") do |io|				# open the pipe
			IO.select([io], nil, nil, 0.5)												# non-blocking download through the pipe
		end
		self.downloaded_thumb = true
		self.icon = File.expand_path(self.thumb_path)
	end

	# Thumbnail path composed by the search engine and image id
	# Extract from the thumb_url the what is the search engine using the the core of the url
	def define_thumbnail_path
		directories = %w(youtube webshots flickr)										# directories names like engines names
		directory = directories.detect {|d| self.url.include?(d)}						# search for engines names in url
		"./images/#{directory}/#{self.image_id}.jpg"
	end	

	def downloaded_thumb?
		self.downloaded_thumb
	end

	def self.reset_next_image_id
		class_variable_set(:@@next_image_id, 0)											# metaprogramming to reset the instance counter
	end
end
