##test case for filter_packet.py code


1- first you need to execute the code in root privilege,             
2- add rules or use the default rules             
3- you can remove rules          
4- view the existing rules, there will be a firewall_log.txt file which will be created
to hold firewall rules and logs of the blocked packets      
5- start monitoring to test the firewall rules, use a browser or ping to try to reach google.com or any
other website, once the rules matched, the logs will be logged in firewall_log.txt with the timestamp


here an example, where I used the default rules, then used a browser to reach google.com
![test-1](https://github.com/user-attachments/assets/b27f934b-7034-49b5-a638-5f922a40e615)







once I started the monitoring, the logs logged into the firewall_log.txt
![Screenshot_2025-01-19_11_30_59](https://github.com/user-attachments/assets/362c1473-e9e6-4a4b-b688-8f3503dd3e03)

