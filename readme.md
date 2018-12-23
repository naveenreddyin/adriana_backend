# This is the backend for Adriana project
## To run
1. Create virtualenv with python 3 
2. Clone this repository and run pip install -r requirements.txt
3. Run command 'python manage.py migrate' to generate sqlite database.
4. The test coverage is 94%, to see it, run 'coverage run --source='.' manage.py test' and than 'coverage report'
5. This views and models are properly tested.

## Limitations and future improvements
1. More than 5 answers to a question is not permitted now.
2. It only has GET method to fetch the question and answers, so we cant create anything new. 
3. There are two api urls, in reality 3 but two are for the same purpose and clarity, but the 'load' api helps to load the json file from root dir, it is named in settings file, i.e; settings.py -> data.json
4. The structure of json is loaded into db, for the clarity sake, pk field could change but wont have any affect on the program or on frontend. 
5. The json structure should not be in relational db, rather it should be in NoSQL databases as it is more of a graph.
