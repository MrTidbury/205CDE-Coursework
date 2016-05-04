# Jack Tidbury 205CDE Coursework

How to add a new commit to this repository from the c9 workspace

```sh
$ git add .
$ git status
$ git commit
```
It will now ask you to make a title for the commit, once done exit and then press Y then enter
```sh
$ git push
```
You should see some stuff pop up and then it is done, go and check GITHUB to make sure.

## How to work inside the virtual enviroment

```sh
$ virtualenv venv
$ . venv/bin/activate
mysql-ctl start

```
To run the main.py file, and thus the webserver, run this command
```sh
$(venv) python main.py
```
