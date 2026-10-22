1. Which two layers standardize Ethernet and Wi-Fi operation?

A. Layers 1 and 4, the Physical and Transport layers, which combine media signaling with flow control, a pairing unrelated to standardized link operations for Ethernet or Wi‑Fi.

B. Layers 1 and 2, the Physical and Data Link layers, which define signaling on media and frame formats for Ethernet and Wi‑Fi across local networks.

C. Layers 2 and 3, the Data Link and Network layers, which jointly manage routing decisions but do not define physical signaling for Ethernet or Wi‑Fi transmission.

D. Layers 3 and 4, the Network and Transport layers, which handle logical addressing and end‑to‑end reliability rather than link signaling or local frame construction.
 
2. Which two layers standardize most of the Internet’s operation?

A. Layers 1 and 2, the Physical and Data Link layers, which concern local transmission details and frames, not internetwork routing or end‑to‑end transport behavior.

B. Layers 3 and 4, the Internet and Transport layers, which define IP forwarding and TCP/UDP communication for end‑to‑end delivery across heterogeneous internetworks.

C. Layers 2 and 2, repeated Data Link layers, which cannot govern IP routing or transport services across the Internet’s multiple autonomous networks.

D. Layers 5 and 6, the Session and Presentation layers, which manage dialogue control and data representation rather than packet forwarding or transport connections.
 
3. What do IP, TCP, and UDP govern?

A. The characteristics of physical cabling and radio channels, which determine signal encoding and media access rather than network routing or transport behavior.

B. The general transmission of packets and contents across any medium without addressing, sequencing, or ports, which is unrelated to standardized IP or transport functions.

C. The transmission of packets and their contents over the Internet from the source host to the destination host, providing addressing and transport communication services.

D. The internal operation of network interface hardware, which handles framing and media access control rather than end‑to‑end internetwork transport.
 
4. What do TCP/IP supervisory protocols govern?

A. The encryption and decryption of payloads for confidentiality, which is performed by security protocols and not by general supervisory control protocols.

B. Everything except the transmission of packets and their contents across the Internet: DNS, routing exchanges, control messages, and related management and error signaling.

C. The selection of data‑link paths within a single Ethernet segment, which is a switching function rather than interdomain control or management signaling.

D. The exclusive handling of DNS and router communication only, excluding error reporting or control, which understates supervisory protocol responsibilities.
 
5. Distinguish between Step 1 and Step 2 in the routing process.

A. Step 1 identifies a destination MAC address; Step 2 selects a VLAN tag, which are data‑link procedures unrelated to IP best‑match selection.

B. Step 1 forwards the packet immediately; Step 2 records the decision later, reversing the standard order of lookup then forwarding.

C. Step 2 configures network interfaces; Step 1 initializes routing protocols, which concerns management tasks not included in per‑packet routing.

D. Step 1 finds all matching rows for the destination; Step 2 selects the best‑match row using longest‑prefix criteria and possibly metrics.
 
6. If any row other than the default row matches an IPv4 address, why will the router never choose the default row?

A. The default is highest priority administratively yet still never selected, an inconsistency with routing behavior and control plane policies.

B. The default has a zero‑length match; any specific matching row has a longer prefix length and is therefore selected by longest‑match rules.

C. The default lacks the necessary next‑hop information, making it unusable, which contradicts the definition of a functional default route.

D. The default row always has the lowest metric value, guaranteeing it is skipped even if it were the only route covering the destination.
 
7. Given rows in Figure 8-11 match 128.171.17.13? Don’t forget the default row.

A. Rows 1, 7, 13, where both specific prefixes and the default route match, and the longest explicit prefix is chosen for actual forwarding.

B. Rows 4, 8, 12, suggesting arbitrary entries match without shared prefixes, which contradicts the structure described for the routing figure.

C. Rows 2, 5, 9, indicating unrelated routes that would not logically cover the specified destination address in a hierarchical table.

D. Rows 3, 6, 11, implying nonoverlapping networks somehow match the same destination, which is inconsistent with prefix‑based routing behavior.
 
8. Given rows 1, 7, 13 of Figure 8-11 match for a packet destined for 128.171.17.13. Which of these is the best-match row?

A. Row 13 is best because it is the default, ignoring that any specific match must take precedence over a zero‑length prefix.

B. Row 1 is best because it has the lowest metric overall, which cannot overrule a longer match under standard longest‑prefix selection.

C. Row 7 is best because it has the longest matching prefix length, /24, which outranks broader aggregates and the zero‑length default route.

D. Row 1 is best simply because it appears first in the table, disregarding the requirement to select by longest prefix length.
 
9. From Figure 8-11, which rows match 172.30.12.47?

A. Row 2, 5, and 9, which would imply unrelated networks redundantly cover the same internal address, contrary to typical summarization.

B. Row 10, 11, and 13, where two specific prefixes cover the destination alongside the default route, with the longest prefix preferred.

C. Row 1, 7, and 8, indicating mismatched external networks align with an internal destination, which conflicts with figure assumptions.

D. Row 4, 6, and 12, suggesting three unrelated entries simultaneously match, which is unlikely under organized hierarchical addressing.
 
10. Given row 10, 11, and 13 are a match for 172.30.12.47 in Figure 8-11, which of these is the best-match row?

A. Row 13 is chosen as the default regardless, contradicting the requirement to prefer any specific matching prefix over the default route.

B. There is a tie at /24 between 10 and 11; Row 11 has the lower metric, so it becomes the best‑match route for forwarding.

C. Row 13 is preferred due to a lower metric than specifics, which cannot override the longer prefix length of the matching routes.

D. Row 10 is selected simply because it appears first, which ignores standard rules requiring longest match and metric comparison.
 
11. Distinguish between Step 2 and Step 3 in routing.

A. Step 2 picks the best‑match row; Step 3 forwards the packet out the listed interface toward the specified next‑hop or directly attached destination.

B. Step 2 transmits frames onto the wire; Step 3 then decides the route, reversing the logical order of decision and forwarding.

C. Step 2 chooses the egress interface; Step 3 reconfigures routing protocols, which are management actions separate from per‑packet forwarding.

D. Step 3 discovers the destination MAC address; Step 2 chooses a VLAN, which are link‑layer tasks not defining IP forwarding steps.
 
12. What are router ports called?

A. Channels, a term used for multiplexed media streams rather than discrete IP forwarding endpoints on routing equipment.

B. Ports, the application transport identifiers, not the router’s physical or logical egress and ingress connection entities.

C. Gates, a colloquial term for security boundaries rather than the standardized name for router forwarding connection points.

D. Interfaces, the logical and physical attachment points used to send and receive packets across connected networks and next‑hop devices.
 
13. According to Figure 8-11, if the router selects Row 13 as the best-match row, what interface will the router send the packet out?

A. Interface 2, which would represent an alternative internal path and not the listed default next‑hop interface in the depicted routing table.

B. Interface 3, as indicated by the default route’s egress selection for unmatched destinations requiring forwarding toward the upstream next‑hop device.

C. Interface 4, which is not the figure’s outbound selection for the default route and would misdirect otherwise unmatched traffic.

D. Interface 1, which would contradict the figure’s specification for the default route’s designated outbound interface toward the upstream device.
 
14. According to Figure 8-11, if the router selects Row 13 as the best-match row, to what device will it send it to?

A. Router A, which is an internal neighbor not designated by the default route for unmatched destinations in the illustrated forwarding table.

B. Router C, which represents another internal peer and is not the default next‑hop device for otherwise unmatched destinations.

C. Router H, the upstream next‑hop designated by the default route, receiving traffic for destinations that lack more specific matching prefixes.

D. Router B, which handles a different set of internal prefixes and is not the configured next hop for the default route’s traffic.
 
15. Why is this router called the default router?

A. It has the highest priority in all routing tables, which overrides specific routes and contradicts longest‑prefix match behavior.

B. It always offers the fastest processing path, making it the preferred choice even when specific routes exist for the destination.

C. It is always the final router before the destination host, ensuring direct delivery without relying on any intermediate hops.

D. It is the router listed in the default row; packets with no specific matching route are forwarded to it as the upstream next hop.
 
16. If the router selects Row 2 as the best-match row for packet 172.30.33.6, what interface will the router send the packet out?

A. 3, which conflicts with the row’s egress designation and would not align with the forwarding information base entry.

B. 1, corresponding to the egress interface specified in Row 2, which directs the packet along the indicated path toward its destination.

C. 2, which would ignore the routing table entry’s configured interface and misdirect the packet away from the selected next‑hop path.

D. 4, which does not match Row 2’s interface selection and would be incorrect for the specified destination and next‑hop choice.
 
17. If the router selects Row 2 as the best-match row for packet 172.30.33.6, to what device will is send the packet?

A. Router C, which is another neighbor device and not the directly attached destination host indicated by the routing table entry.

B. Local means the destination host; the router is directly connected and therefore forwards the packet directly to that host on the local subnet.

C. Router B, which indicates an alternate upstream neighbor and not the direct delivery implied by the “Local” designation in the row.

D. Router A, which would be used only if the row specified a next hop rather than a directly connected local destination network.
 
18. According to the standard, what should a router do if it receives several packets going to the same destination IPv4 address?

A. Forward all packets to the default router immediately, bypassing lookup for efficiency and ignoring any available specific matching routes.

B. Drop all but one packet, assuming duplicates are unnecessary, which would discard valid traffic and violate standard forwarding behavior.

C. Only process the first packet and cache the outcome permanently, ignoring later changes that could invalidate the original decision.

D. Go through the entire three‑step lookup and forwarding process for each packet, independently determining matches and best routes before transmission.
 
19. How would decision caching speed the routing decision for packets after the first one?

A. It would increase the number of steps by adding a verification stage, which would slow forwarding rather than improving performance.

B. The router could reuse the earlier best‑match decision for subsequent packets to the same destination, avoiding repeated full lookups for each.

C. It would deliberately delay forwarding to batch decisions, which contradicts the goal of minimizing per‑packet processing overhead.

D. It would skip only Step 1 while still repeating Steps 2 and 3, yielding no practical benefit over performing the entire lookup sequence.
 
20. Why is decision caching dangerous?

A. If the route later becomes invalid, subsequent packets might be forwarded incorrectly, because the cached decision no longer reflects current topology.

B. It slows packet transmission by forcing every packet through a cache, which is inherently more expensive than performing lookups.

C. It increases overall network congestion by amplifying duplicate packets, independent of any changes in routing tables or next‑hop reachability.

D. It consumes excessive memory regardless of traffic, even when caches are small, making it inherently impractical on any routing platform.
 
21. An arriving packet has the destination IPv4 address 128.171.180.13. Row 86 has the destination value 128.171.160.0. The row’s mask is 255.255.224.0. Does this row match the destination IPv4 address?

A. Yes, because applying the 255.255.224.0 mask groups 128.171.160.0 through 128.171.191.255, which includes the destination 128.171.180.13 within that prefix.

B. Maybe, because the address falls into multiple disjoint ranges simultaneously, making it impossible to determine membership with the given mask.

C. No, because a /24 mask would be required to cover the destination, and 255.255.224.0 cannot aggregate addresses into such a narrow range.

D. Not enough information, because the next hop and metric are needed to decide if the destination numerically belongs inside the specified prefix.
 
22. What are interfaces?

A. Separate devices placed between networks to relay traffic, acting as standalone routers rather than connection points on an existing router chassis.

B. Ports on a router where network cables or links connect, providing attachment points and identifiers for sending and receiving frames and packets.

C. Menu screens that provide access to a router’s underlying programming interface, not the forwarding endpoints used for network transmission.

D. Communication protocols that define message formats and procedures, not the physical or logical ports through which a router forwards traffic.
 
23. How long is each part of an IPv4 address?

A. Each address part is always eight bytes long, producing a total length of sixty‑four bytes, which conflicts with the IPv4 thirty‑two‑bit standard.

B. The total address is 32 bits, while each dotted‑decimal part represents eight bits but may vary numerically from 0 to 255 based on value.

C. Each address part is sixteen bits long, creating sixty‑four total bits, which would correspond to IPv6 rather than IPv4 addressing practice.

D. Each address part is sixty‑four bits long, creating two hundred fifty‑six total bits, which does not represent any standardized Internet addressing scheme.
 
24. What is the total length of an IPv4 address?

A. 256 bits, which exceeds standardized addressing sizes and is not used for host addressing in either IPv4 or IPv6 protocol suites.

B. 128 bits, which is the length used by IPv6 addressing, not the length associated with IPv4 packet source and destination addresses.

C. 32 bits, represented as four octets in dotted‑decimal notation, providing source and destination addressing for routing across interconnected IP networks.

D. 64 bits, which would align with certain legacy architectures but not the standardized addressing length defined for IPv4 in modern internetworks.
 
25. In the IPv4 address, 10.11.13.13, what is the network part?

A. 10.11.0.0, which assumes a /16 mask without information, overlooking that classful assumptions are invalid in modern classless addressing.

B. We cannot say, because the network portion depends on the applied mask or prefix length, which is not provided with the bare dotted‑decimal address.

C. 10.11.13.0, which assumes a /24 mask without evidence, ignoring that the actual network boundary could fall at different bit positions.

D. 10.0.0.0, which assumes an old class A default, disregarding variable‑length subnet masks that determine the true network boundary.
 
26. If you see an IPv4 address, what do you know for certain?

A. That it belongs to the 10.x.x.x network space, which cannot be concluded from an arbitrary address without observing its specific numeric range.

B. That it is a private address, which is only true for reserved ranges like 10/8, 172.16/12, and 192.168/16, not for all IPv4 values.

C. That it is a Class A address, which relies on outdated classful rules and provides no certainty without considering modern classless prefix usage.

D. That the total length is 32 bits, because IPv4 addresses consist of four eight‑bit octets regardless of the specific numeric values shown.
 
27. Connecting different networks is the main job of what type of router?

A. Access points, which provide wireless connectivity to clients and do not perform interdomain routing between internal and external networks.

B. Border routers, which sit at the edge of an autonomous system and forward traffic between internal networks and external networks or upstream providers.

C. Distribution switches, which aggregate access switches within a campus and do not perform interdomain routing between different organizations.

D. Internal routers, which primarily forward traffic between subnets within the same organization and are not positioned at the external boundary.
 
28. What type of router connects different subnets?

A. Wireless controllers, which manage access points and client associations but are not responsible for routing across different IP subnets.

B. Load balancers, which distribute application sessions across servers and do not perform IP routing between separate internal subnets.

C. Border routers, which connect an organization to external networks, focusing on interdomain paths rather than internal subnet connectivity.

D. Internal routers, which forward packets between subnets inside an organization, enforcing routes and policies for internal segment‑to‑segment communication.
 
29. How many bits are there in an IPv4 mask?

A. 16 bits, which would be insufficient to define flexible subnet boundaries across the full IPv4 address space used in routing.

B. 8 bits, which is far too short for representing generic network masks and would not support modern subnetting requirements.

C. 24 bits, which would correspond to a specific prefix length but does not represent the general size of all valid IPv4 masks.

D. 32 bits, matching the length of the IPv4 address and indicating which bits identify the network versus the host portion of the address.
 
30. What do the 1s in an IPv4 NETWORK mask correspond to in IPv4 addresses?

A. The broadcast address exclusively, which is a special destination and not a direct mapping of the one bits used in the mask.

B. The subnet part only, ignoring that a network mask does not distinguish subnet structure unless explicitly defined by a subnet mask.

C. The network part, identifying the bits that remain constant for all hosts within the same routed network segment and prefix length.

D. The host part, which varies per device and is indicated by zeros in the mask, not the ones that define the network boundary.
 
31. What do the 1s in an IPv4 SUBNET mask correspond to in IPv4 addresses? Think carefully!

A. The host part, which is represented by zero bits in both network and subnet masks and varies among individual devices.

B. The subnet address value itself, which is a specific computed result, not the general meaning of one bits within the mask definition.

C. The network and subnet part, marking the prefix bits shared by all hosts in the subnet and distinguishing them from the host identifier bits.

D. The network part only, which omits the additional bits that further subdivide networks into subnets under variable‑length subnetting.
 
32. When a network mask is applied to any IPv4 address on the network, what is the result?

A. The bits of the host part isolated alone, which are derived by inverse masking but are not themselves the routed network identifier.

B. The bits of the subnet part only, excluding the main network portion, which does not represent the complete routed prefix used for forwarding.

C. The bits of the broadcast address, which are formed by setting host bits to one and are not obtained directly by masking an arbitrary address.

D. The network IP address found in route tables, produced by bitwise AND of the address and mask, identifying the routed network or subnet prefix.
 
33. A mask has eight 1s, followed by 0s. Express this mask in dotted decimal notation.

A. 128.0.0.0, representing a single leading one bit only, which does not correspond to an octet‑aligned eight‑bit network mask boundary.

B. 255.0.0.0, representing a /8 prefix with the first octet masked and the remaining three octets available for host or subnet bits.

C. 192.0.0.0, representing two leading one bits only, which corresponds to a /2 prefix rather than a full /8 octet boundary.

D. 240.0.0.0, representing four leading one bits only, which equals a /4 prefix and not an eight‑bit masked octet.
 
34. A mask has eight 1s, followed by 0s. Express this mask in prefix notation.

A. /8, indicating that the first eight bits are masked as network bits and the remaining twenty‑four bits are available for host or subnetting.

B. /128, indicating a one‑hundred‑twenty‑eight‑bit prefix length, which applies to IPv6 and not to thirty‑two‑bit IPv4 addressing.

C. /64, indicating a sixty‑four‑bit prefix length, which is a common IPv6 boundary and not valid for IPv4 addressing masks.

D. /32, indicating all bits masked, which represents a host route and not an eight‑bit network prefix across the first octet.
 
35. In prefix notation, a mask is /16. Express this mask in dotted decimal notation.

A. 255.0.0.0, which represents a /8 mask and would mask only the first octet, not the first two octets required for /16.

B. 255.255.0.0, which masks the first two octets and leaves the remaining two octets for host identifiers within the routed subnet.

C. 255.255.255.255, which represents a /32 host route and is not equivalent to a /16 network or subnet prefix length.

D. 255.255.255.0, which represents a /24 mask and would incorrectly mask three octets rather than two for this particular prefix.
 
36. Express the mask /18 in dotted decimal notation.

A. 255.0.0.0, which corresponds to a /8 prefix and masks only one octet, not the required eighteen bits for this mask.

B. 255.255.255.255, which is a /32 host mask and does not represent a routable network prefix of eighteen masked bits.

C. 255.255.255.0, which corresponds to a /24 prefix and masks three full octets, exceeding the specified eighteen bits for this case.

D. 255.255.192.0, which sets the first eighteen bits to one by masking two full octets and the upper two bits of the third octet.
 
37. Why are routing tables more complex than Ethernet switching tables?

A. Ethernet switches include specialized hardware that complicates lookups, whereas routers rely on software only, reducing complexity in finding next‑hop routes.

B. Ethernet addressing uses many more fields than IP, creating complexity in switches rather than routers, which actually simplifies IPv4 longest‑prefix matching.

C. In Ethernet there is one data‑link path per destination MAC, so one matching row; in mesh routing, multiple IP prefixes may match, requiring expensive best‑match selection.

D. Routing tables contain fewer entries than switching tables, reducing search complexity and making lookup times trivial compared with Ethernet forwarding.
 
38. In a routing table, what does a row represent?

A. A subnet mask entry alone without a destination, which cannot guide next‑hop decisions or interface selection during packet forwarding.

B. A destination MAC address learned by observation, which applies to switching tables and not to IP routing table entries.

C. A single specific IP address only, never a prefix, which would prevent aggregation and efficient forwarding decisions across multiple destinations.

D. A route for a range of IP addresses, defined by a destination prefix, mask length, next hop, outgoing interface, and metric attributes.
 
39. Do Ethernet switches have a row for each individual Ethernet address?

A. No, they store only network prefixes, aggregating many MAC addresses into a single route entry similar to IP longest‑prefix matching.

B. Yes, they learn and store entries mapping destination MAC addresses to switch ports, enabling unicast forwarding on a per‑address basis.

C. Only for managed switches, because MAC learning is a management feature rather than a fundamental function of Ethernet bridge operation.

D. It depends on the switch model, because unmanaged devices never learn MAC addresses and always flood unicast traffic to every connected port.
 
40. Do routers have a row for each individual IPv4 address?

A. Only for enterprise‑grade routers, which have sufficient memory to store every host route and do not require prefix aggregation for efficiency.

B. No, they store routes for prefixes that cover ranges of addresses, using longest‑prefix matching instead of per‑host entries for scalability.

C. Yes, they maintain separate entries for every host globally, ensuring exact matches and eliminating the need for aggregated prefixes.

D. It depends on the routing protocol, because some protocols only distribute host routes and cannot advertise network prefixes of varying lengths.
 
41. What is the advantage of routers in not having a row for each address?

A. Troubleshooting becomes automatic since fewer rows guarantee correctness, removing the requirement to validate prefixes, next hops, or route sources.

B. There are far fewer rows than hosts, enabling scalable forwarding by aggregating destinations into prefixes that reduce table size and lookup work.

C. The routing process becomes trivial because aggregation removes any need for metrics, best‑path selection, or longest‑prefix matching algorithms.

D. Routers can enumerate every host on the Internet, replacing aggregation with complete knowledge and eliminating the need for default routes.
 
42. Why is the last row called the default row?

A. If no other row matches, it is selected as the best‑match row by default, providing a fallback next hop for otherwise unmatched destinations.

B. It is dedicated to private networks only, preventing public Internet destinations from being forwarded via the router’s default gateway.

C. It is reserved strictly for administrative notes and never participates in forwarding decisions during the routing lookup process.

D. It contains the highest priority routes for specific prefixes, ensuring it is always chosen even when more specific routes are available.
 
43. Why must a router look at all rows in a routing table?

A. It prevents routing loops by scanning the full table, since loops are eliminated by exhaustive search rather than protocol‑level safeguards.

B. It needs to update the routing table during every lookup, so it traverses all rows to modify entries before forwarding each packet.

C. It ensures efficient delivery because shorter matches are always better, so examining every row guarantees a route with the smallest prefix length.

D. It cannot know how many matches exist until evaluation completes, because it must consider all candidate prefixes to select the longest matching route.
 
44. Which rows in Figure 8-11 match 172.30.17.6? Don’t forget the default row.

A. Only Row 13, the default row, matches, indicating no specific prefix covers the destination beyond the all‑else fallback route provided.

B. Rows 4 and 12 match equally, reflecting redundant host entries that duplicate coverage for the same address and contradict aggregation practices.

C. Rows 8 and 10 match together, providing overlapping host routes for the same destination, an unlikely configuration in standard route aggregation.

D. Rows 2 and 6 match simultaneously, demonstrating two equal‑length specific prefixes that override the default despite no evidence of such coverage.
 
45. Which rows in Figure 8-11 match 60.168.7.32?

A. Row 7 and 9, representing duplicate host routes that conflict with standard aggregation rules for summarized destination coverage.

B. Row 1 and 11, implying a backbone route and an internal subnet both exactly match, which is inconsistent with standard prefix organization.

C. Row 12 and 13, indicating one specific prefix and the default route both cover the destination, with the specific prefix preferred by longest match.

D. Row 3 and 5, showing two unrelated internal routes somehow cover an external network, contrary to expected boundaries in typical routing tables.
 
46. Which rows in Figure 8-11 match 128.171.17.13?

A. Row 1, 7, 13, where two specific prefixes and the default route match, with the longest matching prefix chosen for forwarding preference.

B. Row 3, 6, 11, indicating mismatched networks that do not summarize to the given destination and therefore would not register as matches.

C. Row 4, 8, 12, implying parallel paths from different domains all match equally, which is inconsistent with the described figure’s organization.

D. Row 2, 5, 9, representing unrelated prefixes that would not overlap to cover this destination address under typical hierarchical aggregation.
 
47. A router wishes to send an IP packet to a host on its subnet. It knows the host’s IP address. What else must it know?

A. It must know the router’s own MAC address, which it already has and which does not substitute for the destination’s address on the frame.

B. It must know the destination host’s subnet mask, which does not affect framing once the destination is already confirmed to be locally attached.

C. It must know the destination host’s data‑link (MAC) address, enabling encapsulation of the IP packet inside a frame deliverable on the local medium.

D. It must know the source host’s IP address, which is already inside the packet header and not required for local frame delivery.
 
48. A router wishes to send an IP packet to a host on its subnet. It knows the host’s IP address. Why must it know the data link layer address?

A. It identifies the packet source uniquely, which is already provided by the IP header and does not drive local layer‑two delivery.

B. It is needed to encrypt the packet payload, which is unrelated to addressing the frame for delivery on the shared local medium.

C. It must place the packet into a frame addressed with the destination’s MAC, ensuring the local network forwards the frame to the correct host.

D. It ensures the router chooses the right next‑hop, which is unnecessary because the host is directly attached and not reached through another router.
 
49. A router wishes to send an IP packet to a host on its subnet. It knows the host’s IP address. What message will it first broadcast?

A. It will broadcast an ICMP echo request, which tests reachability but does not return the MAC address needed for local delivery.

B. It will broadcast an ARP request, asking which device owns the specified IP address so it can learn the corresponding destination MAC address.

C. It will broadcast a DHCP request, which obtains addressing configuration and is unrelated to resolving neighbor MAC addresses.

D. It will broadcast a DNS query, which resolves hostnames to IP addresses rather than discovering local MAC addresses for frame delivery.
 
50. A router wishes to send an IP packet to a host on its subnet. It knows the host’s IP address. What device will respond to the ARP message?

A. The DNS server will respond with a MAC address record, which DNS does not provide because it resolves names to IP addresses only.

B. The destination host will respond with its MAC address, allowing the router to encapsulate the packet into a frame for local transmission.

C. The DHCP server will respond with lease information, which does not answer ARP requests or provide the destination’s layer‑two address.

D. The default gateway will respond on behalf of the host, even when the destination is local, which is not standard ARP behavior.
 
51. Does a router have to go through the ARP process each time it needs to send a packet to a destination host or to a next-hop router?

A. Caches are never used in networking, so address resolution repeats constantly, contradicting the standard neighbor discovery process.

B. ARP is performed only at startup, after which mappings never change, which ignores aging and updates required for accurate delivery.

C. No, it stores IP‑to‑MAC mappings in an ARP cache and reuses them until they age out, avoiding repeated broadcasts for each packet.

D. Yes, it must perform ARP for every frame transmitted, which would flood the network and ignore caching mechanisms designed for efficiency.
 
52. Is ARP used to find the destination data link layer destination addresses of destination hosts, routers, or both?

A. Only hosts, since routers never participate in neighbor discovery and cannot act as ARP targets on shared or switched local segments.

B. Both, because ARP resolves MAC addresses for local hosts and for directly connected next‑hop routers when forwarding to external networks.

C. Only routers, because hosts do not advertise their MAC addresses and cannot respond to local address resolution requests on a subnet.

D. Neither, because ARP only configures IP addresses and never resolves layer‑two addresses for any device on the local network.
 
53. At what layer does the ARP protocol operate?

A. The application layer (Layer 5), which concerns user services and does not manage address resolution on local Ethernet networks.

B. The data link layer (Layer 2), where devices resolve IP addresses to MAC addresses for local delivery on shared or switched media.

C. The internet layer (Layer 3), which handles logical addressing and routing rather than performing MAC resolution on local segments.

D. The transport layer (Layer 4), which provides end‑to‑end reliability and multiplexing rather than neighbor discovery at layer two.
 
54. Why must client PCs use ARP to transmit packets?

A. They use ARP to reduce latency by bypassing routing, which misrepresents ARP’s role as a neighbor discovery protocol only.

B. They require ARP to encrypt packets before sending, which is unrelated to address resolution and link‑layer frame construction.

C. They need ARP to enable payload compression, which is not a function of address resolution or Ethernet frame preparation.

D. They must learn the MAC address of the default router or local destination, enabling correct framing for delivery on the local network.
 
55. What is the purpose of dynamic routing protocols?

A. They facilitate payload encryption end‑to‑end, which is handled by security protocols rather than by dynamic routing exchanges.

B. They allow routers to exchange routing information, building and updating routing tables automatically as topology and link states change.

C. They minimize latency by shaping traffic at the application layer, unrelated to control‑plane route calculation and distribution.

D. They ensure that packet payloads remain confidential, providing encryption and decryption services as part of the routing process.
 
56. For its own network, can an organization choose its interior dynamic routing protocol?

A. Only if permitted by the ISP, which controls internal routing policy within the customer’s autonomous system and endpoints.

B. Only with government approval, as interior routing choices are formally regulated and standardized for every enterprise deployment.

C. Yes, organizations select an interior gateway protocol appropriate for their environment, such as OSPF, IS‑IS, or vendor‑specific alternatives.

D. No, interior protocols are assigned exclusively by upstream providers, leaving enterprises unable to choose routing behavior inside their networks.
 
57. What is the IETF interior dynamic routing protocol?

A. BGP, an exterior gateway protocol used between autonomous systems rather than for interior routing within a single organization.

B. OSPF, an open standard link‑state interior gateway protocol widely implemented for dynamic routing within a single autonomous system.

C. RIP, a simple distance‑vector protocol from early networks, which is not the primary IETF standard for modern large‑scale interiors.

D. EIGRP, a proprietary protocol historically associated with one vendor and not standardized by the IETF as the primary interior protocol.
 
58. When might you use EIGRP as your interior dynamic routing protocol?

A. When you need to support multiprotocol routing beyond pure TCP/IP, leveraging features historically available in certain proprietary environments.

B. When you must prioritize voice traffic end‑to‑end, which is primarily addressed by QoS policies rather than the choice of routing protocol.

C. When you need to establish encrypted VPN tunnels, which is handled by security protocols rather than interior gateway routing mechanisms.

D. When you require application‑layer load balancing, which is outside the scope of routing protocols and belongs to traffic management devices.
 
59. May a company select the routing protocol its border router uses to communicate with the outside world?

A. No, exterior protocol choice is effectively constrained to the common interdomain standard used by providers and peers on the public Internet.

B. Yes, organizations independently choose any interior or exterior protocol, regardless of compatibility with peers in interdomain exchanges.

C. Only if it is a multinational corporation, because smaller organizations must adopt whatever protocols are mandated by regional authorities.

D. Only if it has a large network engineering team, since exterior protocol selection depends on staffing rather than interoperability requirements.
 
60. What is the almost-universal exterior dynamic routing protocol?

A. OSPF, a link‑state protocol designed for interior routing within a single autonomous system, not for interdomain path selection.

B. EIGRP, a proprietary protocol primarily intended for interior routing and not standard for exchanges between separate autonomous systems.

C. RIP, an early distance‑vector protocol unsuitable for large‑scale interdomain routing due to slow convergence and limited metric sophistication.

D. Border Gateway Protocol (BGP), the widely deployed interdomain routing protocol used between autonomous systems across the public Internet.
 
61. What is a gateway?

A. An older term for a router still present in many standards and products, referring to a device that forwards packets between networks.

B. A type of cable used to connect two devices directly, not a system that makes forwarding decisions based on network‑layer addressing.

C. A network switch that operates at layer two exclusively, not a device responsible for routing packets between separate IP subnets.

D. A specialized firewall that filters traffic only at the application layer, unrelated to the general function of forwarding between networks.

## Answer Key

1. B
2. B
3. C
4. B
5. D
6. B
7. A
8. C
9. B
10. B
11. A
12. D
13. B
14. C
15. D
16. B
17. B
18. D
19. B
20. A
21. A
22. B
23. B
24. C
25. B
26. D
27. B
28. D
29. D
30. C
31. C
32. D
33. B
34. A
35. B
36. D
37. C
38. D
39. B
40. B
41. B
42. A
43. D
44. A
45. C
46. A
47. C
48. C
49. B
50. B
51. C
52. B
53. B
54. D
55. B
56. C
57. B
58. A
59. A
60. D
61. A
