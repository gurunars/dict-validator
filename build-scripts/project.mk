test docs publish-docs publish:
	./build-scripts/$@.sh

publish-docs: docs

publish: test publish-docs

.PHONY: test publish docs publish-docs
