#test case for filter_packet.py code
###############

1- first you need to execute the code in root privilege,             
2- add rules or use the default rules             
3- you can remove rules          
4- view the existing rules, there will be a firewall_log.txt file which will be created
to hold firewall rules and logs of the blocked packets      
5- start monitoring to test the firewall rules, use a browser or ping to try to reach google.com or any
other website, once the rules matched, the logs will be logged in firewall_log.txt with the timestamp


here an example, where I used the default rules, then used a browser to reach google.com

![test-1.png](../../../../../Pictures/test-1.png)






once I started the monitoring, the logs logged into the firewall_log.txt

![Screenshot_2025-01-19_11_30_59.png](../../../../../Pictures/Screenshot_2025-01-19_11_30_59.png)