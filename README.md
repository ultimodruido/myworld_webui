Maerklin MyWorld web UI
=================================

version number: 1.0

author: ultimodruido

Overview
--------

Web based simple UI to control all your [Maerklin MyWorld](https://www.maerklin.de/de/lp/2020/willkommen-bei-my-world) 
trains from your PC browser

Requirements
------------

A running [MyWorld remote](github.com/ultimodruido/myworld_remote) server is necessary.
Even if the _MyWorld remote_ server is running locally, an internet connection is required,
otherwise the fonts and icon will not be displayed properly. Probably in the future it won't 
be necessary anymore...

Under the hood
---------------
Some external libraries have been used:
 - The user interface is build with [Fomantic UI](https://fomantic-ui.com)
 - The logic behind the scene is written in Python thanks to [Brython](https://brython.info/index.html)
 - A self written Python library, Brymantic UI (not yet published) is used to create and manage UI elements from Brython


Usage
-----

Download the `html` folder locally and open `index.html` in a browser.

Configuration
-------------

The UI does not record or transmits private data over the network. 
The server _ip_ and _port_ are saved using the **HTML5 local store** protocol by the browser. 
The values are accessible only from webpages that share the same root.
For more information, refer to the 
[Mozilla Docs](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage?retiredLocale=it)
or
[W3 School](https://www.w3schools.com/html/html5_webstorage.asp).

Final notes
-----------

Possible bugs available, the software does not include tests yet.