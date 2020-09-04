# FIXME: npm install --global @vue/cli?

all: build

.PHONY: clean
clean:
	-rm -rf dist
	-rm -rf node_modules

.PHONY: deps
deps:
	yarn install

.PHONY: gen
gen: deps
	yarn proto

.PHONY: build
build: gen
	yarn build

.PHONY: serve
serve:
	yarn serve

.PHONY: lint
lint:
	yarn lint
