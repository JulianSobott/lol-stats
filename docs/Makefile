.PHONY: pdf
pdf:
	docker run --rm -v "`pwd`/latex-documentation":/src -v "`pwd`/pdf":/pdf debian-texlive


.PHONY: pdf
docker_image:
	docker build -t debian-texlive build