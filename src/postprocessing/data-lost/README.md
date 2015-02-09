cat /Users/nsaez/pucthesis/datasets/README.md |sed 's/-/_/g' |awk '{print "python id_deri_vs_time.py -e "$2" /Users/nsaez/datasets/"$2"/lotuce2-run-results-"$12"."$14".txt &"}' |tail -n 8
