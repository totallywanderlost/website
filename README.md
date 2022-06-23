# 🗺 Totally Wanderlost

## Requirements

- [brew](https://brew.sh)

## Setup

This will install `asdf` and use that to install the required versions
of `ruby` and `python` and the required dependencies for each. It assumes
you donn't already have `asdf` configured.

    make setup

## Build

This will build the site and store the output in the `build/` directory.

    make build

## Running Locally

This will build and serve the site on [localhost:8080](http://localhost:8080):

    make run

You can override the port if required:

    make run port=1337

## Deployments

Commits to the `main` branch are deployed automatically to [totallywanderlost.com](https://totallywanderlost.com) and hosted on [Cloudflare Pages](https://pages.cloudflare.com/).

Commits to a branch are deployed automatically to `${branch}.totallywanderlost.pages.dev`.

For example a brand named `test` would be available at [test.totallywanderlost.pages.dev](https://test.totallywanderlost.pages.dev).
