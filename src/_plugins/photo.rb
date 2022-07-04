module Jekyll
  module PhotoFilter
    CDN = 'https://ik.imagekit.io/totallywanderlost'

    def avatar_url(name, config)
      photo_url("avatars/#{name.downcase}", config)
    end

    def photo_url(path, config)
      "#{CDN}/#{path}?tr=w-#{config['width']},h-#{config['height']},fo-center"
    end

    def photo_tag(path, config)
      "<img loading=lazy src=\"#{photo_url(path, config)}\" width=#{config['width']} height=#{config['height']}>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::PhotoFilter)
