
#rm -f compute*.png
#python compute.py
#rm -f compute0.png
#bash create_gif.sh compute -d

#rm -f students*.png
#python students.py
#rm -f students0.png
#bash create_gif.sh students -d

rm -f factorial*.png
python factorial.py
rm -f factorial0.png
bash create_gif.sh factorial -d

python permutations_dot.py perms_LR3.png LR 3

rm -f permutations*.png
python permutations.py
rm -f permutations0.png
bash create_gif.sh permutations -d

rm -f permutations_neighbor*.png
python permutations_neighbor.py
rm -f permutations_neighbor0.png
bash create_gif.sh permutations_neighbor -d

python draw_graph.py 10 2 graph_small 2 > edges_small.out
python draw_graph.py 26 3 graph_big 1 > edges_big.out
