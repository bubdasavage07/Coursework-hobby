1. What information do the two tag fields give?

A. The Tag Protocol Identifier holds checksum values, and the Tag Control Information stores payload size values and end‑to‑end error‑detection parameters for reliability.

B. The Tag Protocol Identifier records routing hop counts, and the Tag Control Information contains IP addressing details and next‑hop gateway forwarding instructions.

C. The Tag Protocol Identifier indicates the frame is VLAN‑tagged, and the Tag Control Information encodes priority bits and the specific VLAN membership information.

D. The Tag Protocol Identifier specifies the physical cable type, and the Tag Control Information lists the destination switch port and the connected patch‑panel position.

2. What is POE Plus? Do not just spell out the abbreviation.

A. Power over Ethernet Plus is a routing protocol that dynamically selects high‑priority paths for voice traffic across enterprise backbone networks using QoS queues.

B. Power over Ethernet Plus is a standard allowing a switch to deliver roughly twenty‑five watts of DC power over twisted‑pair cabling to attached devices.

C. Power over Ethernet Plus is a cabling category rating that specifies improved shielding and reduced crosstalk for ten‑gigabit links in noisy industrial environments.

D. Power over Ethernet Plus is a faster Ethernet signaling method that increases link speed without changing connectors, frames, or existing Layer 2 switching functions.

3. Why is POE Plus attractive to corporations?

A. It eliminates many separate electrical runs by powering suitable endpoints over Ethernet, reducing installation cost, complexity, and coordination with building electricians.

B. It prevents congestion on access switches by limiting broadcast frames and automatically converting hubs into managed switches with per‑port isolation policies.

C. It hardens network security by encrypting frames at Layer 2, eliminating the need for higher‑layer protections such as TLS, IPsec, or application authentication.

D. It significantly increases TCP throughput by prioritizing traffic, thereby reducing queueing delay and packet loss across congested aggregation and core links.

4. What maximum standard power does the POE Plus standard specify?

A. The standard specifies a maximum delivered power of about twenty‑five watts at the powered device, subject to cable length, loss, and compliance conditions.

B. The standard specifies a maximum delivered power of about thirty watts, guaranteeing identical power at the injector and at the powered device with no loss.

C. The standard specifies a maximum delivered power of about fifteen watts, which is sufficient for desktop computers, monitors, and multi‑radio access points.

D. The standard specifies a maximum delivered power of fifty watts, enabling direct operation of laser printers, small servers, and multi‑disk storage arrays.

5. For what types of devices is POE Plus sufficient?

A. It is optimized for core switches and large routers, providing the substantial power required by backplanes, modular line cards, and high‑capacity fabric interconnects.

B. It is primarily intended for desktop computers and most laptops, which require only minimal power for displays, processors, memory, and integrated storage devices.

C. It is designed for enterprise servers and high‑performance workstations that demand continuous multi‑hundred‑watt power for CPUs, GPUs, and redundant power supplies.

D. It typically powers VoIP phones, many surveillance cameras, and numerous Wi‑Fi access points that fall within the approximately twenty‑five‑watt power budget.

6. Is POE Plus sufficient for desktop computers and most notebook computers?

A. No, POE Plus generally cannot power desktops or most notebooks because their typical power requirements far exceed the approximately twenty‑five‑watt delivery limit.

B. Yes, POE Plus intentionally exceeds conventional AC power, allowing pass‑through charging of peripherals, external monitors, and multi‑disk external storage arrays.

C. Yes, POE Plus reliably powers all computing devices, including gaming desktops and mobile workstations, without supplemental adapters, batteries, or external supplies.

D. It depends entirely on screen size and color depth, as graphics settings rather than CPUs or storage determine whether POE Plus can provide adequate power.

7. What is a VLAN?

A. A VLAN is a virtual router instance that forwards IP packets between subnets, replacing traditional default gateways for all devices within a broadcast domain.

B. A VLAN is a wireless access technology that assigns radios to channels, enabling roaming users to maintain sessions without changing their physical connections.

C. A VLAN is a logical Layer 2 grouping that permits selected hosts to communicate as if on one switch, independent of their physical switch locations.

D. A VLAN is a physical segmentation method that requires dedicated cabling and separate switches to isolate traffic across different wiring closets and floors.

8. What two benefits do VLANs bring?

A. VLANs improve routing efficiency by collapsing core layers, eliminating the need for default gateways and allowing switches to route frames across subnets directly.

B. VLANs mainly enhance scalability by adding IP addresses automatically, preventing subnet exhaustion while preserving identical collision domains across legacy hubs.

C. VLANs primarily increase raw link speed and eliminate latency by converting copper runs to fiber, thereby raising throughput regardless of application requirements.

D. VLANs reduce broadcast congestion and strengthen security by limiting which hosts share a broadcast domain and by isolating sensitive groups from general users.

9. How do VLANs bring security?

A. They encrypt every Ethernet frame on access links, replacing the need for IPsec, TLS, or application authentication in standard enterprise deployments.

B. They block all broadcast, multicast, and unicast traffic, allowing only management frames, which guarantees isolation but disables normal business communications.

C. They randomize MAC addresses for each transmission, making traffic analysis impossible and rendering traditional intrusion detection sensors ineffective by design.

D. They enforce traffic separation at Layer 2, preventing unauthorized hosts in other VLANs from receiving frames unless permitted through routing and access controls.

10. When VLANs or priority is uses, what two fields does the 802.1Q standard add to Ethernet frames?

A. It appends IP addresses and subnet masks, allowing switches to route packets between subnets without involving routers or Layer 3 gateway configurations.

B. It adds source and destination MAC addresses, enabling switches to learn locations and forward frames across the network based on physical device addresses.

C. It provides transport control and error detection fields, replacing TCP checksums and Ethernet CRCs to ensure reliable delivery across lossy wired links.

D. It inserts a Tag Protocol Identifier and a Tag Control Information field that together mark the frame and encode priority and VLAN identification.

11. When VLANs are used, what does the Tag Protocol ID field tell a receiving switch or NIC?

A. It provides the source MAC address of the sending host, enabling the switch to populate its forwarding table without inspecting the Ethernet header.

B. It sets the priority level for the frame, determining strict priority queue selection and discarding thresholds for congestion management on every port.

C. It signals that the frame carries an IEEE 802.1Q tag, instructing the receiver to parse additional tag information before processing the payload.

D. It identifies the exact VLAN number that should be applied to the frame, replacing the Tag Control Information and eliminating the need for separate parsing.

12. What information does the tag control information field tell the switch or receiver?

A. It encodes the twelve‑bit VLAN ID and priority bits; a VLAN ID of zero indicates priority tagging without membership in a specific VLAN.

B. It provides authentication tokens for port security, granting access without 802.1X by validating pre‑shared keys within the tag on each frame.

C. It contains the IP time‑to‑live and header length fields, allowing the switch to decrement hops and detect fragmentation needs before forwarding.

D. It carries the destination MAC address and EtherType fields, enabling the receiver to perform hardware offload for checksum and segmentation operations.

13. In Figure 5‑27, what server or servers can Host A communicate with?

A. Host A can communicate with Host B and Host E because those systems share Host A’s VLAN membership within the depicted switched topology.

B. Host A can communicate with Host C and Host F because those destinations share the same IP subnet even if their VLAN assignments are different.

C. Host A can communicate with Host D and Host E because all hosts attached to a switch can exchange frames regardless of their VLAN configuration.

D. Host A can communicate with Host B and Host D because switch ports dynamically bridge every VLAN using automatic spanning tree tunneling between trunks.

14. In Figure 5‑27, what server or servers can Host C communicate with?

A. Host C can communicate with Host D and Host F because those systems reside in Host C’s VLAN, permitting switched forwarding without inter‑VLAN routing.

B. Host C can communicate with Host A and Host B because VLAN tags are ignored by access ports, allowing unrestricted communication across all hosts.

C. Host C can communicate with Host B and Host F because trunk links automatically merge VLANs, removing the need for routing or access control lists.

D. Host C can communicate with Host A and Host E because devices in different VLANs always share broadcast domains and exchange frames transparently.

15. At what layers do wireless LANs operate?

A. They primarily operate at the data‑link and network layers, corresponding to OSI Layers 2 and 3 for routing, addressing, segmentation, and congestion management.

B. They primarily operate at the physical and data‑link layers, corresponding to OSI Layers 1 and 2 for signaling, framing, media access, and error handling.

C. They primarily operate at the transport and session layers, corresponding to OSI Layers 4 and 5 for dialog management, encryption, and application stream multiplexing.

D. They primarily operate at the network and transport layers, corresponding to OSI Layers 3 and 4 for connection management, reliability, and flow‑control services.

16. Do wireless LAN standards governed by OSI or TCP/IP standards? Justify your answer.

A. They are governed by TCP/IP because Wi‑Fi radios implement IP addressing directly, eliminating the need for separate data‑link and physical specifications.

B. They are unrelated to either model, because Wi‑Fi simply forwards application payloads and relies exclusively on middleware brokers to coordinate sessions.

C. They align with OSI at Layers 1 and 2; IEEE 802 specifications define Wi‑Fi signaling and framing, not TCP/IP protocols, so they are OSI‑layer standards.

D. They only apply to wired environments, since wireless networks use proprietary vendor methods rather than standardized OSI or TCP/IP layering principles.

17. Does a signal travel at a single frequency, or does it spread over a range of frequencies?

A. Practical signals always use a single frequency, because any spread would violate conservation laws and be rejected by radio receivers.

B. Practical signals alternate rapidly among many unrelated frequencies, preventing receivers from synchronizing to carriers or decoding any information.

C. Practical signals spread only across time, not frequency, since the spectrum remains fixed while frames lengthen to carry larger payloads.

D. Practical signals occupy a range of frequencies, defined by channel bandwidth and modulation, rather than an idealized single‑frequency tone.

18. If the lowest frequency in a channel is 1.22 MHz and the highest frequency is 1.25 MHz, what is the channel bandwidth? Give your answer in kHz.

A. The bandwidth is 0.3 megahertz, which equals three hundred kilohertz, a value inconsistent with the stated lower and upper channel edge frequencies.

B. The bandwidth is 0.03 gigahertz, which equals thirty megahertz, indicating extremely wide channels reserved for deep‑space signal telemetry links.

C. The bandwidth is 0.03 megahertz, which equals thirty kilohertz, computed as 1.25 minus 1.22 megahertz and converted to kilohertz.

D. The bandwidth is 0.03 kilohertz, which equals thirty hertz, reflecting the smallest possible spacing used in narrowband laboratory test signals.

19. If you want to transmit seven times as fast, how much wider must the channel be?

A. The channel must be about seven times wider, since achievable data rate generally scales proportionally with available channel bandwidth under similar conditions.

B. The channel must be about seven times narrower, because decreasing bandwidth increases spectral efficiency and therefore multiplies the supported data rate.

C. The channel must be about four times narrower, since reducing occupied spectrum concentrates power and consequently multiplies throughput across users.

D. The channel must be about four times wider, as data rate grows with the square root of bandwidth for all digital modulation schemes in practice.

20. Why is large channel bandwidth desirable?

A. Larger bandwidth increases signal strength automatically, providing greater range without requiring any additional transmit power or improved receiver sensitivity.

B. Larger bandwidth reduces interference by eliminating adjacent channels, ensuring no external devices can occupy nearby frequencies within the same band.

C. Larger bandwidth decreases propagation delay, shortening physical distances so signals arrive sooner at receivers located throughout a large building.

D. Larger bandwidth enables higher peak and sustained data rates, allowing faster transfers and better support for modern applications that consume substantial throughput.

21. What do we call a system whose channels are wide?

A. We call it narrowband, referring to systems that purposely restrict channels to extremely small widths to achieve maximum possible throughput.

B. We call it broadband, referring to systems that employ wide channels and therefore can support higher data rates than narrowband systems.

C. We call it high‑bandwidth, referring to systems that ignore channelization and transmit across the entire spectrum without any frequency planning.

D. We call it baseband, referring to systems that use optical carriers and frequency hopping to provide multi‑gigabit speeds across satellite links.

22. What other types of system do we call broadband?

A. The term applies solely to satellite downlinks, which always use spread‑spectrum modulation and therefore qualify as broadband in every jurisdiction.

B. The term is reserved for multi‑band transceivers only, preventing its use for wired access technologies regardless of their data rates or capacities.

C. The term describes only analog television, whose channels are narrow yet considered broadband because they include color and audio subcarriers.

D. The term is also applied to high‑speed access like cable or fiber Internet, which are labeled “broadband” even though they are not radio systems.

23. Do WLANs today use licensed or unlicensed service bands?

A. They generally operate in hybrid bands that switch between licensed and unlicensed status depending on daily traffic patterns and weather conditions.

B. They generally operate in unlicensed service bands, which are open for compliant devices without individual licenses under specified technical constraints.

C. They generally operate in both licensed and unlicensed bands simultaneously, using automatic spectrum leases negotiated directly by client devices.

D. They generally operate in licensed service bands, requiring every access point and client to obtain separate frequency assignments before association.

24. What is the advantage of using unlicensed service bands?

A. No individual device licensing is required, and moving or adding Wi‑Fi equipment does not trigger license modifications, simplifying deployments significantly.

B. Transmission speed is inherently increased, because unlicensed radios ignore channelization rules and may occupy the entire band at once.

C. Signal quality is automatically improved, since unlicensed bands permit higher transmit power and guarantee exclusive use within each building.

D. Interference is reduced to zero, as regulations ensure no neighboring devices can share frequencies within the same geographic area.

25. What is the downside of using unlicensed service bands?

A. You cannot prevent other organizations or homes from using the same channels, so interference risk remains and must be managed operationally.

B. Coverage area is severely limited by law to a single room, preventing access points from serving clients in adjacent spaces or hallways.

C. Equipment costs are significantly higher because unlicensed radios require expensive frequency leases and ongoing payments to spectrum owners.

D. Regulatory compliance becomes extremely complex, involving individualized permits for every move, add, or change to any wireless endpoint.

26. In what two unlicensed service bands does 802.11 usually operate?

A. It commonly operates in the 1‑gigahertz and 3‑gigahertz bands, which are international maritime ranges reserved for long‑distance ship communications.

B. It commonly operates in the 2.4‑gigahertz and 5‑gigahertz unlicensed service bands defined for general‑purpose local wireless networking.

C. It commonly operates in the 4‑gigahertz and 6‑gigahertz bands, which are exclusive satellite control ranges unavailable for enterprise networks.

D. It commonly operates in the 5‑gigahertz and 7‑gigahertz bands, which are specialized radar ranges designated for aviation and weather services only.

27. How many 20 MHz nonoverlapping channels does the 2.4 GHz band support?

A. It supports three nonoverlapping twenty‑megahertz channels, which limits dense deployments and increases the likelihood of co‑channel interference.

B. It supports twelve nonoverlapping twenty‑megahertz channels, making channel planning unnecessary in typical enterprise wireless designs.

C. It supports six nonoverlapping twenty‑megahertz channels, allowing full reuse on every floor without any interference across buildings.

D. It supports nine nonoverlapping twenty‑megahertz channels, enabling complete separation of guest, voice, and data networks in small venues.

28. Why is the limited non‑overlapping channels in the 2.4 GHz a problem?

A. The limited channels require static IP addresses for clients, complicating network management and preventing DHCP from operating across subnets.

B. The limited channels restrict the number of MAC addresses allowed on the network, preventing most laptops and phones from associating simultaneously.

C. With only three clear channels, nearby access points often reuse frequencies, making it hard to avoid co‑channel interference and performance degradation.

D. The limited channels reduce maximum transmit power per device, forcing controllers to throttle radios below regulatory limits at all times.

29. Why are companies moving rapidly into the 5 GHz band?

A. The 5‑gigahertz band is almost unused, guaranteeing exclusive spectrum for each organization without any need for coordination or planning.

B. The 5‑gigahertz band offers many more channels, reducing harmful co‑channel interference and enabling better performance in dense enterprise environments.

C. The 5‑gigahertz band delivers slower data rates, which conserves battery life and therefore is preferred over faster but less efficient 2.4‑gigahertz radios.

D. The 5‑gigahertz band provides dramatically longer propagation distances, allowing single access points to cover entire multi‑building campuses reliably.

30. If you triple channel bandwidth, what happens to the number of channels in a service band? The answer is not directly in the text.

A. The number of channels remains unchanged, because bandwidth affects data rate only and does not influence how many channels can exist.

B. The number of channels is halved, because allocating any wider channel always removes exactly one adjacent channel regardless of the original count.

C. The number of channels triples, because wider channels pack more efficiently and therefore allow additional center frequencies to be inserted.

D. The number of channels drops to roughly one‑third, because each channel occupies three times more spectrum within the same fixed service band.

31. In the 2.4 GHz and 5 GHz service bands, what type of transmission method is required by regulators?

A. Regulators require frequency‑division multiplexing alone, eliminating any need for coding, guard intervals, or power limits across channels.

B. Regulators require spread‑spectrum methods, which distribute energy to reduce interference potential and improve coexistence among many unlicensed devices.

C. Regulators require narrowband methods, which concentrate energy to ensure single users fully occupy each band without sharing with nearby systems.

D. Regulators require time‑division multiplexing only, mandating that devices take strict turns rather than dividing the spectrum by frequency.

32. What is the benefit of spread spectrum transmission for business communication?

A. It primarily extends geographic range by amplifying output power beyond regulatory limits while keeping average channel utilization constant.

B. It primarily increases raw throughput by compressing frames, which multiplies spectral efficiency independent of modulation and coding schemes used.

C. It primarily enhances secrecy by encrypting signals at the physical layer, removing the need for any higher‑layer cryptographic protections.

D. It improves reliability by reducing susceptibility to narrowband interference and allows multiple systems to coexist more gracefully in shared bands.

33. Is spread spectrum transmission done for security reasons in commercial WLANs?

A. It depends on network configuration; when DHCP is enabled, spreading guarantees confidentiality by randomizing channel center frequencies.

B. Sometimes; security depends solely on SSID names, which determine whether spreading hides frames from unauthorized scanners in the vicinity.

C. No; commercial WLANs use spread‑spectrum mainly for interference mitigation and coexistence, not as a replacement for security mechanisms like WPA2 or WPA3.

D. Yes; because a Wi‑Fi device is on the Internet, spread‑spectrum encryption automatically protects traffic without any additional configuration.

34. Does spread spectrum transmission increase transmission speed thanks to its wider channels?

A. Yes; because spread‑spectrum always multiplies throughput, it replaces the need for wider channels or advanced modulation to achieve higher speeds.

B. It may increase or decrease speed randomly, since spreading forces radios to change frequencies even when no interference is present nearby.

C. It depends on configuration; enabling any passphrase causes spread‑spectrum to compress frames and therefore increase throughput in busy offices.

D. No; spread‑spectrum primarily aids robustness and coexistence, while higher data rates depend on modulation, coding, and actual channel bandwidth choices.

35. What spread spectrum transmission method dominates today?

A. Direct‑Sequence Spread Spectrum dominates, multiplying bit streams with long chipping codes to achieve the highest data rates available today.

B. Orthogonal Frequency‑Division Multiplexing (OFDM) dominates, using many orthogonal subcarriers to deliver reliable, high‑throughput links in typical WLAN deployments.

C. Frequency‑Hopping Spread Spectrum dominates, rapidly changing frequencies to maximize secrecy and eliminate the need for modern channel coding.

D. Chirp Spread Spectrum dominates, using wideband chirps to provide cellular handoff and mobility management in metropolitan macro‑cell networks.

36. Why does it divide the channel into subcarriers?

A. Dividing channels into subcarriers increases latency intentionally, adding interleaver delay to slow acknowledgments and reduce access‑point processing load.

B. Subcarriers are required to encrypt frames at Layer 2, replacing Wi‑Fi security suites and preventing the need for authentication exchanges.

C. Splitting channels into subcarriers ensures only one device can transmit, disabling multiuser access and eliminating contention from client stations.

D. Narrow subcarriers suffer less frequency‑selective fading and are easier to equalize, improving control of transmission quality and overall robustness.

37. Distinguish between 802.3 standards and 802.11 standards.

A. IEEE 802.3 defines Wi‑Fi authentication, whereas IEEE 802.11 defines Ethernet switching, including VLAN tagging and Spanning Tree Protocol operations.

B. IEEE 802.3 defines Ethernet for wired LANs, whereas IEEE 802.11 defines Wi‑Fi for wireless LANs using radio channels and media‑access mechanisms.

C. IEEE 802.3 defines only wireless LANs, whereas IEEE 802.11 defines only wired LANs that operate exclusively over fiber in enterprise backbones.

D. IEEE 802.3 covers cellular radio networks, whereas IEEE 802.11 covers Wi‑Fi networks that require SIM authentication and base‑station handoff protocols.

38. What is the actual difference between 802.11 and Wi‑Fi?

A. 802.11 defines VPN tunneling standards, while Wi‑Fi defines firewall policies and intrusion prevention signatures for enterprise perimeter security deployments.

B. 802.11 and Wi‑Fi are identical to Ethernet, both specifying wired frame formats and copper cabling categories for structured office and campus installations.

C. 802.11 governs cellular voice calls, while Wi‑Fi focuses on wired Ethernet backbones that aggregate campus access switches into core routers.

D. 802.11 is the IEEE standards family; Wi‑Fi is a certification program defining interoperable profiles, allowing compliant products to display the Wi‑Fi certification mark.

39. Do we use the two terms 802.11 and Wi‑Fi interchangeably?

A. Only in narrow radio‑astronomy contexts, where Wi‑Fi devices use Ethernet cabling and therefore fall outside traditional IEEE 802 standardization processes.

B. In this course, we will treat the terms interchangeably for simplicity, even though formally one is a standard and the other is a certification program.

C. No, they are never used interchangeably, because both terms strictly require numerical channel identifiers and cannot reference product interoperability at all.

D. It depends entirely on the manufacturer, since each vendor redefines the standard and certification independently for branding within marketing literature.

40. In a Wi‑Fi LAN, do two wireless hosts usually send frames directly to one another? Explain.

A. No; wireless clients communicate through ad hoc mesh routing only, because access points forward management frames and never carry normal data traffic.

B. No; a sending host transmits to the access point, which relays the frame to the receiving host, providing association control and centralized media coordination.

C. Yes; associated wireless clients always establish direct links, bypassing the access point, which is reserved solely for guest authentication and DHCP services.

D. Yes; clients automatically form peer‑to‑peer tunnels that remain active during roaming, eliminating the need for infrastructure access points entirely.

41. Why does the access point connect to the corporate Ethernet LAN?

A. It encrypts every wireless frame by default, removing the need for WPA2 or WPA3 and allowing open authentication for faster association times.

B. It supplies DC power to battery‑backed laptops, allowing continuous operation without chargers and reducing electrical circuit load in crowded office spaces.

C. It bridges wireless clients onto the enterprise LAN and uplinks to the Internet, enabling access to internal servers, services, and external resources.

D. It adjusts transmit power for nearby devices, ensuring uniform signal strength across floors without requiring clients to manage their own radio settings.

42. In 802.3 Ethernet networks, can simple installation rules usually reduce propagation effects to nonissues?

A. No; wired links inherently suffer uncontrollable multipath fading, requiring directional antennas and advanced spread‑spectrum techniques to achieve stability.

B. Maybe; it depends primarily on SSID selection and beacon intervals, which determine whether copper pairs can sustain long‑distance signal coherence.

C. It depends; only jumbo frames and flow control can mitigate reflection and scattering, while cable quality and layout have no measurable effect.

D. Yes; adhering to cabling limits, connector quality, and grounding practices generally keeps propagation effects negligible in typical structured wired Ethernet deployments.

43. In 802.11 Wi‑Fi networks, can simple installation rules usually reduce propagation effects to nonissues?

A. Yes; because Wi‑Fi is a device connected to the Internet, propagation effects vanish automatically once the SSID and passphrase are configured correctly.

B. No; variable obstacles, reflections, and interference mean propagation issues persist despite careful placement, requiring channel planning and radio design features.

C. Maybe; propagation depends solely on DHCP lease duration, which controls renewal timing and consequently the probability of collisions on the wireless medium.

D. It depends; only Ethernet autonegotiation settings determine wireless coverage, so adjusting duplex modes typically eliminates attenuation and dead zones.

44. What is a transceiver?

A. It is a processor that inspects packets, applying firewall rules and intrusion signatures without any capability to generate or detect radio signals.

B. It is a device that only transmits data, converting digital bits into light pulses for fiber runs where receivers are unnecessary at the far end.

C. It is a component that only receives data, demodulating signals while relying on separate infrastructure to transmit acknowledgments and control frames.

D. It is a component that both transmits and receives signals; in 802.11 radios, the same device handles sending and detecting modulated RF energy.

45. Is wireless radio transmission usually described in terms of wavelength or frequency?

A. It is rarely described with either quantity, because engineers rely on color labels and arbitrary channel names rather than measurable physical characteristics.

B. It is primarily described using wavelength, because equipment is tuned by measuring physical antenna length rather than counting oscillations per second.

C. It is always described using both measures simultaneously, since regulatory filings and device manuals must quote identical values for frequency and wavelength.

D. It is typically described in terms of frequency, which directly characterizes channel allocation, bandwidth, regulatory limits, and device radio tuning parameters.

46. What is a hertz?

A. A hertz represents one bit per second, the common unit used to express throughput on Ethernet links and wide‑area network circuits.

B. A hertz represents one cycle per second, the standard unit for measuring signal frequency and oscillation rates in electrical and radio systems.

C. A hertz represents one volt per meter, the regulatory unit used to certify electromagnetic emissions and shielding effectiveness for network equipment.

D. A hertz represents one watt per second, the accepted measure for energy used by powered devices and delivered through Power over Ethernet cabling.

47. At what range of frequencies do most wireless systems operate?

A. Most wireless systems operate strictly between 1 and 10 gigahertz, excluding lower and higher frequencies due to universal global regulatory prohibitions.

B. Most wireless systems operate only from 500 megahertz to 1 gigahertz, because antennas outside this region cannot efficiently radiate or receive electromagnetic energy.

C. Most wireless systems operate primarily from 10 to 20 gigahertz, as lower frequencies lack sufficient bandwidth for any practical digital modulation techniques.

D. Many Wi‑Fi systems commonly operate around the 2.4‑gigahertz and 5‑gigahertz bands, which are widely available for unlicensed local wireless communications.

48. Distinguish between omnidirectional and dish antennas in terms of operation.

A. An omnidirectional antenna requires coax splitters for alignment, while a dish antenna requires VLAN tags for steering, enabling precise Layer 2 beamforming.

B. An omnidirectional antenna radiates and receives broadly in all horizontal directions, while a dish antenna concentrates and gathers energy in a narrow, targeted beam.

C. An omnidirectional antenna supports only receiving functions, while a dish antenna supports only transmitting functions, preventing any bidirectional communication paths.

D. An omnidirectional antenna concentrates power into a tight beam, while a dish antenna distributes energy evenly in every direction across the coverage area.

49. Under what circumstances would you use an omnidirectional antenna?

A. You use it when you need to receive from many faraway towers simultaneously, requiring extremely narrow lobes that reject nearby reflections completely.

B. You use it when you must transmit only management frames, ensuring control traffic is strong while data frames are confined to a focused narrow beam.

C. You use it when the other device is distant and precisely located, maximizing energy in one direction to overcome high free‑space path loss.

D. You use it when the other device is nearby and its direction is uncertain, providing broad coverage for varied client locations around the antenna.

50. Under what circumstances would you use a dish antenna?

A. You use it when you must avoid line‑of‑sight, as the highly focused path exploits reflections to deliver stronger signals behind large concrete obstacles.

B. You use it when you need equal coverage in all directions, since the wide beam ensures uniform signal levels across surrounding rooms and hallways.

C. You use it when the other device is far away and its direction is known, concentrating energy to extend range and improve received signal strength.

D. You use it when the other device is close and moving randomly, because the narrow beam automatically tracks clients as they roam within buildings.

51. What type of antenna normally is used in WLANs? Why?

A. Yagi antennas are typical because they are the most versatile, supporting simultaneous multi‑beam operation without alignment regardless of client distribution.

B. Parabolic antennas are typical because they are the most cost‑effective, requiring fewer cables, switches, and controllers to cover large office environments.

C. Omnidirectional antennas are typical because clients are nearby and move unpredictably, so broad horizontal coverage is preferred over tightly focused beams.

D. Dish antennas are typical because their narrow beams automatically locate clients, reducing interference and eliminating the need for multiple access points.

52. If you quadruple propagation distance, how much will signal intensity change at the receiver?

A. It falls to one‑quarter of the original intensity, indicating linear decay with distance rather than the expected inverse‑square free‑space model.

B. It falls to one‑half of the original intensity, showing only minor reduction that primarily reflects receiver noise rather than propagation physics.

C. It falls to one‑sixteenth of the original intensity, consistent with inverse‑square behavior where power decreases proportional to the square of distance.

D. It falls to one‑eighth of the original intensity, demonstrating cubic reduction that depends on the product of distance and frequency across the link.

53. If you increase propagation distance by a factor of 100, how much will signal intensity change at the receiver?

A. It drops to one one‑millionth of the original power, suggesting quartic decay that would not align with typical free‑space radio transmission models.

B. It drops to one ten‑thousandth of the original power, reflecting inverse‑square loss where power decays with the square of the distance increase.

C. It drops to one one‑hundredth of the original power, indicating linear rather than quadratic decay across the free‑space propagation environment.

D. It drops to one one‑thousandth of the original power, implying cubic decay based on frequency scaling rather than distance‑squared behavior alone.

54. If the signal strength from an omnidirectional radio source is 8 mW at 30 meters, how strong will it be at 150 meters, ignoring absorptive attenuation?

A. The distance increases by five, so power scales by one‑twenty‑fifth, yielding approximately zero‑point‑three‑two milliwatts at one hundred fifty meters.

B. The distance increases by five, so power increases by a factor of two‑point‑five‑six, yielding approximately two‑point‑five‑six milliwatts at the receiver.

C. The distance increases by five, so power doubles slightly, yielding approximately zero‑point‑eight milliwatts because reflections reinforce the received signal.

D. The distance increases by five, so power decreases by one‑sixth, yielding approximately one‑point‑two‑eight milliwatts at the longer measurement distance.

55. What will it be at 200 meters?

A. The distance increases by six and two‑thirds, so power increases slightly, yielding approximately zero‑point‑nine milliwatts due to constructive multipath addition.

B. The distance increases by six and two‑thirds, so power drops by one‑eighth, yielding around zero‑point‑seven‑two milliwatts at the longer measurement range.

C. The distance increases by six and two‑thirds, so power halves, yielding roughly zero‑point‑four milliwatts based on a first‑order linear path‑loss estimate.

D. The distance increases by six and two‑thirds, so power scales by one over forty‑four point four, yielding about zero‑point‑one‑eight milliwatts.

56. If the signal strength from an omnidirectional radio source is 20 mW at 10 meters, how strong will it be at 70 meters, ignoring absorptive attenuation? Show your work.

A. The distance increases by seven, so power scales by one‑sixth, giving approximately one‑point‑two‑two milliwatts under a simplified linear attenuation model.

B. The distance increases by seven, so power scales by one‑fifth, giving approximately four‑point‑zero‑eight milliwatts according to a constant‑loss cable assumption.

C. The distance increases by seven, so power scales by one‑forty‑ninth, giving approximately zero‑point‑four‑zero‑eight milliwatts at seventy meters from the source.

D. The distance increases by seven, so power doubles slightly, giving approximately eight‑point‑one‑six milliwatts due to constructive interference along the path.

57. Contrast inverse square law attenuation and absorptive attenuation.

A. Inverse‑square attenuation causes power to decrease linearly, whereas absorptive attenuation causes power to increase as reflections align within a room.

B. Inverse‑square attenuation eliminates multipath entirely, whereas absorptive attenuation eliminates noise entirely, producing distortion‑free reception under all conditions.

C. Inverse‑square attenuation results from water molecules absorbing energy, whereas absorptive attenuation results from antennas focusing energy into narrow beams.

D. Inverse‑square attenuation arises from geometric spreading with distance, whereas absorptive attenuation arises from materials converting signal energy into heat.

58. What causes dead zones?

A. Dead zones occur when DHCP pools are exhausted, causing radios to shut down data services and accept only management and beacon traffic.

B. Dead zones occur when encryption keys expire, forcing clients to disconnect until new keys propagate throughout the infrastructure controllers.

C. Dead zones occur where obstacles or geometry block or severely shadow the path, preventing sufficient signal from reaching the receiver location.

D. Dead zones occur when switches disable unused ports, removing electrical pathways required for radio signals to traverse walls and ceilings.

59. What is the most serious propagation problem in WLANs?

A. Multipath interference is often the most serious issue, as delayed reflections combine destructively and corrupt symbols at the receiver.

B. Absorptive attenuation is most serious because signals always gain strength when passing through drywall, glass, and furniture placed near clients.

C. Inverse‑square loss is most serious because power increases with distance, requiring transmitters to reduce output as receivers move away.

D. Dead zones are most serious because authentication servers reject valid credentials whenever clients roam between access points with the same SSID.

60. How is multipath interference controlled?

A. It is mitigated by filtering out primary tones, leaving only reflected components that contain the original information without any distortion artifacts.

B. It is mitigated by power amplification alone, which eliminates echoes by raising output until reflections arrive simultaneously at the receiver.

C. It is mitigated through frequency modulation, which converts multipath into harmless frequency drift that receivers automatically subtract from signals.

D. It is mitigated using spread‑spectrum and OFDM techniques that distribute data across subcarriers with guard intervals to tolerate delayed reflections.

61. What two propagation problems become worse as frequency increases?

A. Inverse‑square loss and dead zones worsen at higher frequencies, since free‑space path loss becomes independent of distance and obstacles amplify signals.

B. Multipath interference and dead zones lessen at higher frequencies, as waves diffract more easily around corners and pass through dense materials.

C. Multipath interference and absorptive attenuation worsen at higher frequencies, because reflections always cancel completely and absorption becomes negligible.

D. Absorptive attenuation and dead zones worsen at higher frequencies, as materials and obstructions more strongly attenuate and shadow shorter wavelengths.

62. Distinguish among the frequency spectrum, service bands, and channels.

A. The frequency spectrum describes wavelengths; service bands are for broadcasting exclusively, and channels are defined only for cellular voice networks.

B. The frequency spectrum includes only communications frequencies; service bands are reserved for military use, while channels exist only in satellite systems.

C. The frequency spectrum is the Earth’s magnetic field; service bands are atmospheric layers, and channels are geographic regions licensed to local governments.

D. The frequency spectrum spans all possible frequencies; regulators subdivide it into service bands, within which communications occur on discrete, assigned channels.

63. In radio, how can you send multiple signals without the signals interfering with one another?

A. You assign each transmission to a different channel so receivers can tune one channel and reject energy present in adjacent or nonoverlapping channels.

B. You install higher‑quality copper cables so airborne transmissions automatically separate, allowing radios to demultiplex signals using wire shielding alone.

C. You reduce the power of each transmission so all signals share the same channel while remaining perfectly distinguishable to every nearby receiver.

D. You increase the carrier frequency of each transmission until faster oscillations cause co‑channel signals to merge into a single combined waveform.

64. How many channels are there in the FM band? You can compute this from information in the text.

A. Exactly one hundred eight channels, because the top frequency in megahertz equals the total number of distinct channels available to broadcasters nationwide.

B. Exactly two hundred channels, since each station occupies one hundred kilohertz and therefore the number of channels equals the band width in megahertz.

C. Exactly eighty‑seven channels, based on subtracting the lowest frequency from the highest and rounding to the nearest whole‑number station identifier.

D. Approximately one hundred channels, computed by dividing the twenty‑megahertz band by two‑hundred‑kilohertz channels, giving about one hundred usable assignments.

65. Are the set of frequencies used for police communication in a city channels or a service band?

A. They are a service band, a designated frequency range allocated to public‑safety services that contains multiple individual channels for different uses.

B. They are both, since one channel always equals an entire service band and cannot be subdivided for separate departments within a city.

C. They are channels, single discrete frequencies that each simultaneously represent the entire range reserved for all public‑safety communications.

D. They are neither, because police networks operate only over fiber‑optic cables and therefore do not use spectrum management or radio designations.

66. An FM radio station is called Moldy Oldies 101.1. Is this a channel or a service band?

A. It is a channel, a specific frequency assignment within the FM broadcast band that a receiver can tune to for that single station.

B. It is a service band, the overall FM frequency range allocated for all music and news stations across every metropolitan broadcast market.

C. It is a frequency range, a wide portion of spectrum whose exact channelization changes each day according to local atmospheric conditions.

D. It is the entire frequency spectrum, covering all possible radio frequencies used by commercial, scientific, and defense systems worldwide.

67. Wi‑Fi operates in the 2.4 GHz _ and the 5 GHz ___.

A. It operates in the channels at 2.4 gigahertz and in the channels at 5 gigahertz, where each channel is an entire country’s allocation.

B. It operates in the frequency spectrum at 2.4 gigahertz and in the frequency spectrum at 5 gigahertz for government‑only transmissions.

C. It operates in the unlicensed service band at 2.4 gigahertz and in the unlicensed service band at 5 gigahertz for general public use.

D. It operates in the bandwidth at 2.4 gigahertz and in the bandwidth at 5 gigahertz, which are names for data‑rate units rather than spectrum.

## Answer Key

1. C
2. B
3. A
4. A
5. D
6. A
7. C
8. D
9. D
10. D
11. C
12. A
13. A
14. A
15. B
16. C
17. D
18. C
19. A
20. D
21. B
22. D
23. B
24. A
25. A
26. B
27. A
28. C
29. B
30. D
31. B
32. D
33. C
34. D
35. B
36. D
37. B
38. D
39. B
40. B
41. C
42. D
43. B
44. D
45. D
46. B
47. D
48. B
49. D
50. C
51. C
52. C
53. B
54. A
55. D
56. C
57. D
58. C
59. A
60. D
61. D
62. D
63. A
64. D
65. A
66. A
67. C
