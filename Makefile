SHELL:=/bin/bash

PROJECT:=iceworm

PYTHON_VERSION:=3.7.8

PYENV_ROOT:=$(shell if [ -z "$${PYENV_ROOT}" ]; then echo "$${HOME}/.pyenv" ; else echo "$${PYENV_ROOT%/}" ; fi)
PYENV_BIN:=$(shell if [ -f "$${HOME}/.pyenv/bin/pyenv" ] ; then echo "$${HOME}/.pyenv/bin/pyenv" ; else echo pyenv ; fi)

PIP_ARGS:=

PYENV_BREW_DEPS:= \
	openssl \
	readline \
	sqlite3 \
	zlib \

BREW_DEPS:= \
	$(PYENV_BREW_DEPS) \
	protobuf \

ANTLR_VERSION=4.8


### Toplevel

all: venv gen build flake test


### Clean

.PHONY: clean
clean:
	-rm -rf $(PROJECT).egg-info
	-rm -rf .benchmarks
	-rm -rf .cache
	-rm -rf .mypy_cache
	-rm -rf .pytest_cache
	-rm -rf .venv*
	-rm -rf build
	-rm -rf dist

	find $(PROJECT) \
	\
		-name '*.dylib' -delete -or \
		-name '*.exe' -delete -or \
		-name '*.pyc' -delete -or \
		-name '*.pyo' -delete -or \
		-name '*.so' -delete -or \
		-name '.revision' -delete -or \
		-name '__pycache__' -delete -or \
	\
	-name NeVeRmAtCh

	(cd $(PROJECT)-js && make clean)
	(cd $(PROJECT)-jvm && make clean)
	(cd $(PROJECT)-rs && make clean)


### Env

.PHONY: brew
brew:
	brew install $(BREW_DEPS)

define do-venv
	set -e ; \
	\
	if [ -z "$$DEBUG" ] && [ "$$(python --version)" = "Python $(2)" ] ; then \
		virtualenv $(1) ; \
	\
	else \
		PYENV_INSTALL_DIR="$(2)" ; \
		PYENV_INSTALL_FLAGS="-s -v"; \
		if [ ! -z "$$DEBUG" ] ; then \
			PYENV_INSTALL_DIR="$$PYENV_INSTALL_DIR"-debug ; \
			PYENV_INSTALL_FLAGS="$$PYENV_INSTALL_FLAGS -g" ; \
		fi ; \
		\
		if [ "$$(uname)" = "Darwin" ] && command -v brew ; then \
			PYENV_CFLAGS="" ; \
			PYENV_LDFLAGS="" ; \
			for DEP in $(PYENV_BREW_DEPS); do \
				DEP_PREFIX="$$(brew --prefix "$$DEP")" ; \
				PYENV_CFLAGS="-I$$DEP_PREFIX/include $$PYENV_CFLAGS" ; \
				PYENV_LDFLAGS="-L$$DEP_PREFIX/lib $$PYENV_LDFLAGS" ; \
			done ; \
			\
			PYTHON_CONFIGURE_OPTS="--enable-framework" ; \
			if brew --prefix tcl-tk ; then \
				TCL_TK_PREFIX="$$(brew --prefix tcl-tk)" ; \
				TCL_TK_VER="$$(brew ls --versions tcl-tk | head -n1 | egrep -o '[0-9]+\.[0-9]+')" ; \
				PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS --with-tcltk-includes='-I$$TCL_TK_PREFIX/include'" ; \
				PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS --with-tcltk-libs='-L$$TCL_TK_PREFIX/lib -ltcl$$TCL_TK_VER -ltk$$TCL_TK_VER'" ; \
			fi ; \
			\
			CFLAGS="$$PYENV_CFLAGS $$CFLAGS" \
			LDFLAGS="$$PYENV_LDFLAGS $$LDFLAGS" \
			PKG_CONFIG_PATH="$$(brew --prefix openssl)/lib/pkgconfig:$$PKG_CONFIG_PATH" \
			PYTHON_CONFIGURE_OPTS="$$PYTHON_CONFIGURE_OPTS" \
			"$(PYENV_BIN)" install $$PYENV_INSTALL_FLAGS $(2) ; \
		\
		else \
			"$(PYENV_BIN)" install $$PYENV_INSTALL_FLAGS $(2) ; \
		\
		fi ; \
		\
		"$(PYENV_ROOT)/versions/$$PYENV_INSTALL_DIR/bin/python" -m venv $(1) ; \
	fi ; \
	\
	$(1)/bin/pip install --upgrade pip setuptools wheel
endef

define do-deps
	(cat requirements.txt ; (if [ $(2) == "1" ] ; then cat requirements-dev.txt ; fi) ; echo) | \
		egrep -o '^[^#]+' | \
		egrep -v '[ ]*-r' | \
		egrep -v omnibus | \
		xargs $(1)/bin/pip $(PIP_ARGS) install ; \
	\
	$(1)/bin/pip install $(PIP_ARGS) --upgrade git+https://github.com/wrmsr/omnibus@wrmsr_working ; \
	\
	if [ -d "/Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/" ] ; then \
		if $(1)/bin/python -c 'import sys; exit(0 if sys.version_info < (3, 7) else 1)' ; then \
			$(1)/bin/python "/Applications/PyCharm.app/Contents/plugins/python/helpers/pydev/setup_cython.py" build_ext --inplace ; \
		fi ; \
	fi
endef

.PHONY: venv
venv:
	if [ ! -d .venv ] ; then \
		$(call do-venv,.venv,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv,1) ; \
	fi

.PHONY: venv-inst
venv-inst:
	if [ ! -d .venv-inst ] ; then \
		$(call do-venv,.venv-inst,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv-inst,0) ; \
	fi


### Gen

.PHONY: gen
gen: antlr proto
	true

.PHONY: antlr
antlr:
	if [ ! -f "antlr-$(ANTLR_VERSION)-complete.jar" ] ; then \
		curl \
			--proto '=https' \
			--tlsv1.2 \
			"https://www.antlr.org/download/antlr-$(ANTLR_VERSION)-complete.jar" \
			-o "antlr-$(ANTLR_VERSION)-complete.jar" ; \
	fi

	set -e ; \
	\
	java -version ; \
	\
	find $(PROJECT) -name _antlr -type d | xargs -n 1 rm -rf ; \
	\
	for D in $$(find $(PROJECT) -name '*.g4' | xargs -n1 dirname | sort | uniq) ; do \
		echo "$$D" ; \
		\
		mkdir "$$D/_antlr" ; \
		touch "$$D/_antlr/__init__.py" ; \
		\
		for F in $$(find "$$D" -maxdepth 1 -name '*.g4' | sort) ; do \
			cp "$$F" "$$D/_antlr/"; \
		done ; \
		\
		P=$$(pwd) ; \
		for F in $$(find "$$D/_antlr" -name '*.g4' | sort) ; do \
			echo "$$F" ; \
			( \
				cd "$$D/_antlr" && \
				java \
					-jar "$$P/antlr-$(ANTLR_VERSION)-complete.jar" \
					-Dlanguage=Python3 \
					-visitor \
					$$(basename "$$F") \
			) ; \
		done ; \
		\
		find "$$D/_antlr" -name '*.g4' -delete ; \
		\
		for P in $$(find "$$D/_antlr" -name '*.py' -not -name '__init__.py') ; do \
			( \
				BUF=$$(echo -e '# flake8: noqa' && cat "$$P") ; \
				IMP=$$(echo "$$D" | tr -dc / | tr / .) ; \
				BUF=$$(echo "$$BUF" | sed "s/^from antlr4/from omnibus._vendor.antlr4/") ; \
				echo "$$BUF" > "$$P" \
			) ; \
		done ; \
	done

.PHONY: proto
proto: venv
	.venv/bin/python -m $(PROJECT).protos.gen gen


### Build

define do-build
	$(1)/bin/python setup.py build_ext --inplace
endef

.PHONY: build
build: venv
	$(call do-build,.venv)


### Check

.PHONY: flake
flake: venv
	.venv/bin/flake8 $(PROJECT)

.PHONY: typecheck
typecheck: venv
	.venv/bin/mypy --ignore-missing-imports $(PROJECT) | awk '{c+=1;print $$0}END{print c}'


### Test

.PHONY: test
test: build
	.venv/bin/pytest -v $(PROJECT)

.PHONY: test-parallel
test-parallel: build
	.venv/bin/pytest -v -n auto $(PROJECT)

.PHONY: test-verbose
test-verbose: build
	.venv/bin/pytest -svvv $(PROJECT)


### Deps

.PHONY: deps
deps: venv
	$(call do-deps,.venv,1)

.PHONY: dep-freze
dep-freeze: venv
	.venv/bin/pip freeze > requirements-frz.txt

.PHONY: dep-tree
dep-tree: venv
	.venv/bin/pipdeptree

.PHONY: dep-updates
dep-updates: venv
	.venv/bin/pip list -o --format=columns


### Dist

define do-dist
	rm -rf build
	mkdir build
	$(eval DIST_BUILD_PYTHON:=$(shell echo "$(shell pwd)/$(1)/bin/python"))

	cp -rv \
		LICENSE \
		$(PROJECT) \
		README.md \
	\
		build/
	cp -rv \
		LICENSE-* \
	\
		build/ || :

	cp setup.py build/setup.py
	cp MANIFEST.in build/MANIFEST.in

	cd build && "$(DIST_BUILD_PYTHON)" setup.py clean

	git describe --match=NeVeRmAtCh --always --abbrev=40 --dirty > "build/$(PROJECT)/.revision"

	if [ "$(1)" = ".venv" ] ; then \
		cd build && "$(DIST_BUILD_PYTHON)" setup.py sdist --formats=zip ; \
	fi

	cd build && "$(DIST_BUILD_PYTHON)" setup.py bdist_wheel

	if [ ! -d ./dist ] ; then \
		mkdir dist ; \
	fi
	cp build/dist/* ./dist/
endef

.PHONY: dist
dist: venv
	$(call do-dist,.venv,0)


### Docker

## Proxies

.PHONY: docker-clean-venv
docker-clean-venv:
	rm -rf .venv-docker

.PHONY: docker-venv
docker-venv:
	./docker-dev make _docker-venv

.PHONY: _docker-venv
_docker-venv:
	if [ ! -d .venv-docker ] ; then \
		$(call do-venv,.venv-docker,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv-docker,1) ; \
	fi

.PHONY: docker-venv-inst
docker-venv-inst:
	./docker-dev make _docker-venv-inst

.PHONY: _docker-venv-inst
_docker-venv-inst:
	if [ ! -d .venv-docker-inst ] ; then \
		$(call do-venv,.venv-docker-inst,$(PYTHON_VERSION)) ; \
		$(call do-deps,.venv-docker-inst,0) ; \
	fi

.PHONY: docker-deps
docker-deps:
	./docker-dev make _docker-deps

.PHONY: _docker-deps
_docker-deps: _docker-venv
	$(call do-deps,.venv-docker,1)

.PHONY: docker-build
docker-build: docker-venv
	./docker-dev make _docker-build

.PHONY: _docker-build
_docker-build: _docker-venv
	$(call do-build,.venv-docker)

.PHONY: docker-test
docker-test: docker-build
	./docker-dev .venv-docker/bin/pytest -v $(PROJECT)

.PHONY: docker-dist
docker-dist: docker-venv
	./docker-dev make _docker-dist

.PHONY: _docker-dist
_docker-dist: _docker-venv
	$(call do-dist,.venv-docker,0,1)

## Compose

.PHONY: docker-clean
docker-clean:
	(cd docker && $(MAKE) clean)

.PHONY: docker-stop
docker-stop:
	(cd docker && $(MAKE) stop)

.PHONY: docker-rmdev
docker-rmdev:
	(cd docker && $(MAKE) rmdev)

.PHONY: docker-reup
docker-reup:
	(cd docker && $(MAKE) reup)

## Images

.PHONY: docker-invalidate
docker-invalidate:
	date +%s > .dockertimestamp


### Utils

.PHONY: pg-repl
pg-repl: venv
	export PORT=$$(.venv/bin/python -c "import yaml; dct = yaml.safe_load(open('docker/docker-compose.yml', 'r').read()); print(dct['services']['iceworm-postgres']['ports'][0].split(':')[0])") ; \
	PGPASSWORD=iceworm .venv/bin/pgcli --user iceworm --host localhost --port "$$PORT"

.PHONY: sf-repl
sf-repl:
	export $(cat .env | sed 's/#.*//g' | xargs) && \
	export $$(.venv/bin/python -c "import os, configparser; parser = configparser.ConfigParser(); parser.read_file(open(os.environ['ICEWORM_SNOWFLAKE_CONFIG_PATH'], 'r')); print(' '.join(f'SF_{k.upper()}={v}' for k, v in parser.items('snowflake')))" | xargs) && \
	snowsql --username "$$SF_USER" --host "$$SF_HOST" --accountname "$$SF_ACCOUNT" --authenticator "$$SF_AUTHENTICATOR" --schemaname "$$SF_SCHEMA"
