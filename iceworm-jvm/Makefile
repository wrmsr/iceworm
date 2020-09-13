SHELL:=/bin/bash

UNAME:=$(shell uname)


### Toplevel

all: clean package test


### Java

.PHONY: java-home
java-home:
ifndef JAVA_HOME
ifeq ($(UNAME), Darwin)
	$(eval JAVA_HOME=$(shell find /Library/Java/JavaVirtualMachines -name 'jdk1.8.0_*' -type d -maxdepth 1 | sort | tail -n1)/Contents/Home)
endif
endif

.PHONY: mvn-version
mvn-version: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw --version

.PHONY: clean
clean: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw clean
	find . -name '*.class' -delete

.PHONY: package
package: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw package -DskipTests

.PHONY: tool
tool: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw -pl iceworm-tool -am package -DskipTests

.PHONY: test
test: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw test

.PHONY: install
install: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw install -DskipTests

.PHONY: uninstall
uninstall: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw dependency:purge-local-repository -DmanualInclude="com.wrmsr.iceworm"

.PHONY: dep-tree
dep-tree: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw dependency:tree

.PHONY: dep-updates
dep-updates: java-home
	JAVA_HOME=$(JAVA_HOME) ./mvnw -N versions:display-dependency-updates
