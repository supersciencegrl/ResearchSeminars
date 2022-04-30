# ResearchSeminars
Python-led interaction with API for <a href="https://researchseminars.org">https://researchseminars.org</a>. The main file here is _researchseminars.py_, which interacts with the Research Seminars API. This was originally used to migrate my list of online chemistry events (conferences, webinars, etc; archive list <a href="https://supersciencegrl.co.uk/online-old">here</a>) that I kept at the start of the pandemic, but can be used to add any chemistry event or list of events to Research Seminars. 

Note: The `warnings.simplefilter()` at the end of the script is used to work with corporate proxy servers. In less strict environments, it may be more secure to comment out this line to ensure warnings are displayed. 
