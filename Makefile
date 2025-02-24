# version string from pyproject.toml
VERSION := $(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

# default list of platforms for which multiarch image is built
ifeq (${PLATFORMS}, )
	export PLATFORMS="linux/amd64,linux/arm64"
endif

.PHONY: usage
usage:
	@echo "Usage:"
	@echo "  make build"

.PHONY: build
build:
	@if ! docker buildx ls | grep -q container-builder; then\
		docker buildx create --platform ${PLATFORMS} --name container-builder --use;\
	fi
	docker buildx build --no-cache --platform ${PLATFORMS} \
		-t dash14/amazon-translate-simple-mock:${VERSION} \
		-t dash14/amazon-translate-simple-mock:latest \
		-t ghcr.io/dash14/amazon-translate-simple-mock:${VERSION} \
		-t ghcr.io/dash14/amazon-translate-simple-mock:latest \
		. --push
