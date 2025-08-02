# test case for filter_packet.py code


1. First, you need to execute the code in root privilege,
2. Add rules or use the default rules
3. You can remove rules
4. View the existing rules. There will be a firewall_log.txt file, which will be created to hold firewall rules and logs of the blocked packets
5. Start monitoring to test the firewall rules, use a browser or ping to try to reach `google.com`, once the rules match, the logs will be logged in firewall_log.txt with the timestamp

