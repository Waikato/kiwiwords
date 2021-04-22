all: aotearoa-nz.png

aotearoa-nz.png: aotearoa-nz.r aotearoa-nz.csv
	Rscript aotearoa-nz.r

aotearoa-nz.csv: aotearoa-nz.py gaz_names.csv
	python3 aotearoa-nz.py

gaz_names.csv:
	curl https://www.linz.govt.nz/system/files_force/media/file-attachments/gaz_names.csv --output $(@)

