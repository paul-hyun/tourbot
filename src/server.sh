#!/bin/sh

##########################################################
# General Environment
##########################################################
KILL_CMD=`which kill`
TAIL_CMD=`which tail`

APP_HOME=/home/chatbot/tourbot/src

SERVICE_NAME='TourBot Again'

USER_DIR=`pwd`

##########################################################
# Check Running
##########################################################
CheckRunning()
{
	if [ -f $APP_HOME/.pid ]; then
                Alive_Flag=1
		PID=`cat $APP_HOME/.pid`
	else
                Alive_Flag=0
	fi
}

##########################################################
# Program Running
##########################################################
case "$1" in
'start')
        echo
        echo "         << $SERVICE_NAME Start >>"
        echo
        CheckRunning
        if [ $Alive_Flag != 1 ]
        then
                echo "     >> Starting $SERVICE_NAME process ..."
		cd $APP_HOME
		nohup /home/chatbot/anaconda3/envs/chatbot/bin/python server.py &
		echo $! > .pid
                sleep 5

                CheckRunning
                if [ ${Alive_Flag} = 1 ]
                then
                        echo "     >> $SERVICE_NAME system was started. [PID=$PID]"
                fi
        else
                echo "     >> $SERVICE_NAME system is already running. [PID=$PID]"
        fi
        echo
        echo
        ;;

'stop')
        echo
        echo "         << $SERVICE_NAME Stop >>"
        echo
        echo "     >> Stopping $SERVICE_NAME process ..."
        CheckRunning
        if [ $Alive_Flag != 0 ]
        then
		cd $APP_HOME
		kill -9 $PID
		rm .pid
                echo "     >> $SERVICE_NAME system was stopped. [PID=$PID]"
        else
                echo "     >> $SERVICE_NAME system is already stopped."

        fi

        echo
        echo
        ;;

'status')
        echo
        echo "         << $SERVICE_NAME Check >>"
        echo
        CheckRunning
        if [ $Alive_Flag != 0 ]
        then
                echo "     >> $SERVICE_NAME system is running. [PID=$PID]"
        else
                echo "     >> $SERVICE_NAME system is not running."
        fi
        echo
        echo
        ;;

*)
    echo "Usage: $0 { start | stop | status }"
    exit 1
    ;;
esac
exit 0

