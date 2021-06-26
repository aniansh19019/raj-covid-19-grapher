# Covid-19 Grapher

This is a python flask based web application for generating and exporting graphs and animations for the different data elements associated with the Covid-19 pandemic. 

The web app allows anyone to generate almost all possible graphs concerning the current Covid-19 Pandemic. I have tried to make the whole process as simple and self explanatory as possible. The user just selects the relevant options and then proceeds to view/download the generated graph/animation. 

## Setup

The flask server runs using a python virtual environment for dependencies.
```
git clone https://github.com/aniansh19019/raj-covid-19-grapher.git
cd raj-covid-19-grapher
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
flask run
```
The webapp will be hosted on localhost this way and can be accessed using the address displayed in the terminal.

## Credits and Sources

Thanks to <a href="https://github.com/CSSEGISandData/COVID-19" target="_blank">John Hopkins University</a> for making the data publicly available.
<br>
Thanks to <a href="https://blog.miguelgrinberg.com/" target="_blank">Miguel Grinberg</a> for the awesome <a href="https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world" target="_blank">Flask tutorial</a>.
<br>
Mainly coded in <a href="https://www.python.org/" target="_blank">Python</a>.
<br>
Plots created using <a href="https://matplotlib.org/" target="_blank"> Matplotlib</a>.
<br>
Web interface created using <a href="https://flask.palletsprojects.com/en/1.1.x/" target="_blank">Flask</a>, <a href="https://wtforms.readthedocs.io/en/stable/" target="_blank">WT-forms</a> and <a href="	https://getbootstrap.com/" target="_blank">Bootstrap</a> including icons from <a href="	https://fontawesome.com/" target="_blank">Font Awesome</a>.
<br>
