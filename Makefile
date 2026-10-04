# Rebuild everything from the raw downloads in data/raw/.
#   make            the whole chain: data -> checks -> notebooks -> slides -> viva notes
#   make data       processed datasets only
#   make slides     slide figures, tables and both PDFs
# Needs Python (see requirements.txt) and a TeX Live install with latexmk.

PY      := python3
NB      := notebooks
DECK    := presentation

.PHONY: all data validate notebooks check slides viva overleaf clean

all: data validate notebooks check slides viva overleaf

data:
	$(PY) src/build_dataset.py
	$(PY) src/write_sources.py

validate:
	$(PY) src/validate_dataset.py

# each notebook is re-run in place so the outputs shown on GitHub are the current ones
notebooks:
	cd $(NB) && for f in 0*.ipynb; do \
		jupyter nbconvert --to notebook --execute --inplace "$$f" || exit 1; \
	done

# recompute every number quoted in the slides and notes from the raw files (docs/number_check.md)
check:
	$(PY) src/check_numbers.py

slides:
	$(PY) src/slide_figures.py
	cd $(DECK) && latexmk -pdf -interaction=nonstopmode slides.tex
	cd $(DECK) && latexmk -pdf -interaction=nonstopmode -jobname=slides_with_notes \
		-usepretex='\def\withnotes{}' slides.tex

viva:
	$(PY) src/build_viva_pdf.py

# the zip people upload to Overleaf: the deck source and everything it inputs
overleaf:
	cd $(DECK) && rm -f overleaf_upload.zip && zip -r -X -q overleaf_upload.zip slides.tex figures tables

clean:
	cd $(DECK) && latexmk -c slides.tex && latexmk -c -jobname=slides_with_notes slides.tex
