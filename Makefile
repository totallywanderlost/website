.PHONY: build

port ?= 8080

setup:
	asdf install
	gem install bundler:2.3.9
	bundle
	pip install "pipenv==2022.3.28"
	pipenv install --deploy

fetch:
	@pipenv run python data/fetch.py -t $(trip) -f $(file)

build:
	@bundle exec jekyll build

run:
	@bundle exec jekyll serve -P $(port)
