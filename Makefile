INTERACTIVE:=$(shell [ -t 0 ] && echo 1)
RUN=docker run --rm -v $(PWD):/project
IMG=python-library.cache
BASE=nephilimsolutions/docker-ci-python

all: clean static-checks tests build build-docs

update-base:
	docker pull ${BASE}

cache:
	echo "FROM ${BASE}" | docker build -t $(IMG) . -f-

help tests static-checks build connect repl clean build-docs reformat: cache
ifdef INTERACTIVE
	@$(RUN) -it $(IMG) $@
else
	@$(RUN) $(IMG) $@
endif

.PHONY: help build static-checks connect tests clean repl reformat all cache update-base
