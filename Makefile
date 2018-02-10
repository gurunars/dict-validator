INTERACTIVE:=$(shell [ -t 0 ] && echo 1)
RUN=docker run --rm -v $(PWD):/project
IMG=docker-ci-python.cache

all: clean static-checks tests build build-docs

cache:
	echo "FROM docker-ci-python" | docker build -t $(IMG) . -f-

help tests static-checks build connect repl clean build-docs reformat: cache
ifdef INTERACTIVE
	@$(RUN) -it $(IMG) $@
else
	@$(RUN) $(IMG) $@
endif

.PHONY: help build static-checks connect tests clean repl reformat all cache
.DEFAULT_GOAL: help
