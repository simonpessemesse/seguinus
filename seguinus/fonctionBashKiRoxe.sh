
function setdsm() { 
    # add the current directory and the parent directory to PYTHONPATH
    # sets DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$PYTHONPATH:$PWD/..
    export PYTHONPATH=$PYTHONPATH:$PWD
    if [ -z "$1" ]; then 
        x=${PWD/\/[^\/]*\/}               
        export DJANGO_SETTINGS_MODULE=$x.settings
    else    
        export DJANGO_SETTINGS_MODULE=$1 
    fi

    echo "DJANGO_SETTINGS_MODULE set to $DJANGO_SETTINGS_MODULE"
}

