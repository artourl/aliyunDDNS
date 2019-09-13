from aliyun_sdk import list_domain_records, add_domain_record, update_domain_record
from get_wan_ip import get_wan_ip
import json
import logging
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException


path = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger("ip_updater")
handler1 = logging.StreamHandler()
handler2 = logging.FileHandler(filename=os.path.join(path, "alyDDNS.log"))

logger.setLevel(logging.INFO)
handler1.setLevel(logging.INFO)
handler2.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler1.setFormatter(formatter)
handler2.setFormatter(formatter)

logger.addHandler(handler1)
logger.addHandler(handler2)


f = open(os.path.join(path, 'alyDDNS.json'))
config = json.load(f)
f.close()
client = AcsClient(config['access_key'], config['access_secret'], 'cn-hangzhou')

ip = get_wan_ip()
if not ip:
    logger.info('can not get ip, abort')
logger.info('local wan ip: ' + ip)

for sub in config['sub']:
    domain_name = sub + '.' + config['domain']
    logger.info('run update for domain: ' + domain_name)
    records = list_domain_records(client, domain_name)
    exist = False
    rid = None
    for record in records:
        if record['Type'] == 'A':
            exist = True
            rid = record['RecordId']
            old_ip = record['Value']
    if not exist:
        logger.info("no previous ipv4 record exist, add a new one")
        add_domain_record(client, config['domain'], sub, 'A', ip)
    elif old_ip != ip:
        logger.info("ip changed, update")
        res = update_domain_record(client, rid, sub, 'A', ip)
    else:
        logger.info("same ip, do nothing")



        
