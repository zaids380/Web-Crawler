# Web-Crawler
My first web scrapping project

---installation---

extract the files and go to project folder

open terminal in the folder and execute the below commands

assuming python3 and pip3 already installed

**execute the following commands**

sudo apt-get install python3-tk

pip3 install -r requirements.txt

**if this doesn't work**

pip3 install selenium

pip3 install beautifulsoup4

pip3 install pandas

pip3 install requests

**install the chrome driver and provide appropriate path in main.py on line no 332**

**run the file**

python3 main.py


**flow of the application**

 1. Enter a Product like mobile, penrive, mobile charger, laptop charger, routers etc(tested on these products)
 2. click search.
 3. other widgets will get visible
 4. for other details default values are already set, change if needed and click submit.
 5. let the program run at the end file name data.csv will be created in the project folder containing fetched products.  
