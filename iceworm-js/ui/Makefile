# FIXME: npm install --global @vue/cli?

all: build

.PHONY: clean
clean:
	-rm -rf dist
	-rm -rf node_modules

.PHONY: deps
deps:
	yarn install

.PHONY: build
build: deps
	yarn build

.PHONY: serve
serve:
	yarn serve

.PHONY: lint
lint:
	yarn lint
