DotFilter: a simple filter to extract interested part of dot file
================================================================


- [Intro](#intro)
- [Installation](#installation)
- [User Guide](#user-guide)
- [Options](#options)
- [License](#license)



Intro
-----
DotFilter is a simple tool for filter out interested part of a complicated dot file. 

The input to DotFilter is an existed dot file;

The output from DotFilter is a **customized** dot file;

DotFilter allows you to do several kinds of customization:

- Indicate from which node to view
- Indicate to which node to view
- Indicate nodes with which attribute to view

Currently, it only supports customization for dot file exported by [systemd-analyze dot][]. 

Installation
------------

**Note: It is only tested on Ubuntu 12.04-lts now**

Firstly, make sure you have graphviz installed:

    sudo apt-get install graphviz

Secondly, copy script to any location where you have access right.

User Guide
-----------
###Get Input File
Run following command on **systemd-init** system to get input file:

    systemd-analyze dot > systemd.dot

###Convert dot to svg
Run following command to convert to human-readable picture:

    dot -Tsvg systemd.dot -o systemd.svg 

You can use `eog` to open this picture, but you will find it's quite complicated.

###Use SystemdViewr.py to extract intrested part of dot file
Run following command to extract interested part of dot file and output a customized version:

    ./SystemdFilter.py input

                     -o output 

                     [--from-node FROMNODE]

                     [--to-node TONODE]

                     [--output OUTPUT] 

                     [--filter [{conflicts,after,wants,requires,requisite} [{conflicts,after,wants,requires,requisite} ...]]]

E.g. `./SystemdFilter.py test/systemd.dot -o test/output.dot --from-node focussed.target --filter wants`

You could then get a dot file `test/output.dot` which contains only nodes started from `focussed.target` and only show information about `wants`.


###Convert customize dot to svg
Run following command to convert customized dot file to human-readable picture:

    dot -Tsvg systemd_customized.dot -o systemd_customized.svg

You can use `eog` to open this picture. This time you can get clearer picture.

Options
-------

    --from-node NODENAME        Indicate DotFilter from which node to construct. Could be combined with  --to-node  .

    --to-node NODENAME          Indicate DotFilter to which node to construct. Could be combined with  --from-node  .

    --output FILENAME           Indicate output file name. Output _./output.dot_ by default.

    --filter ATTR_LIST          A list of space separated interested attributes to extract.


License
-------

This software is licensed under the [GPL v3 license][gpl].


[systemd-analyze dot]: http://www.freedesktop.org/software/systemd/man/systemd-analyze.html
[gpl]: http://www.gnu.org/copyleft/gpl.html
