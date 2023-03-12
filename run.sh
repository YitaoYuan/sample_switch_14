#!/bin/bash

#################################################
NF_NAME="envTest"
#################################################

# Para :
#     ${1} : time (seconds)
#
progress_bar() {
    if [ ! ${1} ]; then
        echo_erro "usage: ${FUNCNAME} time"
	exit 0
    fi
    if [ ${1} -le 0 ]; then
        echo_erro "usage: ${FUNCNAME} time"
	exit 0
    fi
    bTool=''
    curTool=0
    intervalTool=1
    maxlenTool=50
    temptimeTool=$((${1}-1))
    intervalTool=`expr ${temptimeTool} / ${maxlenTool}`
    intervalTool=$((${intervalTool}+1))
    barlenTool=$((${1}/${intervalTool}))
    while [ ${curTool} -le ${1} ]
    do
        printf "[${color_yellow}WAIT${color_reset}] [${color_green}%-${barlenTool}s${color_reset}] [%2d/%d] \r" "$bTool" "${curTool}" "${1}";
        bTool+="#"
        ((curTool=curTool+${intervalTool}))
        sleep ${intervalTool}
    done
    echo ""
}

PID=`pgrep bf_switchd`
if [ ${PID} ]; then
    echo "bf_switchd is running! Please kill it! (kill ${PID})"
    exit 0
fi

$SDE/run_switchd.sh -p ${NF_NAME} >/dev/null 2>&1 &
echo "Teminal this program with -- kill 'pgrep bf_switchd'"
progress_bar 20

$SDE/run_p4_tests.sh -t ptf/ -p ${NF_NAME}
