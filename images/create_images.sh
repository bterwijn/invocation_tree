
rm -f students*.png
python students.py
rm -f students0.png
bash create_gif.sh students

rm -f factorial*.png
python factorial.py
rm -f factorial0.png
bash create_gif.sh factorial
