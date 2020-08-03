Document Summarizer 

The code in this project was designed to use NLP and web scraping tools to both classify the content of documents / html text, summarize the content of documents / html text and break apart html pages so that only analyzable text is present and one can perform a proper reading of valuable data from the page 

1 Document Classifier 
This tool uses beautiful soup in combination with test data to classify text from documents or scraped from sites using the Naive Bayes (NB) classifier provided by sklearn and trained on a series of sets of example data.

How to use:
first make sure you have all libraries installed in your condo environment or a virtual one you have set up 

Next simply run the doc_classifier.py with the command in terminal

python doc_classifier.py 

Or from your python IDE of choice such as Spyder 

From there follow the prompts to classify your own text or some of the example files or a target page 


2 Document Summarizer
This tool uses Sumy and wx python UI to generate a interface where you can choose documents and have the tool break down massive text into a full text summery of the chosen topic.

How to use:
first make sure you have all libraries installed in your condo environment or a virtual one you have set up 

Next simply run the doc_summarizer.py with the command in terminal or using an IDE
NOTE : if you are on mac you will have to run the command pythonw doc_summarizer.py - for wxpython to work 






