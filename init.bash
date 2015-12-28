cd seguinus
cp -n settings.py.example settings.py
cd ..
cp -n preferences.example preferences.py
python manage.py loaddata initData.json
