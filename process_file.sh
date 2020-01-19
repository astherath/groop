pathToOriginal="/Users/felipearce/Downloads/CHAT_ORIGINAL.txt"
# save orig file
cp $pathToOriginal .

# set filename here
filename="CHAT_ORIGINAL.txt"

# take out all unwanteds
vim $filename -c ':%s/\%u200e//g' -c ':%s/\%u200d//g' -c ':%s/\%u202a' -c ':%s/\%u202c' -c 'wq'
vim $filename -c ':%s/Felipe Cool Guy ...../Felipe/g' -c ':%s/Quinns P/Quinn/g' -c ':%s/Babakweiner Rohani ./Babak/g' -c 'wq'
vim $filename -c ':%s/John Mass Effect Jr. ...../John/g' -c ':%s/Israel Zion/Israel/g' -c ':%s/el Cowboy Man Morales//g' -c 'wq'
vim $filename -c ':%s/Evan The Hot One/Evan/g' -c ':%s/Cynder Leon Haynes Sr/Cynder/g' -c ':%s/Jimmy Jam/Jimmy/g' -c 'wq'
vim $filename -c ':%s/+1 (786) 925-3927/Jose/g' -c ':%s/Justin Eastwood/Justin/g' -c ':%s/Hannan Rhodes/Hannan/g' -c 'wq'
vim $filename -c ':%s/Liam Arzola/Liam/g' -c ':%s/+1 (305) 431‑8141/Josh/g' -c ':%s/Matias The One With The Heart ....../Matias/g' -c 'wq'
vim $filename -c ':%s/Martin Penis Vaginer Queen/Martin/g'  -c ':%s/Collin Ridge Rock ...../Collin/g' -c ':%s/Davo The Boy/Davo/g' -c 'wq'
vim $filename -c ':%s/Fabreeze Pierez?/Fabricio/g' -c ':%s/+34 674 26 01 40/Rai/g' -c ':%s/Aron Delevic/Aron/g' -c 'wq'
# vim $filename -c '

# +:%s/\%u200d//g +:%s/\%u200e//g +:%s/\%u202a +:%s/\%u202c +wall +qall -c ':%s/'

# -c ':%s/Felipe Cool Guy ...../Felipe/g' -c ':%s/Quinns P/Quinn/g' -c ':%s/Babakweiner Rohani ./Babak/g' -c ':%s/John Mass Effect Jr. ...../John/g' -c ':%s/Israel Zion/Israel/g' -c ':%s/el Cowboy Man Morales//g' -c ':%s/Evan The Hot One/Evan/g' -c ':%s/Cynder Leon Haynes Sr/Cynder/g' -c ':%s/Jimmy Jam/Jimmy/g' -c ':%s/+1 (786) 925‑3927/Jose/g' -c ':%s/Justin Eastwood/Justin/g' -c ':%s/Hannan Rhodes/Hannan/g' -c ':%s/Liam Arzola/Liam/g' -c ':%s/+1 (305) 431‑8141/Josh/g' -c ':%s/Matias The One With The Heart ....../Matias/g' -c ':%s/Martin Penis Vaginer Queen/Martin/g'