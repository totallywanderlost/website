.PHONY: build

port ?= 8080

setup:
	asdf install
	asdf plugin add ruby
	asdf plugin add python
	$(MAKE) setup_bundle
	$(MAKE) setup_pipenv

setup_bundle:
	gem install bundler:2.3.9
	bundle

setup_pipenv:
	pip install "pipenv==2022.3.28"
	pipenv install --deploy

fetch:
	@pipenv run python data/fetch.py -t $(trip) -f $(file)

build:
	@JEKYLL_ENV=production bundle exec jekyll build

run:
	@JEKYLL_ENV=production bundle exec jekyll serve -P $(port)
