#include <tofino/intrinsic_metadata.p4>
#include <tofino/stateful_alu_blackbox.p4>
#include <tofino/constants.p4>

#include "include/header.p4"
#include "include/parser.p4"
#include "include/routing.p4"


/*********************************************************/
/*************** control ingress && egress ***************/
/*********************************************************/

control ingress {
	apply(forward);
}

control egress {
}

