PATH=/home/lubianat/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/lib/pkgconfig:/snap/bin
cd ~/Documents/my_random_stuff/read-the-classics-karen/Europe-PMC-classics

runipy getting_europepemc_classics.ipynb

cd ..
git add . 
git commit -m "Automatic update of the EuropePMC list of classics"
git push
