THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
NF_NAME="sample_switch_14"

# Compiling the P4 program
#   All build files will be placed in $SDE/build/p4-build/$NF_NAME
#   All logs will be placed in $SDE/logs/p4-build/$NF_NAME
#   All final artifacts will be placed in $SDE_INSTALL
#   
# There is an spelling error in p4_build.sh : --enalbe-thrift rather than --enable_thrift
all:
	bash ${SDE}/tools/p4_build.sh ${NF_NAME}

.PHONY : clean
clean : 
	rm bf_drivers.log*
	rm zlog-cfg-cur
	rm ptf.log
	rm ptf.pcap

