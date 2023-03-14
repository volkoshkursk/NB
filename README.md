# Description
NB for exam.

In this branch will be latest debugged code. 
In branch `legacy` you can find code in the state it was passed on exam.
In branch `nouveau` you can find newest version of project.
# Installation

You need create libme.so to run this project. 
For this purpose you need installed python3-dev on your system. For building library run

```
make clean && make
```

Default Python version is 3.8. If you need build for another version run 

```
make clean && make VER=<ver>
```

where instead `<ver>` should be your version.