#!/usr/bin/env python3

import subprocess
import re

from time import sleep
from tracemalloc import Snapshot
from prometheus_client import start_http_server
from prometheus_client import Gauge

memRss = Gauge('processes_mem_rss', 'Memory consumption by process (RSS)', ['command', 'pid'])

def collectMetrics():
    rawRssData = subprocess.run(["ps", "-axm", "-o rss,pid,comm"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines = True).stdout.split('\n')

    for rss in rawRssData:
        m = re.search("\s*(\d*)\s(\d*)\s(.*)", rss)

        if not m or not m.group(1) or not m.group(2) or not m.group(3):
            continue
        
        memRss.labels(m.group(3), m.group(2)).set(m.group(1))
    
if __name__ == '__main__':
    port=9160
    start_http_server(port)
    
    print('Prometheus server started on port', port)

    while True:
        collectMetrics()
        sleep(1)

