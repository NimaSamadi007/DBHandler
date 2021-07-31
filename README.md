# DBHandler
A simple database handler class

# Description

This is a simple class which can be used to read and write data from and to database. SQlite database is used with this class. Various functions are provided which I'll introduce them briefly. 

# Usage:

Put this class along with your scripts. First make sure you have `numpy` library. Next import the class into your code, using `import DBHandler [as db]` (the rest is optional). Now create a object using this command:

``` dbcommand = DBHandler(" Your database address ") ```

Now you can make tables using this command:

``` dbcommand.CreateTable("table name", ["column1 name", "column2 name", ....]) ```

Now database is ready to be used!

# Write to database

multiple function are provided to write to database. one method is `[database objectname].WriteCol('table name', 'column name', data) ` which can be used to write a colomn to one table. There is a simillar function to write data to one row. 

# Read from database

There is `ReadParameters` method which can be used to read some paramters from a table. You might write some constants and parameters to database and the read it in different applications. There is also a `ReadColomn` funcion which reads a coloumn of a spedified table. Plus there is `Data2Numpy` which is used for converting data to `numpy` format. 

# Other methods:

There are other methodes that are used for special reason - mainly EEG reason.
