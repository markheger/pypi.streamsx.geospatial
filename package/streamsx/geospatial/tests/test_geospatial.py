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
from subprocess import call, Popen, PIPE
from streamsx.geospatial.schema import RegionMatchSchema, FlighPathEncounterSchema


def _get_test_tk_path():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return script_dir+'/gen.test.data'

def _run_shell_command_line(command):
    process = Popen(command, universal_newlines=True, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def _streams_install_env_var():
    result = True
    try:
        os.environ['STREAMS_INSTALL']
    except KeyError: 
        result = False
    return result

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

    def _index_toolkit(self, tk):
        if _streams_install_env_var():
            cmd = os.environ['STREAMS_INSTALL']+'/bin/spl-make-toolkit -i .'
            _run_shell_command_line('cd '+tk+'; '+cmd)


    def test_region_match(self):
        print ('\n---------'+str(self))
        name = 'test_region_match'
        topo = Topology(name)
        toolkit.add_toolkit(topo, self.geospatial_toolkit_home)
        self._index_toolkit(_get_test_tk_path())
        toolkit.add_toolkit(topo, _get_test_tk_path())
        datagen = op.Invoke(topo, kind='test::GenRegionData', schemas=[RegionMatchSchema.Devices,RegionMatchSchema.Regions])
        device_stream = datagen.outputs[0]
        region_stream = datagen.outputs[1]
        res = geo.region_match(stream=device_stream, region_stream=region_stream)
        res.print()

        if (("TestDistributed" in str(self)) or ("TestStreamingAnalytics" in str(self))):
            tester = Tester(topo)
            tester.tuple_count(res, 4, exact=True)
            tester.test(self.test_ctxtype, self.test_config, always_collect_logs=True)
        else:
            # build only
            self._build_only(name, topo)


    def test_flight_path_encounter(self):
        print ('\n---------'+str(self))
        name = 'test_flight_path_encounter'
        topo = Topology(name)
        toolkit.add_toolkit(topo, self.geospatial_toolkit_home)
        self._index_toolkit(_get_test_tk_path())
        toolkit.add_toolkit(topo, _get_test_tk_path())
        
        datagen = op.Invoke(topo, kind='test::GenFlightPathData', schemas=[FlighPathEncounterSchema.EncounterEvents])
        planes_stream = datagen.outputs[0]
        
        events = planes_stream.map(geo.FlightPathEncounter(north_latitude=52.6,south_latitude=52.4,west_longitude=13.3,east_longitude=13.5,num_latitude_divs=5,num_longitude_divs=5,search_radius=10000,altitude_search_radius=400,time_search_interval=600000), schema=FlighPathEncounterSchema.EncounterEvents)
        
        dump = op.Invoke(topo, inputs=[events], kind='test::DumpData', schemas=CommonSchema.String)
        res = dump.outputs[0]
        res.print()

        if (("TestDistributed" in str(self)) or ("TestStreamingAnalytics" in str(self))):
            tester = Tester(topo)
            tester.tuple_count(res, 1, exact=True)
            tester.test(self.test_ctxtype, self.test_config, always_collect_logs=True)
        else:
            # build only
            self._build_only(name, topo)


class TestDistributed(Test):
    def setUp(self):
        Tester.setup_distributed(self)
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
        #self.test_config = {}
        #job_config = context.JobConfig(tracing='info')
        #job_config.add(self.test_config)
        Tester.setup_streaming_analytics(self, force_remote_build=False)

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

