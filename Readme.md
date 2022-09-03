# It's fine

Ever had your python imports not working? Don't worry, it's fine. Just `import itsfine`.

```shell
pip install itsfine
```

```python
>>> import numpy
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'numpy'
>>> import itsfine
>>> import numpy
>>> numpy.arange(100).sum()
All good {}
```

You can also preload it in your python shell with `python -i -c "import itsfine"`.

Convinced? Make it permanent with `Fix.for_good()`:

```shell
$ python -c "import numpy; print(numpy.arange(10))"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'numpy'
$ python -c "from itsfine import Fix; Fix.for_good()"
$ python -c "import numpy; print(numpy.arange(10))"
All good
```

Also works in jupyter notebooks:

![Screenshot of a jupyter notebook running in the jupyter browser gui, details in demo/demo.ipynb and demo/screenshot 3 alt.txt 
](demo/screenshot%203.png)