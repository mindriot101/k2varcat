all: print-help

print-help:
	@echo "Tasks: $(shell grep -E '^.+:$$' Makefile | sed 's/://g')"

deploy:
	k2var-freeze --root '/phsnag/' && rsync -vaz --exclude '*.fits' build/ norwood.astro:www/

deploy-local:
	k2var-freeze --root '/phsnag/' && rsync -va build/ $(HOME)/www/
