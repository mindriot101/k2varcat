deploy:
	k2var-freeze --root '/phsnag/' && rsync -vaz --exclude '*.fits' build/ norwood.astro:www/
