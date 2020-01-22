# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import os
import streamsx.spl.op as op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring
import datetime
import json
from streamsx.geospatial.schema import Schema
import streamsx.topology.composite

def _add_toolkit_dependency(topo):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, 'com.ibm.streams.geospatial', '[3.4.0,4.0.0)')


class FlightPathEncounter(streamsx.topology.composite.Map):
    """
    Composite map transformation for FlightPathEncounter

    .. versionadded:: 1.1

    Attributes
    ----------
    north_latitude : float64
        The latitude of the north border of the bounding box for the spatial index used by the Encounter detector. Given in degrees. Must be between -90 (south pole) and 90 (north pole).
    south_latitude : float64
        The latitude of the south border of the bounding box for the spatial index used by the Encounter detector. Given in degrees. Must be between -90 (south pole) and 90 (north pole). 
    west_longitude : float64
        The longitude of the west border of the bounding box for the spatial index used by the Encounter detector. Given in degrees. Must be between 0 (greenwich median) and 360.
    east_longitude : float64
        The longitude of the east border of the bounding box for the spatial index used by the Encounter detector. Given in degrees. Must be between 0 (greenwich median) and 360.
    num_latitude_divs : int32
        Number of latitude divisions (rows) for the spatial index used by the Encounter detector. Must be greater than one.
    num_longitude_divs : int32
        Number of longitude divisions (columns) for the spatial index used by the Encounter detector. Must be greater than one.
    altitude_search_radius : int32
        The altitiude distance around the flying objects path, searched for collosions with other objects. Given in meters.
    search_radius : int32
        The radius around the flying objects path, searched for other objects for potential collisions. Given in meters.
    time_search_interval : int32
        The time interval the flight path is extrapolated and searched for collisions with other objects. Given in milliseconds. Must be greater than one second. 
    """


    def __init__(self, north_latitude, south_latitude, west_longitude, east_longitude, num_latitude_divs, num_longitude_divs, altitude_search_radius, search_radius, time_search_interval):

        self.north_latitude = north_latitude
        self.south_latitude = south_latitude
        self.west_longitude = west_longitude
        self.east_longitude = east_longitude
        self.num_latitude_divs = num_latitude_divs
        self.num_longitude_divs = num_longitude_divs
        self.altitude_search_radius = altitude_search_radius
        self.search_radius = search_radius
        self.time_search_interval = time_search_interval

        self.vm_arg = None
        self.cleanup_interval=None
        self.encounter_attribute=None
        self.encounter_distance_attribute=None
        self.encounter_time_attribute=None
        self.filter_by_bounding_box=None
        self.observation_attribute=None

        
    @property
    def vm_arg(self):
        """
            str: Arbitrary JVM arguments can be passed to the Streams operator
        """
        return self._vm_arg

    @vm_arg.setter
    def vm_arg(self, value):
        self._vm_arg = value
        

    @property
    def cleanup_interval(self):
        """
            int: The flying objects are periodically cleaned up from the internal data tables. During cleanup objects are removed whose last observation is older than the current observation minus the 'cleanupInterval'. If not specified the interval defaults to 3 times the value of the 'timeSearchInterval' parameter. Given in milliseconds. The cleanup is not performed on each incoming tuple, instead it is performed when the timestamp of the incoming observation is newer than the timesatmp of the last cleanup plus a third of the 'cleanupInterval' parameter. For example if the 'cleanupInterval' is set to 15 minutes (900000 milliseconds), the operation is invoked roughly every 5 minutes. 
        """
        return self._cleanup_interval

    @cleanup_interval.setter
    def cleanup_interval(self, value):
        self._cleanup_interval = value
        

    @property
    def encounter_attribute(self):
        """
            str: he name of an output attribute of type TUPLE that will contains the data for a detected encounter. The Tuple must be of type com.ibm.streams.geospatial.FlightPathEncounterTypes.Observation3D
        """
        return self._encounter_attribute

    @encounter_attribute.setter
    def encounter_attribute(self, value):
        self._encounter_attribute = value
        

    @property
    def encounter_distance_attribute(self):
        """
            str: The name of an output attribute that will hold the closest lat/lon distance in meters between the objects this encounter was detected for. 
        """
        return self._encounter_distance_attribute

    @encounter_distance_attribute.setter
    def encounter_distance_attribute(self, value):
        self._encounter_distance_attribute = value

        
    @property
    def encounter_time_attribute(self):
        """
            str: The name of an output attribute that will hold the time in milliseconds relative to the timestamp of the observation for this encounter. 
        """
        return self._encounter_time_attribute

    @encounter_time_attribute.setter
    def encounter_time_attribute(self, value):
        self._encounter_time_attribute = value


    @property
    def filter_by_bounding_box(self):
        """
            bool: Set this parameter to ```True`` if observations whith locations outside the bounding box of the detectors spatial index shall be ignored. The bounding box of the detector is specified by the southLatitude,northLatitude,westLongitude and eastLongitude parameters. The default is ``False`` so all observations are processed. Note that processing observations outside of the box may decrease the spatial index performance. 
        """
        return self._filter_by_bounding_box

    @filter_by_bounding_box.setter
    def filter_by_bounding_box(self, value):
        self._filter_by_bounding_box = value

    @property
    def observation_attribute(self):
        """
            str: The name of an input attribute of type TUPLE that contains the data for the observation to process.The Tuple must be of type com.ibm.streams.geospatial.FlightPathEncounterTypes.Observation3D
        """
        return self._observation_attribute

    @observation_attribute.setter
    def observation_attribute(self, value):
        self._observation_attribute = value


    def populate(self, topology, stream, schema, name, **options):

        _op = _FlightPathEncounter(stream=stream, schema=schema, vmArg=self.vm_arg, name=name)
        _op.params['altitudeSearchRadius'] = streamsx.spl.types.int32(self.altitude_search_radius)
        _op.params['eastLongitude'] = streamsx.spl.types.float64(self.east_longitude)
        _op.params['northLatitude'] = streamsx.spl.types.float64(self.north_latitude)
        _op.params['numLatitudeDivs'] = streamsx.spl.types.int32(self.num_latitude_divs)
        _op.params['numLongitudeDivs'] = streamsx.spl.types.int32(self.num_longitude_divs)
        _op.params['searchRadius'] = streamsx.spl.types.int32(self.search_radius)
        _op.params['southLatitude'] = streamsx.spl.types.float64(self.south_latitude)
        _op.params['timeSearchInterval'] = streamsx.spl.types.int32(self.time_search_interval)
        _op.params['westLongitude'] = streamsx.spl.types.float64(self.west_longitude)
        # optional parameters
        if self.cleanup_interval is not None:
            _op.params['cleanupInterval'] = streamsx.spl.types.int32(self.cleanup_interval)
        if self.encounter_attribute is not None:
            _op.params['encounterAttribute'] = self.encounter_attribute
        if self.encounter_distance_attribute is not None:
            _op.params['encounterDistanceAttribute'] = self.encounter_distance_attribute
        if self.encounter_time_attribute is not None:
            _op.params['encounterTimeAttribute'] = self.encounter_time_attribute
        if self.filter_by_bounding_box is not None:
            if self.filter_by_bounding_box is True:
                _op.params['filterByBoundingBox'] = _op.expression('true')
        if self.observation_attribute is not None:
            _op.params['observationAttribute'] = _op.attribute(stream, self.observation_attribute)

        return _op.outputs[0]


def region_match(stream, region_stream, schema=Schema.Events, event_type_attribute=None, region_name_attribute=None, id_attribute=None, latitude_attribute=None, longitude_attribute=None, timestamp_attribute=None, name=None):
    """Uses the RegionMatch operator to compare device data with configured regions.

    Stores geographical regions (also called Geofences) together with a set of attributes per region. On the input stream it receives observations from moving devices and matches the device location against the stored regions. As a result it emits events if the device enters, leaves or is hanging out in a region. The regions can be added or removed via the region_stream. The events are send to output stream. 

    Args:
        stream(Stream): Stream of tuples containing device data of schema :py:const:`streamsx.geospatial.schema.Schema.Devices`, which is matched against all configured regions, to detect events.
        region_stream(Stream): Stream of tuples containing regions of schema :py:const:`streamsx.geospatial.schema.Schema.Regions`
        schema(Schema): Output streams schema, default schema is :py:const:`streamsx.geospatial.schema.Schema.Events`
        event_type_attribute(str): Specify the name of an ouput Stream attribute of type 'rstring', that will receive the event type (ENTER,EXIT,HANGOUT) if a match is detected. If not specified the default attribute name is 'matchEventType'. 
        region_name_attribute(str): Specifies the name of an ouput Stream attribute of type 'rstring', that will receive the name of the region if a match is detected. If not specified the default attribute name is 'regionName'. 
        id_attribute(str): Specify the name of an attribute of type 'rstring' in the region_stream, that holds the unique identifier of the device. If not specified the default attribute name is 'id'. 
        latitude_attribute(str): Specify the name of an attribute of type 'float64' in the region_stream, that holds the latitude of the device. If not specified the default attribute name is 'latitude'. 
        longitude_attribute(str): Specify the name of an attribute of type 'float64' in the region_stream, that holds the longitude of the device. If not specified the default attribute name is 'longitude'. 
        timestamp_attribute(str): Specify the name of an attribute of type 'timestamp' in the region_stream, that holds the timestamp of the device measurement. If not specified the default attribute name is 'timeStamp'. 
        name(str): Operator name in the Streams context, defaults to a generated name.

    Returns:
        Output Stream with specified schema
    """
    # python wrapper geospatial toolkit dependency
    _add_toolkit_dependency(stream.topology)

    _op = _RegionMatch(stream=stream, schema=schema, region_stream=region_stream, eventTypeAttribute=event_type_attribute, idAttribute=id_attribute, latitudeAttribute=latitude_attribute, longitudeAttribute=longitude_attribute, regionNameAttribute=region_name_attribute, timestampAttribute=timestamp_attribute, name=name)

    return _op.outputs[0]

class _RegionMatch(op.Invoke):
    def __init__(self, stream, schema, region_stream, eventTypeAttribute=None, idAttribute=None, latitudeAttribute=None, longitudeAttribute=None, regionNameAttribute=None, timestampAttribute=None, name=None):
        topology = stream.topology
        kind="com.ibm.streams.geospatial::RegionMatch"        
        inputs=[stream,region_stream]
        schemas=schema
        params = dict()

        if eventTypeAttribute is not None:
            params['eventTypeAttribute'] = eventTypeAttribute
        if idAttribute is not None:
            params['idAttribute'] = idAttribute
        if latitudeAttribute is not None:
            params['latitudeAttribute'] = latitudeAttribute
        if longitudeAttribute is not None:
            params['longitudeAttribute'] = longitudeAttribute
        if regionNameAttribute is not None:
            params['regionNameAttribute'] = regionNameAttribute
        if timestampAttribute is not None:
            params['timestampAttribute'] = timestampAttribute
 
        super(_RegionMatch, self).__init__(topology,kind,inputs,schema,params,name)


class _FlightPathEncounter(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema=None, altitudeSearchRadius=None, eastLongitude=None, northLatitude=None, numLatitudeDivs=None, numLongitudeDivs=None, searchRadius=None, southLatitude=None, timeSearchInterval=None, westLongitude=None, cleanupInterval=None, encounterAttribute=None, encounterDistanceAttribute=None, encounterTimeAttribute=None, filterByBoundingBox=None, observationAttribute=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streams.geospatial::FlightPathEncounter"
        inputs=stream
        schemas=schema
        params = dict()

        if vmArg is not None:
            params['vmArg'] = vmArg
        if altitudeSearchRadius is not None:
            params['altitudeSearchRadius'] = altitudeSearchRadius
        if eastLongitude is not None:
            params['eastLongitude'] = eastLongitude
        if northLatitude is not None:
            params['northLatitude'] = northLatitude
        if numLatitudeDivs is not None:
            params['numLatitudeDivs'] = numLatitudeDivs
        if numLongitudeDivs is not None:
            params['numLongitudeDivs'] = numLongitudeDivs
        if searchRadius is not None:
            params['searchRadius'] = searchRadius
        if southLatitude is not None:
            params['southLatitude'] = southLatitude
        if timeSearchInterval is not None:
            params['timeSearchInterval'] = timeSearchInterval
        if westLongitude is not None:
            params['westLongitude'] = westLongitude
        if cleanupInterval is not None:
            params['cleanupInterval'] = cleanupInterval
        if encounterAttribute is not None:
            params['encounterAttribute'] = encounterAttribute
        if encounterDistanceAttribute is not None:
            params['encounterDistanceAttribute'] = encounterDistanceAttribute
        if encounterTimeAttribute is not None:
            params['encounterTimeAttribute'] = encounterTimeAttribute
        if filterByBoundingBox is not None:
            params['filterByBoundingBox'] = filterByBoundingBox
        if observationAttribute is not None:
            params['observationAttribute'] = observationAttribute

        super(_FlightPathEncounter, self).__init__(topology,kind,inputs,schema,params,name)

