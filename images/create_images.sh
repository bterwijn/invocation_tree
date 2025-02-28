
rm -f compute*.png
python compute.py
rm -f compute0.png
bash create_gif.sh compute

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

rm -f my_range*.png
python my_range.py
rm -f my_range0.png
bash create_gif.sh my_range

rm -f generator_function*.png
python generator_function.py
rm -f generator_function0.png
bash create_gif.sh generator_function

rm -f generator_expression*.png
python generator_expression.py
rm -f generator_expression0.png
bash create_gif.sh generator_expression

rm -f generator_pipeline*.png
python generator_pipeline.py
rm -f generator_pipeline0.png
bash create_gif.sh generator_pipeline

