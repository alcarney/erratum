v0.1.1 - 29/04/18
-----------------

- **NEW:** Error definitions can also be used as a context manager, useful
  for when you only want the Error to catch exceptions in a particular block
  of code rather than an entire function. e.g.

  .. code-block:: python

      with SqrtError():
	      math.sqrt(-1)

v0.1.0 - 28/04/18
-----------------

- **CHANGED:** Cleaner syntax for annotating functions with errors you now
  simply use the class name e.g.

  .. code-block:: python

      @SqrtError
	  def mysqrt(x):
	      ...

- **FIXED:** Text in the output of the erratum.document command now has the
  proper indentation


v0.0.1 - 09/04/18
-----------------

Initial release
