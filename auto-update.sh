PATH=/home/lubianat/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/lib/pkgconfig:/snap/bin
cd ~/Documents/my_random_stuff/read-the-classics-karen/Europe-PMC-classics

python3 update_classics.py

cp README.md ../README.md

cd ..
git add . 
git commit -m "Automatic update of the EuropePMC list of classics"
git push
