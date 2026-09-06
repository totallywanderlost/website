module Jekyll
  # Generates, from the trip manifest (src/_data/trips.yml) and the per-trip step
  # arrays (src/_data/journeys/<slug>.json):
  #
  #   /trips/<slug>/          -> layout: trip   (one page per published trip)
  #   /trips/<slug>/<key>/    -> layout: step   (one page per step with photos)
  #
  # Replaces the old jekyll-datapage-generator `page_gen` block, which could only
  # cope with a single flat journey.
  class TripPageGenerator < Generator
    safe true
    priority :normal

    # Matches the old page_gen filter_condition.
    def renderable?(step)
      step["state"] != "planned" && step["photos"] && !step["photos"].empty?
    end

    def generate(site)
      trips = site.data["trips"] || []
      journeys = site.data["journeys"] || {}

      trips.each do |trip|
        next unless trip["published"]

        slug = trip["slug"]
        steps = journeys[slug] || []

        site.pages << TripPage.new(site, slug, trip)

        steps.each do |step|
          next unless renderable?(step)

          site.pages << StepPage.new(site, slug, trip, step)
        end
      end
    end
  end

  class TripPage < PageWithoutAFile
    def initialize(site, slug, trip)
      super(site, site.source, File.join("trips", slug), "index.html")

      self.content = ""
      self.data = trip.merge(
        "layout" => "trip",
        "title" => trip["title"],
        "slug" => slug
      )
    end
  end

  class StepPage < PageWithoutAFile
    def initialize(site, slug, trip, step)
      super(site, site.source, File.join("trips", slug, step["key"]), "index.html")

      self.content = ""
      self.data = step.merge(
        "layout" => "step",
        "title" => step["name"],
        "trip_slug" => slug,
        "trip_title" => trip["title"]
      )
    end
  end
end
