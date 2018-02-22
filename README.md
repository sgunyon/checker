# checker

python script to parse and evaluate history files

---
### usage

main.py takes one argument, the history file.

`python main.py [FILE]`

### features

- stores and updates cluster state (nodes and live nodes)
- checks consistency levels of read and write operations
- validates logging of write operations
- validates data consistency of read operations

### implementation

my approach was to separate this task into two parts:

- parse the history files in to a python data type
- process and evaluate the data

i created both objects outside of the loop to hold state, in this case the write list and node counts. while this wasn't necessary for the Parser object, it made organizational sense to create both objects in the same place.

inside the loop, the parse_data method parses the history file and returns a dictionary. regex seemed the most expedient way to parse the data in the history files. it also provided a convenient way to filter out noise. after parsing, the resulting dictionary is passed to the consistency method.

each module-specific method inside of the Consistency class contains logic for evaluating the data. the consistency method acts as a dispatch to route the input, call module-specific methods, and return an output that is later printed. i strongly considered calling the consistency method 'route-put', as it both routes data to other methods, and outputs the final evaluation.

### output

it is ugly. while processing each module's output from the history file, the consistency method populates an output dictionary. this dictionary is crudely printed to console. quick and dirty and dirty.

### strengths and weaknesses

strengths

- fairly intuitive
- names reflect functionality (idiomatic)
- runs in python2 and python3 (output format may vary)

weaknesses

- relies on a rigid history file template
- output is, as previously referenced, ugly
- lacks exception handling

### feedback

i estimate that i spent 20-30 total hours working on this. probably 15 of those actually creating and confirming things worked and another 10-15 reimplementing things so they made more sense, or looked less messy, or were less embarrassing.

i'm new enough to programming that i knew what i wanted to do, but had to look up ways to do it. that is my general experience with most of my programming projects.

i found myself rereading the gist for things i'd missed or overlooked. one example of that is the type operation documentation. toward the end it states that only the write module makes changes on fail. when initially creating the logic for read validation, i was only checking reads writes that succeeded. it wasn't until a at least my third read-through that i decided i needed to log all write attempts for read validation. at some point i considered only logging write attempts that happened when > 0 live nodes were available. i ended up just checking each read against every attempted write, which my have been too loose an interpretation. this my be a reflection of my reading comprehension, or how late in the evening i worked on this :)

overall i learned a lot doing this exercise. it was good practice for using classes to manage state, which i'm getting better at. it also provided an opportunity to work with regular expressions, which i rarely do.
