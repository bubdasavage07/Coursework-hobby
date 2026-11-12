# Quiz 2

## 1. What is the main Internet Protocol version in use today?
A. IPv2
B. IPv6
C. IPv4
D. IPv3

## 2. Which IPv4 header component specifies QoS?
A. Protocol Identifier
B. Differentiated Services Control Point field
C. Time to Live
D. Header Checksum

## 3. How can the ECN field be used?
A. Identify source address
B. Determine packet size
C. Set handling priority
D. Notify destination of congestion

## 4. Distinguish application message and packet fragmentation.
A. Both occur only at destination
B. Application fragmentation occurs at source transport layer
C. Both occur only at source
D. Both occur at network layer

## 5. When are IP identification, flags, and fragment offset used?
A. Error detection
B. Router fragmentation and destination reassembly
C. QoS settings
D. Routing decisions

## 6. Why were fragmentation fields not studied in detail?
A. Not relevant today
B. Too complex
C. Only IPv6 uses them
D. Fragmentation is obsolete and rarely needed

## 7. Does IPv6 allow packet fragmentation?
A. No
B. Yes, if a router requests it
C. Yes, for all packets
D. Yes, but only large packets

## 8. What does a router do with TTL 2?
A. Reduces it to 1 before forwarding
B. Returns packet to source
C. Discards it immediately
D. Increases it to 3

## 9. What does a router do with TTL 1?
A. Increases it to 2
B. Reduces it to 0 and discards it
C. Sends it to source
D. Forwards it

## 10. What does the Protocol Field tell the destination host?
A. Packet importance
B. Packet route
C. Sender address
D. What the data field contains

## 11. What happens when the destination process sees 17 in the Data Field?
A. TCP segment
B. Discard
C. UDP datagram passed to UDP
D. Forwarded

## 12. What problem does IPv4 option handling cause?
A. Restricts routing
B. Inconsistent and resource-intensive processing
C. Reduces vulnerabilities
D. Limits packet size

## 13. What IPv4 problem was IPv6 created to solve?
A. Address exhaustion
B. Reliability
C. Security flaws
D. Speed

## 14. How does IPv6 solve IPv4's main problem?
A. Dynamic addressing
B. Shorter addresses
C. Routing efficiency
D. 128-bit addresses and a larger address space

## 15. What has held back IPv6 adoption?
A. Cost and effort of migration
B. Lack of awareness
C. Technical limitations
D. Regulations

## 16. Why are IPv6 addresses simplified?
A. Security
B. Speed
C. Packet size
D. Easier human reading

## 17. Why follow IPv6 simplification rules precisely?
A. Routing efficiency
B. Security protocols
C. Canonical form makes searches match
D. Prevent duplication

## 18. Are simplified IPv6 addresses uppercase or lowercase?
A. Lowercase
B. Any format
C. Mixed case
D. Uppercase

## 19. Are simplified IPv6 addresses decimal or hexadecimal?
A. Hexadecimal
B. Decimal
C. Octal
D. Binary

## 20. How many hex digits are in an IPv6 field?
A. 2
B. 16
C. 4
D. 8

## 21. How many bits are in an IPv6 field?
A. 4
B. 16
C. 8
D. 32

## 22. How are IPv6 fields separated?
A. Periods
B. Spaces
C. Dashes
D. Colons

## 23. How many fields are in an IPv6 address?
A. 8
B. 4
C. 16
D. 6

## 24. Canonical form of `2001:0ed2:056b:00d3:000c:abcd:0bcd:0fe0`?
A. `2001:0ed2:56b:d3:0c:abcd:bcd:0fe0`
B. `2001:0ed2:056b:00d3:000c:abcd:0bcd:0fe0`
C. `2001:ed2:56b:d3:c:abcd:bcd:fe0`
D. `2001:ed2:056b:d3:c:abcd:bcd:fe0`

## 25. Canonical form of `2001:0002:0000:0000:0000:abcd:0bcd:0fe0`?
A. `2001:2::abcd:bcd:fe0`
B. `2001:02::abcd:bcd:fe`
C. `2001:2:0:0:abcd:bcd:fe0`
D. `2001::2:abcd:bcd:fe0`

## 26. Simplify `2001:0000:0000:00fe:0000:0000:0000:cdef`.
A. `2001:0:0:fe:0:0:0:cdef`
B. `2001::fe::cdef`
C. `2001:0:0:fe::cdef`
D. `2001::fe:0:0:0:cdef`

## 27. Simplify `2001:0000:0000:00fe:0000:0000:ba5a:cdef`.
A. `2001::fe:ba5a:cdef`
B. `2001::fe:0:0:ba5a:cdef`
C. `2001:0:0:fe:0:0:ba5a:cdef`
D. `2001::fe:0:ba5a:cdef`

## 28. What is the advantage of strict IPv6 simplification?
A. Consistent strings for accurate searching
B. Convenience
C. Security
D. Memory reduction

## 29. Which RFC defines IPv6 canonical form?
A. RFC 4291
B. RFC 791
C. RFC 1035
D. RFC 5952

## 30. How do IPv4 and IPv6 Version Number Fields differ?
A. IPv4 0100; IPv6 0110
B. IPv4 0100; IPv6 1000
C. Both 0110
D. IPv4 0110; IPv6 0111

## 31. What is the Diffserv subfield's purpose?
A. Source ID
B. QoS
C. Packet size
D. Integrity

## 32. What is the Flow Label Field's purpose?
A. Mark packets for the same QoS treatment
B. Destination address
C. Source ID
D. Integrity validation

## 33. How does an IPv6 receiver determine packet length?
A. Header length
B. Total length
C. Data length
D. Payload length

## 34. Does Payload Length include extension headers?
A. Only extension headers
B. Only main header
C. Everything beyond the main header
D. Only data field

## 35. How is Hop Limit used?
A. Packet size
B. Like TTL; decrement and discard at zero
C. Protocol type
D. Priority

## 36. Does IPv6 have a header checksum?
A. Yes, error checking
B. No
C. Yes, routing
D. Yes, integrity

## 37. Benefit of no IPv6 header checksum?
A. Simple design
B. Security
C. Smaller packet
D. Reduced router processing time

## 38. Why are IPv4 options undesirable?
A. Reduce security
B. Increase size
C. Limit routing
D. Unsystematic and slow to process

## 39. Why are optional extension headers desirable?
A. Addressing
B. Consistent structure; routers can ignore most
C. Security
D. Size

## 40. Which extension header must routers usually consider?
A. Destination options
B. Routing
C. Fragment
D. Hop-by-hop options

## 41. What Next Header value indicates a UDP datagram follows?
A. 8
B. 1
C. 17
D. 6

## 42. What follows a Next Header value of 0?
A. Hop-by-hop options
B. Destination options
C. Fragment header
D. Routing header

## 43. Why are payload and data field not synonymous?
A. Same size
B. Unrelated headers
C. Different checksums
D. Payload includes upper-layer data and extension headers

## 44. With an X-bit subnet part, how many subnets are possible?
A. 2^X
B. X^2 − 1
C. 2^X − 2
D. 2X

## 45. With a 9-bit subnet part, how many subnets are possible?
A. 510
B. 1024
C. 512
D. 256

## 46. With a 16-bit subnet part, how many subnets are possible?
A. 128
B. 64
C. 30
D. 64536

## 47. With a 16-bit network part, how many hosts are possible?
A. 65536
B. 65534
C. Always 1
D. Cannot be determined

## 48. At what layer is ICMP used?
A. TCP/IP supervisory protocols
B. Data-link layer
C. Transport layer
D. Application layer

## 49. Distinguish ICMP error advisement and control messages.
A. Both control
B. Both error advisement
C. Both routing only
D. Errors report an error; control messages instruct behavior changes

## 50. What ICMP message types does ping use?
A. Echo request and Echo error
B. Echo reply and Echo success
C. Ping request and Ping reply
D. Echo request and Echo reply

## 51. What security concern comes from ICMP error advisement and echo responses?
A. Packet capture
B. Router configuration exposure
C. Attackers can identify reachable IP addresses
D. Data corruption

## 52. With an 8-bit network part, what subnet part is needed for at least 250 subnets?
A. 8 bits
B. 6 bits
C. 9 bits
D. 7 bits

## 53. With an 8-bit network part and 8-bit subnet part, hosts per subnet?
A. 65534
B. 65536
C. Cannot be determined
D. Always 1

## 54. With an 18-bit network part, subnet bits for at least 16 subnets?
A. 3
B. 5
C. 4
D. 6

## 55. With an 18-bit network part and 4-bit subnet part, hosts per subnet?
A. 1024
B. 512
C. 510
D. 1022

## 56. With a 22-bit network part, subnet bits for at least 10 subnets?
A. 5
B. 3
C. 4
D. 6

## 57. With a 22-bit network part and 4-bit subnet part, hosts per subnet?
A. 126
B. 62
C. 60
D. 30

# Correct Answers
1. C
2. B
3. D
4. B
5. B
6. D
7. D
8. A
9. B
10. D
11. C
12. B
13. A
14. D
15. A
16. D
17. C
18. A
19. A
20. C
21. B
22. D
23. A
24. C
25. A
26. C
27. B
28. A
29. D
30. A
31. B
32. A
33. D
34. C
35. B
36. B
37. D
38. D
39. B
40. D
41. C
42. A
43. D
44. A
45. C
46. D
47. B
48. A
49. D
50. D
51. C
52. A
53. A
54. C
55. D
56. C
57. B
