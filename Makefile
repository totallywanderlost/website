port ?= 8080

setup:
	asdf install
	gem install bundler:2.3.9
	bundle

build:
	@bundle exec jekyll build

run:
	@python -m http.server --bind 127.0.0.1 $(port)
