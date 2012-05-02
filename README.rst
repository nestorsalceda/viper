.. image:: https://secure.travis-ci.org/nestorsalceda/viper.png

Viper Package Index
===================

Viper is a `Python Package Index <http://pypi.python.org>`_ implementation.

What makes Viper different?
---------------------------

Viper is designed for running behind a firewall, in your own network.  This
allows you to share non-public packages with other members in your team.

Viper is designed to be blazing fast.  Running behind your firewall, you can
install it near to your Continuous Integration (or Continuous Delivery) server
and feel how you get feedback faster.  And as it has replication support using
MongoDB, you can have your own mirrors in minutes.

I'm still cooking a cache for keeping packages you use more, but I'm pretty
sure I will finish it soon.  This means fault tolerance (sometimes PyPI or
other services are down) and of course faster downloads.

And finally simplicity.  Viper should be easy to deploy, and easy to configure
(also in the client), you should start using it:

::

$ easy_install --index-url http://yourhost/distutils package

If the package doesn't exist in the index, it redirects automatically to PyPI
(or other mirrors).
