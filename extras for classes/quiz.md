# Quiz

## 1. What four pieces of configuration information does a DHCP server typically provide?
A. IP address, subnet mask, encryption keys, firewall rules  
B. Client address, default gateway, local DNS servers, subnet mask  
C. NTP server, driver update, QoS settings, IP address  
D. MAC address, hostname, lease duration, proxy address

## 2. Why is it useful to configure a client every time it boots up?
A. DHCP provides current settings if network configuration changes  
B. It primarily speeds up operating-system startup  
C. It guarantees the same address every time  
D. It authenticates the user at startup

## 3. Describe NAT operation.
A. It creates virtual addresses without translation  
B. It encrypts every IP header field  
C. It converts IPv4 addresses into IPv6 addresses  
D. It translates private internal addresses to a public address and maps responses back

## 4. What are the two benefits of NAT?
A. It hides internal addresses and conserves public addresses  
B. It guarantees lower latency  
C. It removes administrator involvement  
D. It eliminates the need for security appliances

## 5. How does NAT enhance security?
A. It limits bandwidth through rate control  
B. It encrypts packets end-to-end  
C. It performs deep packet inspection without policies  
D. It hides internal addresses and ephemeral ports from outside observers

## 6. How does NAT help a firm deal with an ISP IP-address shortage?
A. It periodically rotates public addresses  
B. It lets many private devices share one public address for outbound traffic  
C. It permanently combines devices  
D. It doubles capacity with separate external ranges

## 7. How are private IP address ranges used?
A. They are used internally and are not routed on the public Internet  
B. They are reserved exclusively for VPNs  
C. They are publicly routable without translation  
D. They automatically provide confidentiality and authentication

## 8. Is NAT transparent to the operating systems of the two hosts involved?
A. No; both need special drivers  
B. Only the internal host is unaware  
C. Yes; both communicate normally without awareness of the translation  
D. Only the external host is unaware

## 9. Is NAT transparent to all applications?
A. Yes; in general, applications operate without awareness of NAT  
B. Only enterprise applications work  
C. Only web applications work  
D. Most applications require explicit NAT support

## 10. What server will your local DNS server contact if it does not know the IP address of a host?
A. The authoritative server for the host's domain  
B. A random caching resolver  
C. A root server that stores every hostname directly  
D. Another local LAN server

## 11. Does the client know that its local DNS server contacted another DNS server to obtain an IP address?
A. No; the client always gets a direct authoritative response  
B. Yes; it automatically traces the entire query path  
C. No; it receives the local resolver's reply and is unaware of upstream contacts  
D. Yes; diagnostic utilities cause this during ordinary lookups

## 12. Is DNS only used to send back IP addresses for host names? Explain.
A. Yes; DNS exclusively returns IP addresses  
B. Yes; DNS is limited to IPv4  
C. No; DNS supports many record types, including services, keys, aliases, and mail routing  
D. No; DNS returns hardware MAC addresses

## 13. What is a domain?
A. A contiguous range of IP addresses  
B. A collection of named resources administered as a unit within the DNS hierarchy  
C. A DNS text-record type  
D. A transport-layer protocol

## 14. Distinguish between the DNS root and top-level domains.
A. Root servers anchor the hierarchy; TLDs such as .com and .edu categorize namespaces and delegate authority  
B. Every TLD server is identical to a root server  
C. Root servers and TLDs are the same infrastructure  
D. TLDs handle only local intranet names

## 15. What are the two types of top-level domains?
A. Generic TLDs and country-code TLDs  
B. Root domains and generic domains  
C. Local domains and global domains  
D. Country domains and international domains

## 16. Which level of domain name do corporations most wish to have?
A. A second-level domain  
B. A root-level domain  
C. A third-level domain  
D. A subdomain

## 17. What are DNS root servers?
A. Local recursive resolvers  
B. Authoritative servers for individual domains  
C. Servers that store root certificate authorities  
D. The highest-level DNS servers, which provide referrals to TLD servers

## 18. How does a company or individual obtain a second-level domain name?
A. By setting up a personal DNS server  
B. By requesting it from its ISP  
C. By contacting ICANN directly  
D. By registering through an accredited domain registrar

## 19. What does a company need beyond a second-level domain name to have a website?
A. A separate domain exclusively for email  
B. DNS hosting and a web server to deliver content  
C. Proprietary networking protocols  
D. A DNS root server

## 20. Does a DNS server have one record for a particular domain including a host, or more than one?
A. It can maintain several records, including addresses, aliases, mail exchanges, and services  
B. It can store at most five records  
C. It can store at most three records  
D. It stores one consolidated record

## 21. What is the purpose of the A record?
A. To publish an IPv6 address  
B. To publish an IPv4 address  
C. To specify a canonical name for an alias  
D. To designate a mail server

## 22. What is the purpose of the AAAA record?
A. To indicate a canonical-name mapping  
B. To publish an IPv6 address  
C. To identify a mail-exchange server  
D. To publish an IPv4 address

## 23. What hosts are given static IP addresses?
A. Servers that provide shared services  
B. Routers using routing protocols  
C. Printers using DHCP reservations  
D. Ordinary DHCP clients

## 24. Why do servers need static IP addresses?
A. They directly encrypt traffic  
B. They inherently improve processing speed  
C. They force DNS records to cache forever  
D. Clients can reliably locate services and DNS records remain valid

## 25. What are dynamic IP addresses?
A. Addresses reserved solely for printers  
B. Permanent server addresses  
C. Temporary DHCP-assigned addresses that may change when leases expire  
D. Backup failover addresses

## 26. How do clients get dynamic IP addresses?
A. By querying DNS  
B. By obtaining leases from DHCP servers  
C. By receiving unchanging static assignments  
D. By manually entering every setting

## 27. Can a client send DHCP request information to multiple DHCP servers?
A. No; it must unicast to one configured server  
B. Yes; DHCP discovery broadcasts allow reachable servers to receive and offer a lease  
C. Yes; but only with explicit client configuration  
D. Yes; but only two servers may respond

## 28. Do DHCP servers update the configuration information they store automatically?
A. No; they cannot be changed manually  
B. Yes; they continuously scan and rewrite scopes  
C. No; configured scopes and options remain until an administrator changes them  
D. Yes; clients can reprogram policies by packet

## 29. What are DHCP scopes?
A. A catalog of static device addresses  
B. Every IP address on the Internet  
C. A list of permanently reserved static addresses  
D. Defined address ranges and related DHCP options, such as masks, gateways, and leases

# Correct Answers

1. B
2. A
3. D
4. A
6. B
7. A
8. C
9. A
10. A
11. C
12. C
13. B
14. A
15. A
16. A
17. D
18. D
19. B
20. A
21. B
22. B
23. A
24. D
25. C
26. B
27. B
28. C
29. D
