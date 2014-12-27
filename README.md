Kepler K2 Variables Catalogue
=============================

The site is hosted [here](http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat). This readme documents the construction. Please see this [arxiv](http://arxiv.org/abs/1411.6830) release for more detail on the catalogue itself.

Site
----

The site is static html rendered by [Frozen-Flask](http://pythonhosted.org/Frozen-Flask/) into the `build` directory. This name is configurable at the command line.

Each image is embedded in the page directly for simplicity.

Deployment
----------

To deploy the site, run `fab -H <dest> deploy`, which sshs into the machine `<dest>`, renders the code and copies the built directory to `~/www`.

Note this encodes some hidden variables such as the location of the repository on `<dest>`, and the destination of where the code should be put. In a better version of the script I will add command line arguments and turn it into a proper script.

The `master` branch of this repository shall be the deployable branch therefore anything in master is deemed "production ready".

Authors
-------

* Catalogue construction: David Armstrong
* Online site: [Simon Walker](https://github.com/mindriot101)
