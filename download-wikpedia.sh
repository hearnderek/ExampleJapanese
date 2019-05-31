wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 
bzip2 -d jawiki-latest-pages-articles.xml.bz2 
python WikiExtractor.py jawiki-latest-pages-articles.xml

rm jawiki-latest-pages-articles.xml

for file in text/AA/*
do
	python3 jp-period-split.py $file > "${file}.txt"
	rm $file
done
