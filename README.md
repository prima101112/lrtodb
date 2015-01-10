# lrtodb
this is an python script that save svn or git log to mongodb or elasticsearch.

## requirement
- python 2.7
- elasticsearch or mongodb
- elasticsearch python client or pymongo

## how to run
there is 2 steps to export the log.

### 1. export log svn or git
`svn log > svnlog.log` 
`git log > gitlog.log`
you can try the script with example log in the script

### 2. run the script
this just simple run script
{repo} = svn or git
{file log} = log.log
{database} = mongo or elasticsearch
`python logrepo.py {repo} {file log} {database}`