#!/bin/bash -i
# wrapper script for FYP env operations 

main(){
	DIR=/src/fyp/qol_scripts
		
	cd $DIR
	if [ $FYP_COMMAND == "up" ]; then
		./fyp_env_up.sh
	elif [ "$FYP_COMMAND" == "down" ]; then 
		./fyp_env_down.sh
	elif [ "$FYP_COMMAND" == "todo" ]; then 
		./fyp_print_todo.sh
	elif [ "$FYP_COMMAND" == "cd" ]; then
		cd ..
		echo "moved to `pwd`"
	elif [ "$FYP_COMMAND" == "help" ]; then 
		print_help
	else 
		echo "bad command - please insure this script is installed in $DIR"
		echo
		print_help
	fi
}

print_help(){
	cat << EOF 
fyp up - sets up environment
fyp down - tears down environment 
fyp todo - show current to-do list
fyp cd - moves to fyp workplace, must be run at current location by putting a . in front of command.  
fyp help - shows this help 
EOF
}

FYP_COMMAND=$1
main

