# html-parser
An html parser retreiving information and generating a text file with these information.

## Getting Started

The script is written in Python therefore you have to install **Python 3**.

### Prerequisites

BeautifulSoup is a Python library for pulling data out of HTML and XML files. Use the packet manager `pip` to install BeautifulSoup :

```
pip install bs4
```

### Running the script

Since the scripts parse an html file, we assume that both python script `main.py` and html file `html_file` are in the same folder.
Run the script as below:

```
python main.py -o html_file
```
A text file is created containing data and information from the html file
The option `-o` enable the Python program to open text file using the native text editor. 

## Author
* **Rémi Nguyen**
