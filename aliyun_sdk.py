#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

import json


def list_domain_records(client, domain_name):
    request = DescribeSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_SubDomain(domain_name)
    response = client.do_action_with_exception(request)
    response = response.decode()
    return json.loads(response)['DomainRecords']['Record']

def add_domain_record(client, domain_name, sub_name, dtype, value):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain_name)
    request.set_RR(sub_name)
    request.set_Type(dtype)
    request.set_Value(value)

    response = client.do_action_with_exception(request)
    response = response.decode()
    response = json.loads(response)
    if "RecordId" in response:
        return response['RecordId']
    return None

def update_domain_record(client, record_id, sub_name, dtype, value):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId(record_id)
    request.set_RR(sub_name)
    request.set_Type(dtype)
    request.set_Value(value)

    response = client.do_action_with_exception(request)
    response = response.decode()
    response = json.loads(response)
    if "RecordId" in response:
        return response['RecordId']
    return None

