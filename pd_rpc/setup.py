clear_all()

port_of_worker = [56, 48, 40, 32, 24, 16, 8, 0, 4]
MAC_address_of_worker = [ "b8:59:9f:1d:04:f2"
                        , "b8:59:9f:0b:30:72"
                        , "98:03:9b:03:46:50"
                        , "b8:59:9f:02:0d:14"
                        , "b8:59:9f:b0:2d:50"
                        , "b8:59:9f:b0:2b:b0"
                        , "b8:59:9f:b0:2b:b8"
                        , "b8:59:9f:b0:2d:18"
                        , "b8:59:9f:b0:2d:58" ]

len_workers = len(port_of_worker)

# Normal Switch traffic
for i in range(len(port_of_worker)):
    p4_pd.forward_table_add_with_set_egr(
        p4_pd.forward_match_spec_t(macAddr_to_string(MAC_address_of_worker[i])),
        p4_pd.set_egr_action_spec_t(port_of_worker[i])
    )

# conn_mgr.complete_operations()
