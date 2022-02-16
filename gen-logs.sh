#!/bin/bash
LOGDIR=$HOME'/log'
FNAME=''
FNAME_P1='/smbp_2022'
FNAME_P2='_app01.log'
FNAME_RND_MONTH=''
FNAME_RND_DAY=''
FILES_CNT=20
RANGE_MONTH=3
RANGE_DAY=30
LOG_TYPE=0
LOG_MSG=''

while [ $FILES_CNT -gt 0 ]; do
   let "FNAME_RND_MONTH = $RANDOM % $RANGE_MONTH"
   let "FNAME_RND_DAY = $RANDOM % RANGE_DAY"
   LINES_CNT=70

   if [ $FNAME_RND_MONTH -eq 0 ]; then
      FNAME_RND_MONTH='1'
   else
      if [ $FNAME_RND_MONTH -lt 10 ]; then
         FNAME_RND_MONTH='0'$FNAME_RND_MONTH
      fi
   fi

   if [ $FNAME_RND_DAY -eq 0 ]; then
      FNAME_RND_DAY='1'
   else
      if [ $FNAME_RND_DAY -lt 10 ]; then
         FNAME_RND_DAY='0'$FNAME_RND_DAY
      fi
   fi

   FNAME=$LOGDIR''$FNAME_P1''$FNAME_RND_MONTH''$FNAME_RND_DAY'_'$RANDOM''$FNAME_P2
   touch $FNAME
   while [ $LINES_CNT -ge 0 ]; do
       let "LOG_TYPE = $RANDOM % 3"
       if [ $LOG_TYPE -eq 0 ];then
          LOG_MSG='Success'
       fi
       if [ $LOG_TYPE -eq 1 ];then
          LOG_MSG='Info'
       fi
       if [ $LOG_TYPE -eq 2 ];then
          LOG_MSG='Error'
       fi
       echo "$RANDOM/$FNAME_RND_MONTH/$FNAME_RND_DAY $LOG_MSG Log from ip:.....  service....." >> $FNAME 
       let "LINES_CNT -= 1"
   done
   gzip $FNAME

   let "FILES_CNT -= 1"
done
ls $LOGDIR
