# Finding files in S3 

## find-files-with-substring.py 

Allows you to look for a text file of the types 

* Text 
* CSV - comma separated values 
* JSON format 

run the script and interactively add the bucket and the substring you are looking for 

##  find-any-file-with-substring.py

Allows you to look for a  file of all types


run the script and interactively add the bucket name you know  and the substring you are looking for 

Note: a validation check has been added to catch potential errors 
eg: invalid Bucket name. 

## find-any-file-in-any-bucket.py

Allows you to look for a file of all types, however it will also retrieve for you the list of Buckets from the S3 resource. Should be used only by DevSecOps with access to the account.  


## Deployment 

### Pre-condition 

You must have AWS CLI set up in you environment - if not [go here to set up ](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 

### To set up 

Scripts are written and tested in python 3.11 

1. download from  [here](https://github.com/lislema/aws-python-boto)
2. install python 3.11
3. ensure you set up you virtual environment -> *python -m venv venv*
4. Activate your virtual environment -> ./venv/bin/activate 
5. install the boto3 package -> pip install boto3 