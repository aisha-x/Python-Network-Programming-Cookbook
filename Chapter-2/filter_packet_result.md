##Test case for filter_packet.py code


1- first you need to execute the code in root privilege,             
2- specify the interface you want to monitor                        
3- add rules or use the default rules          
4- view the existing rules, there will be a firewall_log.txt file that will be created
to hold firewall rules and logs of the blocked packets      
5- start monitoring to test the firewall rules, use a browser or ping to try to reach google.com or any
other website, once the rules are matched, the logs will be logged in firewall_log.txt with the timestamp


here is an example, where I used the default rules, then used a browser to reach google.com


![test-1](https://github.com/user-attachments/assets/b27f934b-7034-49b5-a638-5f922a40e615)







once I started the monitoring, the logs logged into the firewall_log.txt


![Screenshot_2025-01-19_13-03-26](https://github.com/user-attachments/assets/f6f46e66-999c-4989-b73c-709b5ddb44d5)



