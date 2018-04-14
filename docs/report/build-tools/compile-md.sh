cd `dirname $0`
cd .. # brings us level with all the md files

outdir="./output"

echo "###### BUILD: `date`" > $outdir/out.md

cat intro.md >>  $outdir/out.md
cat sentiment-analysis.md >>  $outdir/out.md
cat design.md >>  $outdir/out.md
cat implementation.md >>  $outdir/out.md
cat pre-processing.md >>  $outdir/out.md
cat machine-learning.md >>  $outdir/out.md
cat multinomial-naive-bayes.md >>  $outdir/out.md
cat code-quality.md >>  $outdir/out.md
cat project-management.md >>  $outdir/out.md
cat user-feedback.md >>  $outdir/out.md
cat results.md >>  $outdir/out.md
cat conclusion.md >>  $outdir/out.md
cat references.md >>  $outdir/out.md
cat appendix.md >>  $outdir/out.md

# md -> pdf
pandoc --pdf-engine=xelatex \
       --toc \
       --highlight-style=./build-tools/custom.theme \
       -V papersize:a4 \
       -V fontsize=12pt \
       -V geometry:margin=2.3cm \
       -V documentclass:article \
       -M title='Sentiment Analysis in Divisive Domains' \
       -M author='David Byrne' \
       -M date='April 2018' \
       -M modified='`date`' \
       -M institute='NUI Galway' \
       -M subtitle='Creating a microservices based, machine learning pipeline for real-time sentiment analysis of Twitter data' \
       -M keywords='Sentiment Analysis',' Machine Learning',' Divisive Domains',' Twitter' \
       -f gfm \
       -s $outdir/out.md \
       -o $outdir/out.pandoc.pdf

# md -> tex
pandoc --toc \
       --highlight-style=./build-tools/custom.theme \
       -V papersize:a4 \
       -V fontsize=12pt \
       -V geometry:margin=2.3cm \
       -V documentclass:article \
       -M title='Sentiment Analysis in Divisive Domains' \
       -M author='David Byrne' \
       -M date='April 2018' \
       -M modified='`date`' \
       -M institute='NUI Galway' \
       -M subtitle='Creating a microservices based, machine learning pipeline for real-time sentiment analysis of Twitter data' \
       -M keywords='Sentiment Analysis',' Machine Learning',' Divisive Domains',' Twitter' \
       -f gfm \
       -t latex \
       -s $outdir/out.md  \
       -o $outdir/out.pandoc.tex

# md -> docx
pandoc --toc \
       --highlight-style=./build-tools/custom.theme \
       -V papersize:a4 \
       -V fontsize=12pt \
       -V geometry:margin=2.3cm \
       -V documentclass:article \
       -M title='Sentiment Analysis in Divisive Domains' \
       -M author='David Byrne' \
       -M date='April 2018' \
       -M modified='`date`' \
       -M institute='NUI Galway' \
       -M subtitle='Creating a microservices based, machine learning pipeline for real-time sentiment analysis of Twitter data' \
       -M keywords='Sentiment Analysis',' Machine Learning',' Divisive Domains',' Twitter' \
       -f gfm \
       -s $outdir/out.md \
       -o $outdir/out.pandoc.docx



# We can't just go from LaTeX to each of the other formats due to a bug in the
# Pandoc LaTeX parser with the _ character https://github.com/jgm/pandoc/issues/4473
# Hence we just go from md -> * with the same config each time

