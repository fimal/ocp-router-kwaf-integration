from ipaddress import IPv4Address
from pip import main
from requests import Request, Session
from haproxyspoa.payloads.ack import AckPayload
from haproxyspoa.spoa_server import SpoaServer
import argparse
import signal
import sys


def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN) # ignore additional signals
    print("Recieved Ctrl+C to exit")
    sys.exit(0)

agent = SpoaServer()

@agent.handler("mirror")
async def handle_mirror(arg_method: str, arg_ver: str, arg_path: str, src: IPv4Address, req_host: str, arg_hdrs: str, arg_body: str):
    headers = {}
    for header in arg_hdrs.split('\r\n'):
        #print(f'header - {header}')
        if header:
            #print(f'header - {header}')
            key, value = header.split(':', maxsplit=1)
            headers[key.strip()] = value.strip()
    kwaf_ip='http://'+main_args.enforcer_svc_host+':'+main_args.enforcer_svc_port
    print(kwaf_ip)
    s = Session()
    req = Request(arg_method, kwaf_ip+arg_path, data=arg_body, headers=headers)
    prepped = req.prepare()
    resp = s.send(prepped,
        # stream=stream,
        # verify=verify,
        # proxies=proxies,
        # cert=cert,
        # timeout=timeout
    )
    print(f'response - {resp.status_code}')
    response=''
    for line in resp.content.decode().split('\n'):
        response=(response+line)
        #print(f'response - {resp.content}')
    return AckPayload().set_txn_var("response", bytes(response, 'utf-8'))
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) # register the signal with the signal handler first
    parser = argparse.ArgumentParser(description='This is implementation of SPOA for KWAF')
    parser.add_argument('--enforcer_svc_host', help='kwaf enforcer service fqdn host', required=False, default="waas-enforcer-service.kwaf.svc")
    parser.add_argument('--enforcer_svc_port', help='kwaf enforcer service port', required=False, default="31012")
    main_args = parser.parse_args()
    agent.run(host='0.0.0.0', port=9008)