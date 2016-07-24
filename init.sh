cd seguinus
if [ ! -f settings.py ]; then
    echo "copy settings"
    cp -nv settings.py.example settings.py
fi
cd ..
if [ ! -f preferences.py ]; then
    echo "copy preferences"
    cp -nv preferences.py.example preferences.py 
fi
python manage.py migrate
python manage.py loaddata initData.json 
#end
