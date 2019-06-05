for file in text/AA/*.txt
do
	echo python3 jp-period-split.py $file > "${file}.tmp"
	python3 jp-period-split.py $file > "${file}.tmp"

	echo rm $file
	rm $file
	echo mv ${file}.tmp $file
	mv ${file}.tmp $file
done
