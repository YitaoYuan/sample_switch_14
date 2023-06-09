import logging
import os
import pd_base_tests
import pltfm_pm_rpc
import pal_rpc
import random
import sys
import time
import unittest

from envTest.p4_pd_rpc.ttypes import *
from pltfm_pm_rpc.ttypes import *
from pal_rpc.ttypes import *
from ptf import config
from ptf.testutils import *
from ptf.thriftutils import *
from res_pd_rpc.ttypes import *

from ptf import config
from ptf.thriftutils import *

from res_pd_rpc.ttypes import *
from port_mapping import *
from tm_api_rpc.ttypes import *

this_dir = os.path.dirname(os.path.abspath(__file__))
# fp_ports = ["9/0", "10/0", "11/0", "12/0", "13/0", "14/0", "15/0", "16/0", "17/0", "18/0", "19/0"]
fp_ports = [str(loop)+"/0" for loop in range(0, 64)]
NF_NAME  = "envTest"

def toInt8(n):
  n = n & 0xff
  return (n ^ 0x80) - 0x80

class L2Test(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, [NF_NAME])

    # The setUp() method is used to prepare the test fixture. Typically
    # you would use it to establich connection to the Thrift server.
    #
    # You can also put the initial device configuration there. However,
    # if during this process an error is encountered, it will be considered
    # as a test error (meaning the test is incorrect),
    # rather than a test failure
    def setUp(self):
        # initialize the connection
        pd_base_tests.ThriftInterfaceDataPlane.setUp(self)
        self.sess_hdl = self.conn_mgr.client_init()
        self.dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))
        self.devPorts = []
        self.dev = 0

        self.platform_type = "mavericks"
        board_type = self.pltfm_pm.pltfm_pm_board_type_get()
        if re.search("0x0234|0x1234|0x4234|0x5234", hex(board_type)):
            self.platform_type = "mavericks"
        elif re.search("0x2234|0x3234", hex(board_type)):
            self.platform_type = "montara"

        # get the device ports from front panel ports
        try:
            for fpPort in fp_ports:
                port, chnl = fpPort.split("/")
                devPort = \
                    self.pal.pal_port_front_panel_port_to_dev_port_get(0,
                                                                    int(port),
                                                                    int(chnl))
                self.devPorts.append(devPort)

            if test_param_get('setup') == True or (test_param_get('setup') != True
                and test_param_get('cleanup') != True):

                # add and enable the platform ports
                for i in self.devPorts:
                    self.pal.pal_port_add(0, i,
                                        pal_port_speed_t.BF_SPEED_100G,
                                        pal_fec_type_t.BF_FEC_TYP_NONE)
                    self.pal.pal_port_an_set(0, i, 2)
                    self.pal.pal_port_enable(0, i)
                self.conn_mgr.complete_operations(self.sess_hdl)
        except Exception as e:
		print "Some Error in port init"
        # # flow control setting, follow "Barefoot Network Tofino Fixed Function API Guide"
        for i in range(len(self.devPorts)):
            # step 1: Map loessless traffice to a PPG handle with a buffer limit
            ppg_cells = 2000
            self.ppg_handler = self.tm.tm_allocate_ppg(self.dev, self.devPorts[i])
            self.tm.tm_set_ppg_guaranteed_min_limit(self.dev, self.ppg_handler, ppg_cells)

            # step 2: Map traffic to an iCos
            icos_bmap = toInt8(0x01)
            self.tm.tm_set_ppg_icos_mapping(self.dev, self.ppg_handler, icos_bmap)

            # step 3: Provision skid buffer set up pasue PFC generation
            skid_cells = 4000
            self.tm.tm_set_ppg_skid_limit(self.dev, self.ppg_handler, skid_cells)
            self.tm.tm_enable_lossless_treatment(self.dev, self.ppg_handler)
            # link-level flow control
            fctype = 1 # BF_TM_PAUSE_PORT
            self.tm.tm_set_port_flowcontrol_mode(self.dev, self.devPorts[i], fctype)
            # iCos to Cos
            # icos_cos_map = tm_pfc_cos_map_t(CoS0_to_iCos=0)
            icos_cos_map = tm_pfc_cos_map_t(0, 1, 2, 3, 4, 5, 6, 7)
            self.tm.tm_set_port_pfc_cos_mapping(self.dev, self.devPorts[i], icos_cos_map)

        ##########################################
        for i in range(len(self.devPorts)):
            #step 4: Apply buffering
            queue_id = 0
            queue_cells = 25000
            self.tm.tm_set_q_guaranteed_min_limit(self.dev, self.devPorts[i], queue_id, queue_cells)

            # step 5: Allocate queues
            q_count = 8
            q_map = tm_q_map_t(0,1,2,3,4,5,6,7)
            self.tm.tm_set_port_q_mapping(self.dev, self.devPorts[i], q_count, q_map)
            # step 6: Apply weighting if needed (skip, no use)

            # step 7: Honor pause/PFC event
            cos = 0
            self.tm.tm_set_q_pfc_cos_mapping(self.dev, self.devPorts[i], queue_id, cos)

        # Can not find below API
        # self.tm.tm_set_port_flowcontrol_rx(self.dev, self.devPorts, fctype)
        self.tm.tm_complete_operations(self.dev)

        for i in range(len(self.devPorts)):
            # For MAC
            self.pal.pal_port_flow_control_pfc_set(self.dev, self.devPorts[i], 1, 1)
        print("Done with PFC")

    def runTest(self):
        self.client.forward_set_default_action_nop(self.sess_hdl,self.dev_tgt);
        print()
        print("*************** Installing table entries ***************")
        self.entries = {} 

        self.entries["forward"] = []
        routing_entry = [
            ("b8:59:9f:1d:04:f2", 24), # worker1 <enp178s0f0: 192.168.0.1>
            ("b8:59:9f:0b:30:72", 16), # worker2 <enp178s0f0: 192.168.0.2>
            ("98:03:9b:03:46:50", 32), # worker <enp178s0f0: 192.168.0.3>
            ("b8:59:9f:02:0d:14", 40), # worker <enp178s0f0: 192.168.0.4>
        ] 
        for entry in routing_entry:
            self.entries["forward"].append(
                self.client.forward_table_add_with_set_egr(self.sess_hdl, self.dev_tgt,
                    envTest_forward_match_spec_t(ethernet_dstAddr=macAddr_to_string(entry[0])),
                    envTest_set_egr_action_spec_t(action_egress_spec=entry[1])))
        
        '''
        while True:
             instruction=raw_input("type stop to finish the task : ")
             if instruction == 'stop':
                 break
        '''

    # Use this method to return the DUT to the initial state by cleaning
    # all the configuration and clearing up the connection
    def tearDown(self):
        try:
            print("*************** Clearing table entries ***************")
            '''
            for table in self.entries.keys():
                print("TABLE_DEL : " + table)
                delete_func = "self.client." + table + "_table_delete"
                for entry in self.entries[table]:
                    exec delete_func + "(self.sess_hdl, 0, entry)"
            '''
        except:
            print("Error while cleaning up. ")
            print("You might need to restart the driver")
        finally:
            self.conn_mgr.complete_operations(self.sess_hdl)
            self.conn_mgr.client_cleanup(self.sess_hdl)
            print("Closed Session %d" % self.sess_hdl)
            pd_base_tests.ThriftInterfaceDataPlane.tearDown(self)
