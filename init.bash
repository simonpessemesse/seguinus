cd seguinus
cp -nv settings.py.example settings.py
cd ..
cp -nv preferences.py.example preferences.py 
python manage.py migrate
python manage.py loaddata initData.json # TODO only execute this if there was no previous settings.py
