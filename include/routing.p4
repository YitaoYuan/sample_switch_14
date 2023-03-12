action set_egr(egress_spec) {
    modify_field(ig_intr_md_for_tm.ucast_egress_port, egress_spec);
}

action nop() {
}

table forward {
    reads {
        ethernet.dstAddr : exact;
    }
    actions {
        set_egr; 
        nop;
    }
}
