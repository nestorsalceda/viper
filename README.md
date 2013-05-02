#Viper Package Index

[![Build Status](https://travis-ci.org/nestorsalceda/viper.png)](https://travis-ci.org/nestorsalceda/viper)

Viper is a [Python Package Index](http://pypi.python.org) implementation.
Designed for being ran in your own network, behind your firewall.

##Features

* Upload non-public Python eggs
* Smart and transparent cache. Ask for packages to Viper, and it will cache them without
  blocking new requests.
* Blazing fast. Get faster results from your Continuous Integration. Deploy your
  product faster.
* Scale up replicating with MongoDB.
* Fault tolerance. Sincerely, I'm so tired of downtimes. Avoid work paralysis when
  third party infrastructure is down.

##How can I use it?

Deploy it. It's a simple [Tornado](http://www.tornadoweb.org) application.

And then, use http://yourhost/distutils

* `easy_install --index-url http://yourhost/distutils package`
* `pip install --index-url http://yourhost/distutils package`
* `python setup.py register ...`


##How it works?

When a package request comes to viper, it tries to serve by itself, but if it's
not cached, you will be redirected to official pypi (or mirrors if you
configured that setting).

Then next time, viper will server by itself the package requested.

##Demo

Try the [demo](http://viper-pypi.herokuapp.com) running in heroku infrastructure.

##Contribute

If you'd like to contribute, fork [repository](http://github.com/nestorsalceda/viper), and send a pull request.
