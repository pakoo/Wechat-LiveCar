#!/bin/bash 

function rand(){  
    min=$1  
    max=$(($2-$min+1))  
    num=$(($RANDOM+1000000000)) #增加一个10位的数再求余  
    echo $(($num%$max+$min))  
}  

live_room_id=$(rand 10000 99999) 

room_id="CAR_"$live_room_id
ffroom=rtmp://{{live_server_host}}/live/$room_id

echo $room_id
echo $ffroom

python twss.py $room_id > twss.log &

ffmpeg -thread_queue_size 512 -f v4l2 -i /dev/video0   -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -acodec aac -ab 128k -strict experimental  -aspect 16:9 -vcodec h264 -preset superfast -crf 25 -pix_fmt yuv420p -g 15 -vb 820k -maxrate 820k  -profile:v baseline  -r 30 -f flv $ffroom  &



