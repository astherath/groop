# set filename here
filename="CHAT_ORIGINAL.txt"

# take out all unwanteds
vim $filename +:%s/\%u200b//g +:%s/\%u200d//g +:%s/\%u200e//g +wall +qall
