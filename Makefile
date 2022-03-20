port ?= 8080

run:
	@python -m http.server --bind 127.0.0.1 $(port)
