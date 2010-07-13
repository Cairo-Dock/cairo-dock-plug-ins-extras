# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module makes the Link abstraction with two classes,
# I - Link, links that does not have related thumb image
# II - ThumnailedLink, links from sites which have thumbnail also deals with thumb download 

class String

	require 'iconv'

	def shorten (count = 70)															# TODO: count as a parameter in .conf 
		if length > count
			shortened = slice(0 .. count-1)
			shortened + "..." if shortened
		else
			self
		end
	end

	def to_utf8
		Iconv.iconv('ascii//ignore//translit', 'utf-8', self).to_s						# what cannot be translitered in UTF-8, must be ignored
	end
end

class Link
	attr_accessor :url, :description, :id, :icon, :shortened_url
	@@next_id = 0																		# sequential id "static"

	def initialize (url, description, icon = File.expand_path("./icon"))
		self.url = url
		self.description = description.shorten.to_utf8									# Dbus parameters must to be string encoded in UTF-8
		self.id = @@next_id += 1
		self.icon = icon
		self.shortened_url = url.shorten
	end

	def self.reset_next_id
		class_variable_set(:@@next_id, 0)												# metaprogramming to reset the instance counter
	end
end

class ThumbnailedLink < Link															# a nice refactoring with the old YoutubeLink class
	attr_accessor :image_id, :thumb_url, :downloaded_thumb, :engine
	@@next_image_id = 0

	def initialize(url, description, thumb_url, engine)
		super(url, description)
		self.thumb_url = thumb_url
		self.image_id = @@next_image_id += 1
        self.engine = engine                                                            # just to define the output directory
		self.downloaded_thumb = false													# keep track of which thumbs were downloaded
	end

	def download_thumbnail																# remember that is being threaded outside
		# download thumb quietly (q), name it (O) '#{image_id}.jpg' and take it to the directory named as engine
        thumb_path = "./images/#{self.engine}/#{self.image_id}.jpg"                     # search engine name == directory name
		IO.popen("wget -q '#{self.thumb_url}' -O #{thumb_path}") do |io|			    # important enclose url in single quotes cuz there is '&'
			IO.select([io], nil, nil, 0.5)												# non-blocking download through the pipe
		end
		self.downloaded_thumb = true
		self.icon = File.expand_path(thumb_path)
	end

	def downloaded_thumb?
		self.downloaded_thumb
	end

	def self.reset_next_image_id
		class_variable_set(:@@next_image_id, 0)											# metaprogramming to reset the instance counter
	end
end
