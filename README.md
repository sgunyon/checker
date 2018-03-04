# checker

python script to parse and evaluate history files

---
### usage

main.py takes one argument, the history file.

`python main.py [FILE]`

### features

- stores and updates cluster state (nodes and live nodes)
- checks consistency of read and write operations
- validates logging of write operations
- validates data consistency of read operations

### implementation

my approach was to separate this task into two parts:

- parse the history files in to a python data type
- process and evaluate the data

i created both objects outside of the loop to hold state, in this case the write list and node counts. while this wasn't necessary for the Parser object, it made organizational sense to create both objects in the same place.

inside the loop, the parse_data method parses the history file and returns a dictionary. regex seemed the most expedient way to parse the data in the history files. it also provided a convenient way to filter out noise. after parsing, the resulting dictionary is passed to the consistency method.

each module-specific method inside of the Consistency class contains logic for evaluating the data. the consistency method acts as a dispatch to route input, call module-specific methods, and print the output. i strongly considered calling the consistency method 'route_put', as it both routes data to other methods, and outputs the final evaluation.

### output

it is ugly. while processing each module's output from the history file, the consistency method populates an output dictionary. i made this an ordered dictionary for my own sanity while testing. this dictionary is crudely printed to console. here is a list of possible keys in the output dictionary:

###### all modules
- <b>time:</b> included for organization and readability
- <b>module:</b> included to track what data should be presented

###### topology/live_node modules
- <b>cluster_state:</b> only presents for topology modules - logs node count (current, new)
- <b>live_nodes:</b> presents for both topology and live_node modules - reflects live nodes available, going forward
- <b>report:</b> presents only on topology or live_node modules that fail (operation failed)

###### read/write modules
- <b>consistency:</b> presents on all reads and writes - compares consistency level requested with cluster state (succeeded/failed)
- <b>data validation:</b> presents only on successful reads - confirms whether or not a read had previous been written (valid/invalid)
- <b>log validation:</b> presents on all writes and successful reads - confirms whether a read or write, failing it's consistency level check, logs a failure (valid/invalid)


### strengths and weaknesses

strengths

- fairly intuitive
- names reflect functionality
- runs in python2 and python3

weaknesses

- relies on a rigid history file template
- output is, as previously referenced, ugly
- lacks exception handling

### feedback

i estimate that i spent 20-30 total hours working on this. probably 15 of those actually creating and confirming things worked and another 10-15 reimplementing things so they made more sense, or looked less messy, or were less embarrassing.

i'm fairly new to programming so while basically what i wanted to do, i still had to look up ways to do it. that is my general experience with most of my programming projects.

i found myself rereading the gist for things i'd missed or overlooked. one example of that is the type operation documentation. toward the end it states that only the write module (may) make changes on fail. when initially creating the logic for read validation, i was only checking against writes that succeeded. it wasn't until a at least my third read through that i decided i needed to log all write attempts for read validation. at some point i considered only logging write attempts that happened when > 0 live nodes were available. i ended up just checking each read against every attempted write, which might have been too loose an interpretation. this may be more a reflection of my reading comprehension than anything programming related, or possibly how late in the evening i worked on this :)

overall i learned a lot doing this exercise. it was good practice for using classes to manage state, which i think i'm getting better at. it also provided an opportunity to work with regular expressions, which was pretty fun.
