all: 
	#cd figs && convert bpref.eps bpref.png && cd ..
	#cd tmp && sh 25.sh > 25.tex && cd ..
	#cd tmp && sh top.sh > top.tex && cd ..
	#latex paper.tex 
	#bibtex paper
	#latex paper.tex 
	#latex paper.tex
	#dvips paper.dvi -o paper.ps
	#ps2pdf paper.ps
	#pdflatex paper
	pdflatex ribas2015ictir

perm:
	chmod -R g+rwx *

run: clean all 
	gv llncs.ps &
clean:
	rm *.aux *.bbl *.blg *.log *.toc *.ps *.pdf *.dvi *~ *.backup *.bak

