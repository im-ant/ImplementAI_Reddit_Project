#=================
# Script to Extract companies
#=================

#NOTE: DO NOT INCLUDE SLASHES IN DIRECTORY INPUT NAMES
#NOTE: RUN IN THE LOCAL DIRECTORY OF THE COMPRESSED FILES

#VARIABLES
OUT_DIR=$1
PY_SCRIPT=$2

# Iterate over all files in the directory
for file in `ls` ; do
	#Check to see if the file is not a compression file
	if [[ $file != *.bz2 ]] ; then
		continue
	fi
	
	#If compressed, save its post-decompression name
	decom_name="`basename  $file .bz2`"
	
	#Decompress the file
	bzip2 -d $file 

	#Create a post-truncated name
	out_name=$decom_name"_companies.json"
		
	#Run the input file into the python script
	python $PY_SCRIPT $decom_name $OUT_DIR$out_name
	
	#Remove the input file
	rm $decom_name
done


#bzip2 -dc $ZIPPED_FILE | less

#hmm
