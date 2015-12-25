if zenity --question --text "Voulez vous imprimer les doubles quotidiens?"
then
	firefox "https://127.0.0.1/easyPoS/factures/doubles/printHier"
    else
        echo "Abort."
    fi

