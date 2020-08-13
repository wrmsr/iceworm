DOCKER_USER=wrmsr

DOCKER_IMAGES:= \
	iceworm-dev \
	iceworm-minio \
	iceworm-postgres \

DOCKER_COMPOSE_DEFAULT_SERVICES:= \
	iceworm-minio \
	iceworm-postgres \

DOCKER_COMPOSE_SERVICES:= \
	$(DOCKER_COMPOSE_DEFAULT_SERVICES) \

.PHONY: all
all: clean images

define do-image
	(cd .. && docker build --tag "$(DOCKER_USER)/$1" -f "docker/$1/Dockerfile" .)
endef

define do-clean
	docker-compose rm -fv $1
endef

clean-services: stop
	for SVC in $(DOCKER_COMPOSE_SERVICES) ; do \
		docker-compose rm -fv "$$SVC" ; \
	done

.PHONY: clean
clean: clean-services
	docker-compose rm -fv iceworm-dev

.PHONY: images
images:
	for IMG in $(DOCKER_IMAGES) ; do \
		(cd .. && docker build --tag "$(DOCKER_USER)/$$IMG" -f "docker/$$IMG/Dockerfile" .) ; \
	done

.PHONY:
push:
	for IMG in $(DOCKER_IMAGES) ; do \
		docker push "$(DOCKER_USER)/$$IMG" ; \
	done

.PHONY:
pull:
	for IMG in $(DOCKER_IMAGES) ; do \
		docker pull "$(DOCKER_USER)/$$IMG" ; \
	done

.PHONY: start
start:
	docker-compose start

.PHONY: stop
stop:
	docker-compose stop

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: rmdev
rmdev:
	docker-compose rm -sf iceworm-dev

.PHONY: reup
reup: stop
	docker-compose rm -sf $(DOCKER_COMPOSE_SERVICES)
	$(MAKE) clean-services images
	docker-compose up --no-recreate $(DOCKER_DEFAULT_COMPOSE_SERVICES) iceworm-dev

.PHONY: enable-ptrace
enable-ptrace:
	docker run --privileged -it python:3 sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
