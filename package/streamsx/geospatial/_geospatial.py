# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import os
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring
import datetime
import json

def _add_toolkit_dependency(topo):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, 'com.ibm.streams.geospatial', '[2.0.0,4.0.0)')

def _check_time_param(time_value, parameter_name):
    if isinstance(time_value, datetime.timedelta):
        result = time_value.total_seconds()
    elif isinstance(time_value, int):
        result = time_value
    else:
        raise TypeError(time_value)
    if result <= 1:
        raise ValueError("Invalid "+parameter_name+" value. Value must be at least one second.")
    return result

def _add_model_file(topology, path):
    filename = os.path.basename(path)
    topology.add_file_dependency(path, 'etc')
    return 'etc/'+filename

def region_match(stream, schema, model_input_attribute_mapping, model_output_attribute_mapping=None, model_stream=None, model_path=None, success_attribute_name=None, error_reason_attribute_name=None, raw_result_attribute_name=None, wml_meta_data_attribute_name=None, initial_model_provisioning_timeout=None, name=None):
    """Uses the PMMLScoring operator to score tuple data.

    The PMMLScoring operator scores tuple data it receives on the first port, mapping input attributes to model predictors of a configurable PMML model, which may be updated via a second port during runtime. The predicted value (score) is sent together with the original input tuple and some model meta information to the ouput port.
    The mapping of model output fields to streams output attributes can be configured.    
    The model data can be loaded from a file on startup of the operator. Additionally, model data can be sent to the second input port in PMML format. This allows to update the model during runtime. 

    Args:
        stream(Stream): Stream of tuples containing the records to be scored.
        schema(Schema): Output streams schema
        model_input_attribute_mapping(str): Maps input stream attributes to predictors in the format ``predictorName1=streamsAttribute1,predictorName2=streamsAttribute2,...`` 
        model_output_attribute_mapping(str): Maps output stream attributes to model output fields in the format ``streamsAttribute1=modelOutputField1,streamsAttribute2=modelOutputField2,...``
        model_stream(Stream): Stream of tuples containing new model versions and model metadata. The tuple requires the type ``com.ibm.streams.pmml::ModelData``. Connect the output stream of ``model_feed`` to this port.
        model_path(str): The path to a local model file. The file has to be in PMML format. This model is loaded on startup of the operator and used for scoring until a new model arrives at the second input port of the operator. Metadata like name, version, etc. for that model cannot be specifed. Therefore the metadata related attributes on the output port are set to 'unknown' as long as this model is used. 
        success_attribute_name(str): Specify the name of an ouput Stream attribute of type 'boolean'. If set, the result of the scoring operation is stored in this attribute. The value is 'true' if the scoring succeeded, 'false' if an error occured. 
        error_reason_attribute_name(str): Specify the name of an ouput Stream attribute of type 'rstring'. If set, an error description is stored in this attribute, in case the operation failed. If the scoring operation was successful, en empty string is stored in the attribute. 
        raw_result_attribute_name(str): Use this parameter to get the model output as JSON string. It specifies the name of an output attribute of type 'rstring' that will get the JSON string. The JSON structure is an array. Each entry contains a row returned from the model after scoring the input record. The entris contain the returned value and the ResultDesciptor that contains all metadata about the entry.
        wml_meta_data_attribute_name(str): Specifies the name of an ouput Stream attribute of type 'map<rstring,rstring>, If set, the map will contain the metadata fetched from the WML repository by the 'WMLModelFeed operator. The data will be just passed through by this operator for debugging and reference purposes. In case the model was not loaded from the WML repository, but by using the 'modelPath' parameter, the map will be empty.
        initial_model_provisioning_timeout(int|datetime.timedelta): Setting this parameter causes the operator to wait for some time until the inital model is loaded. If the modelPath parameter is not used, no initial model is loaded from a file during operator startup. In this case the operator will send tuples to the output port without scoring them. Instead the error indicator is set. To allow for some wait time before the model is loaded from the WML repository, set the parameter to the number of seconds to wait before the initial model is loaded. If the model is not loaded within this time interval, the operator aborts. 
        name(str): Operator name in the Streams context, defaults to a generated name.

    Returns:
        Output Stream with specified schema
    """
    # python wrapper pmml toolkit dependency
    _add_toolkit_dependency(stream.topology)

    if model_path is None and model_stream is None:
        raise ValueError("Either set model_path or model_stream or both.")
    if model_output_attribute_mapping is None and raw_result_attribute_name is None:
        raise ValueError("Either set model_output_attribute_mapping or raw_result_attribute_name or both.")

    if model_path is not None:
        model_path = _add_model_file(stream.topology, model_path)

    _op = _PMMLScoring(stream, schema=schema, model_stream=model_stream, modelPath=model_path, modelInputAttributeMapping=model_input_attribute_mapping, modelOutputAttributeMapping=model_output_attribute_mapping, successAttributeName=success_attribute_name, errorReasonAttributeName=error_reason_attribute_name, rawResultAttributeName=raw_result_attribute_name, wmlMetaDataAttributeName=wml_meta_data_attribute_name, name=name)

    if initial_model_provisioning_timeout is not None:
        _op.params['initialModelProvisioningTimeout'] = streamsx.spl.types.int32(_check_time_param(initial_model_provisioning_timeout, 'initial_model_provisioning_timeout'))

    return _op.outputs[0]

class _PMMLScoring(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema, model_stream=None, errorReasonAttributeName=None, initialModelProvisioningTimeout=None, modelInputAttributeMapping=None, modelOutputAttributeMapping=None, modelPath=None, rawResultAttributeName=None, successAttributeName=None, wmlMetaDataAttributeName=None, name=None):
        topology = stream.topology
        kind="com.ibm.streams.pmml::PMMLScoring"
        
        if model_stream is None:
            inputs=stream
        else:
            inputs=[stream,model_stream]
        schemas=schema
        params = dict()

        if errorReasonAttributeName is not None:
            params['errorReasonAttributeName'] = errorReasonAttributeName
        if initialModelProvisioningTimeout is not None:
            params['initialModelProvisioningTimeout'] = initialModelProvisioningTimeout
        if modelInputAttributeMapping is not None:
            params['modelInputAttributeMapping'] = modelInputAttributeMapping
        if modelOutputAttributeMapping is not None:
            params['modelOutputAttributeMapping'] = modelOutputAttributeMapping
        if modelPath is not None:
            params['modelPath'] = modelPath
        if rawResultAttributeName is not None:
            params['rawResultAttributeName'] = rawResultAttributeName
        if successAttributeName is not None:
            params['successAttributeName'] = successAttributeName
        if wmlMetaDataAttributeName is not None:
            params['wmlMetaDataAttributeName'] = wmlMetaDataAttributeName
 
        super(_PMMLScoring, self).__init__(topology,kind,inputs,schema,params,name)

