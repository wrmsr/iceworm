all:

.PHONY: clean
clean:
	-rm -rf node_modules
	-rm bundle.js

.PHONY: deps
deps:
	if [ ! -d node_modules ] ; then \
		npm install \
		\
			browserify \
			grunt \
			jmespath \
			uglify \
		\
		; \
	fi

.PHONY: bundle
bundle: deps
	node_modules/.bin/browserify blob.js | node_modules/.bin/uglifyjs > bundle.js
