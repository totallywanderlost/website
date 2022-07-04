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
      src = photo_url(path, config)

      config.delete('width')
      config.delete('height')
      link = photo_url(path, config)

      "<a href=\"#{link}\"><img loading=\"lazy\" src=\"#{src}\" width=\"#{config['width']}\" height=\"#{config['height']}\"/></a>"
    end
  end
end

Liquid::Template.register_filter(Jekyll::PhotoFilter)
