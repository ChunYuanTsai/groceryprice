    # Grocery price finder
    #### Video Demo: https://youtu.be/1fME2-WozBE
    #### Description:

    ##### Overview of program functionality:
    This project is called the grocery price finder and it does just that -- find the price of grocery items (or, in general, product items). It does this by accepting user input via the command line interface and then searching it on the website of 2 grocery chains in Singapore, Fairprice and Cold Storage.

    Thr program by default searches both Fairprice and Cold Storage but also allow the user to specify if only one particular grocer should be searched. This is done by include the `-g` option argument.

    The program require the user to include the `-n` option argument for the number of search string entered and checks the length of positional argument (search strings)against the `-n` value. If they do not match, the system exits with a message that the number of products do not tally. To include spaces within the same search string, the user may use comma `,` as the delimiter e.g. `vitamin,c`.

    ##### Files:
    To prevent sending multiple requests to websites, and repeatedly downloading the webpage during debugging, I wrote a function to save the downloaded html into a txt  file, as well as another function to read these txt files. These are the `CShtml.txt` and `html.txt` files.

    `test_project.py` contain some basic unit tests.

    ##### Details and design considerations:
    The program may be categorised into 3 sections -- for getting input, processing it, and then generating the output. The geration of output is the straightforward part in this project and is done using the tabulate module which takes a tuple of tuple as input to ouput a table with 3 column - "Product", "Description" and "Price".

    For getting the input, this is done under the getinput() function. I used `argparse` so the program is more robust, such as being able to accept numerous search strings, allowing the user to specify the grocer to search for via option argument, specifying the choices allowed for the option argument,etc.getinput() returns two arguments - the list of products to search for, and the grocer to search from.

    The processing component is the most code-heavy part of the project. It can be further divided into (i) downloading the webpage from the right url (ii) parsing the downloaded html content and finding the html of interest and (iii) extracting the value of interest, which is the product title, description, and price. The Grocer class was created to contain the methods for doing the aforementioned processing tasks

    Originally I coded the program with just functions and lists but found some sections to be repetitive. I considered to improvise using dictionaries along the way. But finally, the decision was made to refactor my code to create a class called Grocer which will become the backbone of the program. This will make the program more robust and ease the process if more grocers were to be added into the picture (code).

    The main function in the program basically handles the logic on which grocer to search, and the search string based on the ouput returned from getinput() function. searchcs() and searchfp() are helper functions which, mainly through calling other functions, initialise the Grocer object, set the search url, download the webpage, parse and select relevant data from the html, and then finally outputting the table of price
