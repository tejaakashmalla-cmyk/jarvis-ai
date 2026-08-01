from coding.debugger.error_parser import ErrorParser


parser = ErrorParser()

stderr = """
Traceback (most recent call last):
  File "C:/Projects/ExpenseTracker/models/user.py", line 18, in <module>
    main()
NameError: UserModel is not defined
"""

error = parser.parse(stderr)

print(error)

parser.summary(error)