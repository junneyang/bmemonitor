grep 'zhixin New as params' zhixin.log.2015020212 | awk -F'[][]' 'BEGIN {} {
split($1,a," ")
split($23,b,"params,")
print a[2]" "a[3]"\t"$6"\t"b[2]"\t"$total
}
END {}'

cat zhixin.log.2015020212 | while read line
do
a=`echo ${line} | awk  '{print $2}'`
b=`echo ${line} | awk  '{print $4}'`
c=`sed -n "/${a}/p" file2`
if [ $b -gt 10 ]
then
...
else
...
fi
....
done

grep 'zhixin New as params' zhixin.log.2015020212 | awk -F'[][]' 'BEGIN {} {
split($1,a," ")
split($23,b,"params,")
print a[2]" "a[3]"\t"$6"\t"b[2]
}
END {}'

'3371190920': {
	'as_delay': 14, 
	'original_query': '\xe6\x96\xb0\xe5\x9f\x8e\xe5\xb8\x8c\xe5\xb0\x94\xe9\xa1\xbf\xe9\x85\x92\xe5\xba\x97', 
	'as_null': 1, 
	'zhixin_delay': 47, 
	'keyword': '\xe6\x96\xb0\xe5\x9f\x8e\xe5\xb8\x8c\xe5\xb0\x94\xe9\xa1\xbf\xe9\x85\x92\xe5\xba\x97', 
	'req_type': '3', 
	'city_id': '100010000', 
	'zhixin_null': 0, 
	'srcID': '28027'
}

