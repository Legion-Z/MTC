#!/bin/bash
LOGDIR=$HOME'/log'
CURRENT_MONTH=$(date +'%Y%m')
CURRENT_DAY=$(date +'%Y%m%d')
TOTAL_SUCCESS=0

for FNAME in $LOGDIR'/*_'$CURRENT_MONTH'*.gz'; do
	gzip -k -d -c  $FNAME | grep Error > $LOGDIR'/Error.log'

done

for FNAME in $LOGDIR'/*_'$CURRENT_DAY'*.gz'; do
	SUCCESS=$(gzip -k -d -c  $FNAME | grep -c Success)
	let "TOTAL_SUCCESS += $SUCCESS" 

done
echo "total count of success messages is $TOTAL_SUCCESS"
