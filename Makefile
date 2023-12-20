.PHONY: build

port ?= 8080
env ?= production

setup:
	brew install rtx
	rtx install
	$(MAKE) setup_bundle
	$(MAKE) setup_pipenv
	$(MAKE) deps

setup_bundle:
	gem install bundler:2.3.9

setup_pipenv:
	pip install "pipenv==2022.3.28"

deps: bundle pipenv npm

bundle:
	bundle

pipenv:
	pipenv install --deploy

npm:
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

deploy: npm
	npx wrangler pages publish --project-name totallywanderlost build
