# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019
"""
Schemas for streams the :py:meth:`~streamsx.geospatial.region_match` method.
"""

from streamsx.topology.schema import StreamSchema
#
# Defines Message types with default attribute names and types.
_SPL_SCHEMA_EVENTS = 'tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>'
_SPL_SCHEMA_DEVICES = 'tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>'
_SPL_SCHEMA_REGIONS = 'tuple<rstring id, rstring polygonAsWKT, boolean removeRegion, boolean notifyOnEntry, boolean notifyOnExit, boolean notifyOnHangout, int64 minimumDwellTime, int64 timeout>'



class Schema:
    """
    Structured stream schemas for :py:meth:`~streamsx.geospatial.region_match`.
    
    The schema :py:const:`Events` is the default schema for the output stream.
    
    The schemas
    
    * :py:const:`Devices`
    * :py:const:`Regions`
    
    are schemas for the input streams.
    
    All schemas defined in this class are instances of `streamsx.topology.schema.StreamSchema`.
    
    """


    Devices = StreamSchema (_SPL_SCHEMA_DEVICES)
    """
    This schema can be used as input for :py:meth:`~streamsx.geospatial.region_match`.
    
    The schema defines following attributes
    
    * id(str) - the device id
    * latitude(float64) - the latitude of the device
    * longitude(float64) - the longitude value of the device
    * timeStamp(timestamp) - the timestamp
    * matchEventType(str) - the match event type
    * regionName(str) - the region name

    """

    Regions = StreamSchema (_SPL_SCHEMA_REGIONS)
    """
    This schema can be used for :py:meth:`~streamsx.geospatial.region_match` to configure a region.
    
    The schema defines following attributes
    
    * id(str) - The unique identifier of the region.
    * polygonAsWKT(str) - The geometry of the region as WKT string. For example: ``POLYGON((13.413140166512107 52.53577235025506,13.468071807137107 52.53577235025506,13.468071807137107 52.51279486997035,13.413140166512107 52.51279486997035,13.413140166512107 52.53577235025506))``
    * removeRegion(bool) - A flag indicating if the region shall be removed. If false the region will be added. If true it will be removed. On removal only the regionId field is needed.
    * notifyOnEntry(bool) - A flag indicating if an ENTRY event shall be generated when a device enters the region.
    * notifyOnExit(bool) - A flag indicating if an EXIT event shall be generated when a device leaves the region.
    * notifyOnHangout(bool) - A flag indicating if a HANGOUT event shall be generated when a device stays in the region for some time.
    * minimumDwellTime(int64)- The minimum time in seconds a device has to be observed in a certain region, before a 'Hangout' event is reported.
    * timeout(int64) - Device timeout in seconds. In case a device was last observed more than timeout seconds ago, the device is treated as stale and is removed before the new observation is processed. If this value is zero, no timeout handling is performed.
    
    """

    Events = StreamSchema (_SPL_SCHEMA_EVENTS)
    """
    This schema can be used as output for :py:meth:`~streamsx.geospatial.region_match`.
    
    The schema defines following attributes
    
    * id(str) - the device id
    * latitude(float64) - the latitude of the device
    * longitude(float64) - the longitude value of the device
    * timeStamp(timestamp) - the timestamp
    * matchEventType(str) - the match event type
    * regionName(str) - the region name

    """

    pass
