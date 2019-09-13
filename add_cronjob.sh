path=$(cd `dirname $0`; pwd)
crontab -l > tmp_cron 
echo "*/10 * * * * /usr/bin/python3 $path/main.py" >> tmp_cron
crontab tmp_cron
rm -f tmp_cron
