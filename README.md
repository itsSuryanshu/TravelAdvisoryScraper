# TravelAdvisoryScraper

This branch has been updated to show implementation of the scraper for use in an AWS Lambda function. Big changes include:

- Pandas library not being imported as it can be added in as a Layer inside of the Lambda function
- `main.py` has been renamed to `lambda_function.py`
- CSV file's name updated and saving location has changed to work with Lambda
- Uses boto3 for file upload to AWS Lambda

With these changes, the project doesn't work the same as the main branch does (with the terminal). I suggest checking out this [repository](https://github.com/aissa-laribi/bs4-in-lambda) by [@aissa-laribi](https://github.com/aissa-laribi) for how to package your finished code for use with AWS Lambda.
