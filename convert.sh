cd /Users/claudiu/Documents/Projects/parsec-jupyter
jupyter nbconvert --execute --to markdown index.ipynb --no-input
cd r
jupyter nbconvert --execute --to markdown *.ipynb --no-input
cd ..

