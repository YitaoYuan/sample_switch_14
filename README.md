### Get started with Tofino:
#### Introduction: 
  1. This code behaves like a stupid switch, in which the mapping between MAC address and egress port is configured statically. 
  2. Please remember to load the Tofino kernel mode driver (bf_kdrc.ko) each time the CPU is rebooted (cd $SDE && sudo ./install/bin/bf_kdrv_mod_load $SDE_INSTALL).


#### Tofino:
#### Usage
  ```
  +-----------------------------------------------------+         +-----------------------------------------------------+
  |                     Terminal 1                      |         |                     Terminal 2                      |
  +-----------------------------------------------------+         +-----------------------------------------------------+
  |                                                     |         |                                                     |
  | ../../run_switchd.sh -p envTest                     |         | ../../run_p4_tests.sh -t ptf/ -p envTest            | 
  |                                                     |         |                                                     |
  +-----------------------------------------------------+         +-----------------------------------------------------+
  ```
