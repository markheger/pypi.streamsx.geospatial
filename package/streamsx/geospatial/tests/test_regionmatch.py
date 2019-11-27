import streamsx.geospatial as geo

from streamsx.topology.topology import Topology
from streamsx.topology.tester import Tester
from streamsx.topology.schema import CommonSchema, StreamSchema
import streamsx.spl.op as op
from streamsx.spl import toolkit
from streamsx.topology import context
import streamsx.rest as sr
import unittest
import datetime
import os
import json


def get_test_tk_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return script_dir+'/gen.test.data'

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print (str(self))
        self.geospatial_toolkit_home = os.environ["STREAMSX_GEOSPATIAL_TOOLKIT"]
        
    def _build_only(self, name, topo):
        result = context.submit("TOOLKIT", topo.graph) # creates tk* directory
        print(name + ' (TOOLKIT):' + str(result))
        assert(result.return_code == 0)
        result = context.submit("BUNDLE", topo.graph)  # creates sab file
        print(name + ' (BUNDLE):' + str(result))
        assert(result.return_code == 0)


    def test_with_spl_data_gen(self):
        print ('\n---------'+str(self))
        name = 'test_with_spl_data_gen'
        topo = Topology(name)
        toolkit.add_toolkit(topo, self.geospatial_toolkit_home)
        toolkit.add_toolkit(topo, get_test_tk_path())
        events_schema=StreamSchema('tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>')
        datagen = op.Invoke(topo, kind='test::GenData', schemas=['tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>','tuple<rstring id, rstring polygonAsWKT, boolean removeRegion, boolean notifyOnEntry, boolean notifyOnExit, boolean notifyOnHangout, int64 minimumDwellTime, int64 timeout>'])
        device_stream = datagen.outputs[0]
        region_stream = datagen.outputs[1]
        res = geo.region_match(stream=device_stream, region_stream=region_stream, schema=events_schema)
        res.print()

        if (("TestDistributed" in str(self)) or ("TestStreamingAnalytics" in str(self))):
            self._launch(topo)
        else:
            # build only
            self._build_only(name, topo)



class TestDistributed(Test):
    def setUp(self):
        # setup test config
        self.test_config = {}
        job_config = context.JobConfig(tracing='info')
        job_config.add(self.test_config)
        self.test_config[context.ConfigParams.SSL_VERIFY] = False  

    def _launch(self, topo):
        rc = context.submit('DISTRIBUTED', topo, self.test_config)
        print(str(rc))
        if rc is not None:
            if (rc.return_code == 0):
                rc.job.cancel()


class TestStreamingAnalytics(Test):
    def setUp(self):
        # setup test config
        self.test_config = {}
        job_config = context.JobConfig(tracing='info')
        job_config.add(self.test_config)

    def _launch(self, topo):
        rc = context.submit('STREAMING_ANALYTICS_SERVICE', topo, self.test_config)
        print(str(rc))
        if rc is not None:
            if (rc.return_code == 0):
                rc.job.cancel()

    @classmethod
    def setUpClass(self):
        # start streams service
        connection = sr.StreamingAnalyticsConnection()
        service = connection.get_streaming_analytics()
        result = service.start_instance()
        super().setUpClass()

