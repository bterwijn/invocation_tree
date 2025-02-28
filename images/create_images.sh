
rm -f students*.png
python students.py
rm -f students0.png
bash create_gif.sh students

rm -f factorial*.png
python factorial.py
rm -f factorial0.png
bash create_gif.sh factorial

rm -f permutations*.png
python permutations.py
rm -f permutations0.png
bash create_gif.sh permutations

rm -f generator_function*.png
python generator_function.py
rm -f generator_function0.png
bash create_gif.sh generator_function

rm -f generator_expression*.png
python generator_expression.py
rm -f generator_expression0.png
bash create_gif.sh generator_expression

