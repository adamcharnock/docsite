require 'liquid'

module Jekyll
  module Filters
    def pretty_url(input)
    	if input == "index.html"
    		return
    	else
			return input.gsub(/(\/index)?\.html/, '')
		end
    end
  end
end

Liquid::Template.register_filter(Jekyll::Filters)