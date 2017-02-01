test:
	./build-scripts/test.sh

docs:
	./build-scripts/build_docs.sh

publish-docs: docs
	./build-scripts/publish_docs.sh

publish: test publish-docs
	python setup.py sdist upload -r pypi

.PHONY: test publish docs publish-docs
