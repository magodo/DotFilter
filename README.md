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

Currently supported dot file origins are from:

* [bitbake dot][]
* [systemd-analyze dot][]

Each one has a correspoding laucher script under **bin** directory.

The input to script is an existed **raw** dot file;

The output is a **filtered** dot file;

DotFilter allows you to do several kinds of customization:

- Indicate from which node to view(regexp supported)
- Indicate to which node to view(regexp supported)
- Indicate nodes with which attribute to view

Installation
------------

**Note: It is only tested on Ubuntu 12.04-lts now**

Firstly, make sure you have graphviz installed:

    sudo apt-get install graphviz

Secondly, copy script to any location where you have access right.

User Guide - bitbake
-----------

###Get Input File
Run following command in devkits to get input file:

    bitbake -g <target-name>

###Extract intrested part of dot file
Run following command to extract interested part of dot file and output a customized version:

    usage: bitbake_filter.py           [-h] [--from-node FROMNODE]
                                       [--to-node TONODE]
                                       [--filter [{rdepends,depends} [{rdepends,depends} ...]]]
                                       [--output OUTPUT]
                                       input

    positional arguments:
      input

    optional arguments:
      -h, --help            show this help message and exit
      --from-node FROMNODE  From which node to extract(regexp supported)
      --to-node TONODE      To which node to extract(regexp supported)
      --filter [{rdepends,depends} [{rdepends,depends} ...]]
                            Which kind of transitions do you want to view
      --output OUTPUT, -o OUTPUT
                            Output filtered dot file

E.g. `./bitbake_filter.py --from-node ".*conn-connectivity.*app.*" --to-node ".*.hmi.*" --filter depends rdepends --output ../test/pn-depends_output.dot ../test/pn-depends.dot`

You could then get a dot file `../test/pn-depends_output.dot` which contains only nodes started from nodes match pattern `.*conn-connectivity.*app.*` and to nodes match pattern `.*.hmi.*` and only show information about `depends` and `rdepends`.

###Convert customize dot to svg
Run following command to convert customized dot file to human-readable picture:

    dot -Tsvg <input dot file> > -o <output dot file>

You can use `eog` to open this picture. This time you can get clearer picture.

User Guide - systemd
-----------

###Get Input File
Run following command on **systemd-init** system to get input file:

    systemd-analyze dot > systemd.dot

###Convert dot to svg
Run following command to convert to human-readable picture:

    dot -Tsvg systemd.dot -o systemd.svg 

You can use `eog` to open this picture, but you will find it's quite complicated.

###Extract intrested part of dot file
Run following command to extract interested part of dot file and output a customized version:

    usage: systemd_filter.py [-h] [--from-node FROMNODE] [--to-node TONODE]
                             [--filter [{conflicts,after,wants,requires,requisite} [{conflicts,after,wants,requires,requisite} ...]]]
                             [--output OUTPUT]
                             input

    positional arguments:
      input

    optional arguments:
      -h, --help            show this help message and exit
      --from-node FROMNODE  From which node to extract(regexp supported)
      --to-node TONODE      To which node to extract(regexp supported)
      --filter [{conflicts,after,wants,requires,requisite} [{conflicts,after,wants,requires,requisite} ...]]
                            Which kind of transitions do you want to view
      --output OUTPUT, -o OUTPUT
                            Output filtered dot file

E.g. `./systemd_filter.py --from-node "lazy.target" --filter wants requires --output ../test/systemd_out.dot ../test/systemd.dot`

You could then get a dot file `../test/systemd_out.dot` which contains only nodes started from `lazy.target` and only show information about `wants` and `requires`.

###Convert customize dot to svg
Run following command to convert customized dot file to human-readable picture:

    dot -Tsvg <input dot file> > -o <output dot file>

You can use `eog` to open this picture. This time you can get clearer picture.

License
-------

This software is licensed under the [GPL v3 license][gpl].


[bitbake dot]: http://www.yoctoproject.org/docs/2.0.1/ref-manual/ref-manual.html#usingpoky-debugging-dependencies
[systemd-analyze dot]: http://www.freedesktop.org/software/systemd/man/systemd-analyze.html
[gpl]: http://www.gnu.org/copyleft/gpl.html
