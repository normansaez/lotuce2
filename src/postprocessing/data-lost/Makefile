all:clean id_der hist id_t
	@echo "Makeing all images"
#	mkdir -p img/
#	mv *.png img/
id_der:
	@echo "Doing delta ids for all"
	python id_deri_vs_time.py -f /Users/nsaez/datasets/A/lotuce2-run-results-2015_01_23.11.txt &
	python id_deri_vs_time.py -f /Users/nsaez/datasets/B/lotuce2-run-results-2015_01_24.12.txt &
	python id_deri_vs_time.py -f /Users/nsaez/datasets/C/lotuce2-run-results-2015_02_05.1.txt -s /Users/nsaez/datasets/F/lotuce2-run-results-2015_02_04.0.txt &
	python id_deri_vs_time.py -f /Users/nsaez/datasets/D/lotuce2-run-results-2015_02_05.0.txt -s /Users/nsaez/datasets/G/lotuce2-run-results-2015_02_04.1.txt &
	python id_deri_vs_time.py -f /Users/nsaez/datasets/E/lotuce2-run-results-2015_02_06.2.txt -s /Users/nsaez/datasets/H/lotuce2-run-results-2015_02_05.2.txt &
clean:
	rm -fr *.png
	rm -fr img/
hist:
	python histograma.py -f ~/datasets/C/lotuce2-run-results-2015_02_05.1.txt -s ~/datasets/F/lotuce2-run-results-2015_02_04.0.txt &
	python histograma.py -f ~/datasets/D/lotuce2-run-results-2015_02_05.0.txt -s ~/datasets/G/lotuce2-run-results-2015_02_04.1.txt &
	python histograma.py -f ~/datasets/E/lotuce2-run-results-2015_02_06.2.txt -s ~/datasets/H/lotuce2-run-results-2015_02_05.2.txt &
id_t:
	@echo "Doing delta ids for all"
	python id_vs_time.py -f /Users/nsaez/datasets/A/lotuce2-run-results-2015_01_23.11.txt &
	python id_vs_time.py -f /Users/nsaez/datasets/B/lotuce2-run-results-2015_01_24.12.txt &
	python id_vs_time.py -f /Users/nsaez/datasets/C/lotuce2-run-results-2015_02_05.1.txt -s /Users/nsaez/datasets/F/lotuce2-run-results-2015_02_04.0.txt &
	python id_vs_time.py -f /Users/nsaez/datasets/D/lotuce2-run-results-2015_02_05.0.txt -s /Users/nsaez/datasets/G/lotuce2-run-results-2015_02_04.1.txt & 
	python id_vs_time.py -f /Users/nsaez/datasets/E/lotuce2-run-results-2015_02_06.2.txt -s /Users/nsaez/datasets/H/lotuce2-run-results-2015_02_05.2.txt & 
