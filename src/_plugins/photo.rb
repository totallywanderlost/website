module Jekyll
  module PhotoFilter
    CDN = 'https://ik.imagekit.io/totallywanderlost'

    def avatar_url(name, config)
      photo_url("avatars/#{name.downcase}", config)
    end

    def photo_url(path, config)
      "#{CDN}/#{path}?tr=w-#{config['width']},h-#{config['height']},fo-auto"
    end
  end
end

Liquid::Template.register_filter(Jekyll::PhotoFilter)
