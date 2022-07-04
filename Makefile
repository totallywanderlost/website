.PHONY: build

port ?= 8080
env ?= production

setup:
	brew install asdf
	asdf plugin list | grep ruby || asdf plugin add ruby
	asdf plugin list | grep python || asdf plugin add python
	asdf plugin list | grep nodejs || asdf plugin add nodejs
	asdf install
	$(MAKE) setup_bundle
	$(MAKE) setup_pipenv
	$(MAKE) setup_npm

setup_bundle:
	gem install bundler:2.3.9
	bundle

setup_pipenv:
	pip install "pipenv==2022.3.28"
	pipenv install --deploy

setup_npm:
	npm ci

fetch:
	@pipenv run python data/fetch.py -t $(trip) -f $(file)

build:
	@JEKYLL_ENV=$(env) bundle exec jekyll build

run:
	@$(MAKE) build
	@npx concurrently \
	-n jekyll,server \
	-c red,yellow \
	"JEKYLL_ENV=$(env) bundle exec jekyll build --watch" \
	"BROWSER=none npx wrangler pages dev --port $(port) --live-reload ./build"
