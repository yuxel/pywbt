# Python Web Benchmark Tool

A web benchmarking tool like [Apache Benchmark](http://httpd.apache.org/docs/2.0/programs/ab.html)

## Example usage

    python pywbt.py -n 100 -c 30 http://yuxel.net
     > Requests between  0 and 30  sent
     > Requests between  30 and 60  sent
     > Requests between  60 and 90  sent
     > Requests between  90 and 100  sent
     ------------------------------------------------- 
    Process took  9.61535310745 seconds ( 0.0961535310745  per/request)
    Number of succeeded requests  100
    Number of failed requests  0

