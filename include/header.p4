/***************************************************/
/*************** headers' definition ***************/
/***************************************************/

#define LEN         1000 
#define INDEX_LEN   20 

header_type ethernet_t {
    fields {
        dstAddr   : 48;
        srcAddr   : 48;
        etherType : 16;
    }
}

header_type vlan_tag_t  {
    fields  {
       	pri       : 3;
       	cfi       : 1;
       	vlan_id   : 12;
       	etherType : 16;
   }
}

header_type ipv4_t {
    fields {
       	version        : 4;
        ihl            : 4;
       	diffserv       : 6;
       	ecn            : 2;
        totalLen       : 16;
        identification : 16;
        flags          : 3;
       	fragOffset     : 13;
        ttl            : 8;
        protocol       : 8;
        hdrChecksum    : 16;
        srcAddr        : 32;
        dstAddr        : 32;
   }
}

header_type tcp_t {
    fields {
      	srcPort    : 16;
        dstPort    : 16;
       	seqNo      : 32;
        ackNo      : 32;
       	dataOffset : 4;
        res        : 3;
       	ecn        : 3;
        ctrl       : 6;
       	window     : 16;
       	checksum   : 16;
        urgentPtr  : 16;
    }
}

header_type udp_t {
    fields {
       	srcPort    : 16;
        dstPort    : 16;
        hdr_length : 16;
       	checksum   : 16;
    }
}

header_type custom_metadata_t {
    fields {
        pktcounter : 32;
    }
}

metadata custom_metadata_t meta;
header ethernet_t ethernet;
header vlan_tag_t vlan_tag;
header ipv4_t     ipv4;
header tcp_t      tcp;
header udp_t      udp;
