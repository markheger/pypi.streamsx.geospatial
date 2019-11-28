# Python streamsx.geospatial package

This exposes SPL operators in the `com.ibm.streamsx.geospatial` toolkit as Python methods.

Package is organized using standard packaging to upload to PyPi.

The package is uploaded to PyPi in the standard way:
```
cd package
python setup.py sdist bdist_wheel upload -r pypi
```
Note: This is done using the `ibmstreams` account at pypi.org and requires `.pypirc` file containing the credentials in your home directory.

Package details: https://pypi.python.org/pypi/streamsx.geospatial

Documentation is using Sphinx and can be built locally using:
```
cd package/docs
make html
```

or

    ant doc

and viewed using
```
firefox package/docs/build/html/index.html
```

The documentation is also setup at `readthedocs.io`.

Documentation links:
* http://streamsxgeospatial.readthedocs.io

## Version update

To change the version information of the Python package, edit following files:

- ./package/docs/source/conf.py
- ./package/streamsx/geospatial/\_\_init\_\_.py

When the development status changes, edit the *classifiers* in

- ./package/setup.py

When the documented sample must be changed, change it here:

- ./package/streamsx/geospatial/\_\_init\_\_.py
- ./package/DESC.txt

## Environment

You need the streamsx package in version 1.13.15 to use and test the streamsx.geospatial package. Install it like this:

    pip install streamsx==1.13.15

In addition you should unset the PYTHONPATH variable to not use the streams package included in your local Streams installation:

    unset PYTHONPATH
    
## Test

When using local build (e.g. not forcing remote build), then you need to specifiy the toolkit location, for example:

    export STREAMSX_GEOSPATIAL_TOOLKIT=<PATH_TO_GEOSPATIAL_TOOLKIT>/com.ibm.streamsx.geospatial


### Build only test

Run the test with:

    ant test-build-only


```
cd package
python3 -u -m unittest streamsx.geospatial.tests.test_regionmatch.Test
```


### Distributed test

Make sure that the streams environment is set and the environment variables:
STREAMS_INSTALL, STREAMS_DOMAIN_ID, and STREAMS_INSTANCE_ID are setup.

Run the test with:

    ant test

or

```
cd package
python3 -u -m unittest streamsx.geospatial.tests.test_regionmatch.TestDistributed
```



### Streaming Analytics service

Package can be tested with TopologyTester using the [Streaming Analytics](https://www.ibm.com/cloud/streaming-analytics) service.

Run the test with:

    ant test-sas

or

```
cd package
python3 -u -m unittest streamsx.geospatial.tests.test_regionmatch.TestStreamingAnalytics
```

