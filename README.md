# Movie ETL
Simple project that read a list o movies, search information about the Movie on [OMDb API](https://www.omdbapi.com/) and creates a html with the Movies Specifications and upload to a S3 bucket on AWS

The content available on this repository is for study porpose for the ETL exercise on the Bootcamp available on [DIO](web.dio.me/)

# Requirements
- Have Python 3.10 installed
- Create an API tokeon on OMDb website,you can access this [link](https://www.omdbapi.com/apikey.aspx)
- Have an AWS Account key pair configured, and a bucket created.


### Extraction Step
Read the Movies available on file movies.csv, for this exercise the list contains 10 movies that I like. You can change for yours if you want

### Transform Step
Get the information of the movies (provided on Extraction Step) on the OMDb API website, and create a simple html file using those informations

### Load Step
Upload the html file created on 'Transform Step' and upload on AWS S3 bucket

# How To
To Script works, you need to update the script with your OMDb API token and add on variable ***OMDB_API_KEY*** and provide your S3 Bucket name in the variable ***BUCKET_NAME***

After that just run the command
```
python etl.py
```

You can check the html from my list on the link:
[https://etl-movie-list.s3.us-east-2.amazonaws.com/index.html](https://etl-movie-list.s3.us-east-2.amazonaws.com/index.html)





