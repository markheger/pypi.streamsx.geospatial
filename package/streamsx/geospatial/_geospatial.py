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

def _add_toolkit_dependency(topo):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, 'com.ibm.streams.geospatial', '[3.4.0,4.0.0)')

def region_match(stream, region_stream, schema, event_type_attribute=None, region_name_attribute=None, id_attribute=None, latitude_attribute=None, longitude_attribute=None, timestamp_attribute=None, name=None):
    """Uses the RegionMatch operator to compare device data with configured regions.

    Stores geographical regions (also called Geofences) together with a set of attributes per region. On the input stream it receives observations from moving devices and matches the device location against the stored regions. As a result it emits events if the device enters, leaves or is hanging out in a region. The regions can be added or removed via the region_stream. The events are send to output stream. 

    Args:
        stream(Stream): Stream of tuples containing device data, which is matched against all configured regions, to detect events.
        region_stream(Stream): Stream of tuples containing regions.
        schema(Schema): Output streams schema
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

