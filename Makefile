.PHONY: build

port ?= 8080

setup:
	asdf install
	gem install bundler:2.3.9
	bundle

build:
	@bundle exec jekyll build

run:
	@bundle exec jekyll serve -P $(port)
