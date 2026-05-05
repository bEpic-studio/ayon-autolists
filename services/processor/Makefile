ADDON_VERSION := $(shell grep "version" ../../package.py | cut -d' ' -f3 | tr -d '"')
IMAGE := bepic/ayon-autolists-processor:$(ADDON_VERSION)

default:
	@echo ""
	@echo "AYON Autolists $(ADDON_VERSION) Service Builder"

build:
	docker build -t $(IMAGE) .

clean:
	if docker images "$(IMAGE)"; then \
		docker rmi $(IMAGE); \
	fi

push:
	if docker images "$(IMAGE)"; then \
		docker push $(IMAGE); \
	fi

clean-build: clean
	docker build --no-cache -t $(IMAGE) .
