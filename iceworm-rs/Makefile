all: build test

.PHONY: clean
clean:
	cargo clean

.PHONY: build
build:
	cargo build

.PHONY: test
test:
	cargo test

.PHONY: release
release:
	cargo build --release

.PHONY: arrow-rust
arrow-rust:
	curl -s https://raw.githubusercontent.com/apache/arrow/master/.env | egrep '^RUST=' | cut -d= -f2
