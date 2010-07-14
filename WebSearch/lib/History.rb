# This is a part of the external WebSearch applet for Cairo-Dock
# Author: Eduardo Mucelli Rezende Oliveira
# E-mail: edumucelli@gmail.com or eduardom@dcc.ufmg.br
#
# This module deals with the History file that is used to compose
# the context menu "History"

module History
    
    @Entries = []
    NumberOfEntries = 10
    @file = '.history'

    # Return and fill the list of history terms
    def self.entries
        # it is important to bring a reversed list in which the most recent search term appears on the top (first) of the list 
        @Entries = IO.readlines(@file).reverse.first(NumberOfEntries)
    end

    # Save (if necessary) the new entry in the history file
    def self.save_new_entry (entry)
        unless @Entries.include? entry                                                  # if doest not existe yet ...
            File.open(@file, 'a') {|file| file.puts entry}                              # append the new entry at the end of the file
        end
    end

    def self.empty?
        @Entries.empty?
    end

    def self.clear
        File.delete(@file)
        File.open(@file, 'w')
    end
end
