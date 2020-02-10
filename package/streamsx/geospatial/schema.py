# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019, 2020


from streamsx.topology.schema import StreamSchema
#
# Defines Message types with default attribute names and types.
_SPL_SCHEMA_EVENTS = 'tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>'
_SPL_SCHEMA_DEVICES = 'tuple<rstring id, float64 latitude, float64 longitude, timestamp timeStamp, rstring matchEventType, rstring regionName>'
_SPL_SCHEMA_REGIONS = 'com.ibm.streams.geospatial::RegionMatchTypes.RegionInfo'

_SPL_SCHEMA_FLIGHTPATH_ENCOUNTER_EVENT = 'com.ibm.streams.geospatial::FlightPathEncounterTypes.EncounterEvent'
_SPL_SCHEMA_FLIGHTPATH_OBSERVATION3D = 'com.ibm.streams.geospatial::FlightPathEncounterTypes.Observation3D'

class RegionMatchSchema:
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

    EncounterEvents = StreamSchema (_SPL_SCHEMA_FLIGHTPATH_ENCOUNTER_EVENT)
    """
    This schema can be used as output for :py:meth:`~streamsx.geospatial.FlightPathEncounter`.
    
    The schema defines following attributes
    
    * id(str) - the device id
    * latitude(float64) - the latitude of the device
    * longitude(float64) - the longitude value of the device
    * timeStamp(timestamp) - the timestamp
    * matchEventType(str) - the match event type
    * regionName(str) - the region name

    """

    Observation3D = StreamSchema (_SPL_SCHEMA_FLIGHTPATH_OBSERVATION3D)
    """
    This schema can be used as output for :py:meth:`~streamsx.geospatial.FlightPathEncounter`.
    
    The schema defines following attributes
    
    * id(str) - the device id
    * latitude(float64) - the latitude of the device
    * longitude(float64) - the longitude value of the device
    * timeStamp(timestamp) - the timestamp
    * matchEventType(str) - the match event type
    * regionName(str) - the region name

    """
    pass



class FlighPathEncounterSchema:
    """
    Structured stream schemas for :py:meth:`~streamsx.geospatial.FlightPathEncounter`.
    
    All schemas defined in this class are instances of `streamsx.topology.schema.StreamSchema`.
    
    """

    EncounterEvents = StreamSchema (_SPL_SCHEMA_FLIGHTPATH_ENCOUNTER_EVENT)
    """
    The :py:meth:`~streamsx.geospatial.FlightPathEncounter` creates encounter events as output.
    An encounter consists of the original observation, the data for the encountered object and the distances in time and space between the colliding objects.
    This schema is provided for convenience as it can be used as input and output type for the :py:meth:`~streamsx.geospatial.FlightPathEncounter`. 
    
    The schema defines following attributes
    
    * observation(StreamSchema) - The input observation encounters are calculated for. This is a tuple attribute of type :py:meth:`~streamsx.geospatial.schema.FlighPathEncounterSchema.Observation3D`.
    * encounter(StreamSchema) - The data for the object that is encountered. This is a tuple attribute of type :py:meth:`~streamsx.geospatial.schema.FlighPathEncounterSchema.Observation3D`.
    * encounterDistance(float64) - The latitude/longitude distance between the two objects at the time of the encounter. It is given in meters.
    * encounterTime(int64) - The time in the future the encounter will happen. It is an absolute time given in milliseconds since January 1st 1970 (Posix time).

    """

    Observation3D = StreamSchema (_SPL_SCHEMA_FLIGHTPATH_OBSERVATION3D)
    """
    The :py:meth:`~streamsx.geospatial.FlightPathEncounter` processes observations of flying objects.

    Each observation needs to conform to the Observation3D type. The schema defines following attributes
    
    * entityId(str) - The unique identifier of the flying object. You may use the ICAO field from an ADSB feed.
    * latitude(float64) - The latitude of the object in degrees. Allowed values are in the range from -90 to 90.
    * longitude(float64) - The longitude of the object in degrees. Allowed values are in the range from -180 to 180.
    * altitude(float64) - The altitude of the object in meters. Allowed values are greater or equal 0. If you need to convert from feet to meters, multiply the feet by 0.3048.
    * observationTime(int64) - The time stamp of the last observation of this object. Given in milliseconds as Posix time (milliseconds since January 1st 1970).
    * azimuth(float64) - The azimuth of the object. This is the clockwise angle between the objects motion direction and a line from the object to the north pole. Given in degrees (for example if the plane is flying to the east, this will be 90 degrees). Allowed values are 0 to 360.
    * groundSpeed(float64) - The groundSpeed of the object in meters per second. There is a dependency between this value and the timeSearchInterval parameter of the operator. At the given speed the object must not travel more than 20000 kilometers within the given timeSearchInterval. For example with a time search interval of 15 minutes (900000 ms) the object speed must not be faster than 80000 km/h (~22000 m/s). For all practical purposes this should not be a serious limitation. If you need to convert from knots to meters/second multiply the knots by 0.514444.
    * altitudeChangeRate(float64) - The altitudeChangeRate of the object in meters per second. Positive values denote increasing altitude.

    """
    pass
