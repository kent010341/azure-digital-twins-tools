# adttools

## System Requirement
* Python 3.6 or above
* pandas

---

## Table of contents
* [ModelHelper](#azuredigitaltwinstoolshelpermodelhelper)  
  * [list_models](#list_models)  
  * [find_model_components_list](#find_model_components_list)
  * [picker](#picker)
  * [get_component_dict](#get_component_dict)
* [RelationshipHelper](#azuredigitaltwinstoolshelperrelationshiphelper)  
  * [list_relationships](#list_relationships)
  * [add_relationship](#add_relationship)
  * [delete_relationship](#delete_relationship)
  * [find_relationships_with_target](#find_relationships_with_target)
  * [find_and_delete_relationships](#find_and_delete_relationships)
* [PropertyHelper](#azuredigitaltwinstoolshelperpropertyhelper)  
  * [get_twin_detail](#get_twin_detail)  
  * [prepare_property](#prepare_property)
  * [prepare_component](#prepare_component)
  * [prepare_relationship](#prepare_relationship)
  * [submit](#submit)
  * [update_property](#update_property)
  * [add_property](#add_property)
  * [remove_property](#remove_property)
* [TwinHelper](#azuredigitaltwinstoolshelpertwinhelper)  
  * [add_twin](#add_twin)
  * [delete_twin](#delete_twin)
* [QueryHelper](#azuredigitaltwinstoolshelperqueryhelper)  
  * [query_twins](#query_twins)
  * [query_relationships](#query_relationships)
  * [run_query](#run_query)
* [DeployHelper](#azuredigitaltwinstoolshelperqueryhelper)  
  * [csv_deploy](#csv_deploy)
  * [clear](#clear)

---

## adttools.helper
All helpers requires 3 parameters to initialize. Either `token_path` or `token` should be given.  
    
* `host_name`: `str`  
  Host name of the Azure Digital Twins Instance. You can get it from the Azure portal.  
  ![](https://i.imgur.com/tTuBVYM.png)  

* `token_path`: `str`  
  The path of a text file storing the bearer token get by using this command with Azure CLI.  
  `az account get-access-token --resource 0b07f429-9f4b-4714-9392-cc5e8e80c8b0`  

* `token`: `str`  
  A string of token. Get by using this command with Azure CLI.  
  `az account get-access-token --resource 0b07f429-9f4b-4714-9392-cc5e8e80c8b0`  

---

## adttools.helper.ModelHelper
`class adttools.helper.ModelHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the searching requirements of model.  

### list_models
`list_models(model=None)`  

List all model if `model` is not specified.  
If `model` is specified, list all related models including extending and component.  

* Parameters  
  * `model`: `str`  
    Model ID.
    
* Return  
  Type: `dict`  
  Dictionary of each models.

### find_model\_components\_list
`find_model_components_list(model)`  

Get a list of the name of components of `model`.  
This method will affect a private variable which has a getter method `get_component_dict()`.

* Parameters  
  * `model`: `str`  
    Model ID.
    
* Return  
  `None`  
  
### get\_component\_dict
`get_component_dict()`  

Get current found components of models.  

* Return  
  Type: `dict` of `list` of `str`  
  The key is model, value is a list of component of this model.

### picker
`picker(model_folder, model_list, output_folder='picked')`  

Instead of upload all models of a folder, you can use this method the pick the necessary models.  
This method will copy the models of `model_list`, including the models which depend on it from `model_folder` to the folder `output_folder`.  
You can use Azure Digital Twins Explorer or [Azure CLI command](https://docs.microsoft.com/en-us/cli/azure/dt/model?view=azure-cli-latest) to upload the folder of picked models.  

* Parameters  
  * `model_folder`: `str`  
    Folder path storing lots of models. This method will pick the models from here.  
  
  * `model_list`: `list` of `str`  
    List of model IDs.  

  * `output_folder`: `str`  
    The picked models will be copied to here.
    
* Return  
  `None`  

---

## adttools.helper.RelationshipHelper
`class adttools.helper.RelationshipHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the CRUD requirements of relationships between digital twins.

### list\_relationships
`list_relationships(source, rname=None)`  

List all relationships which the source is `source`.  
If `rname` is specified, the response will only contain the relationships with this name.

* Parameters  
  * `source`: `str`  
    Digital twin ID.  

  * `rname`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will list all relationships.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the content (JSON format string) of response, use `.text`.  
  To get the status code of this HTTP request, use `.status_code`.

### add\_relationship
`add_relationship(source, target, rname, init_property={})`  

Add a relationship from `source` to `target` with name `rname`. The properties of relationship can be add with `init_property`.  

* Parameters  
  * `source`: `str`  
    Source digital twin ID.  

  * `target`: `str`  
    Target digital twin ID.  

  * `rname`: `str`  
    Name of the relationship.  

  * `init_property`: `dict`  
    Initial value given to the properties.  
    should look like `{"p_1": 123, "p_2":{"sub_p_1": "some value"}}`  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

### delete\_relationship
`delete_relationship(source, rid)`  

Delete a relationship with Id `rid` from `source`.  

* Parameters  
  * `source`: `str`  
    Source digital twin ID.  

  * `rid`: `str`  
    ID of the relationship.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

### find\_relationships\_with\_target
`find_relationships_with_target(source, target, rname=None)`  

List all relationships which the source is `source` and the target is `target`.  
If `rname` is specified, the response will only contain the relationships with this name.

* Parameters  
  * `source`: `str`  
    Source digital twin ID.  

  * `target`: `str`  
    Target digital twin ID.

  * `rname`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will list all relationships.  

* Return  
  Type: `list` of `dict`  
  The `dict` inside contains 4 keys: `relationshipId`, `relationshipName`, `sourceId`, `targetId`.

### find\_and\_delete\_relationships
`find_and_delete_relationships(source, rname=None, target=None)`

Delete all relationships which the source is `source`.  
If `rname` is specified, it will only delete the relationships with this name.  
If `target` is specified, it will only delete the relationships which the target is this ID.  

* Parameters  
  * `source`: `str`  
    Source digital twin ID.  

  * `target`: `str` (Default: `None`)  
    Target digital twin ID.

  * `rname`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will delete all relationships matched.  

* Return  
  `None`

---

## adttools.helper.PropertyHelper
`class adttools.helper.PropertyHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the CRUD requirements of properties of digital twins, including the properties of a component.

Except for the method `get_twin_detail`, the other methods are like a builder pattern in order to update multiple properties of a twin in one API calling.  

e.g.,  

```
from adttools.helper import PropertyHelper

ph = PropertyHelper(token_path="...", host_name="...")
ph.prepare_property(dtid="Room1")
  .update_property(key="temperature", value=60)
  .update_property(key="humidity", value=55)
  .add_property(key="name", value="sensor")
  .remove_property(key="remove")
  .submit()
```

### get\_twin\_detail
`get_twin_detail(dtid)`  

Get the details of a digital twin (twin ID: `dtid`), including properties.

* Parameters  
  * `dtid`: `str`  
    Digital twin ID.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the content (JSON format string) of response, use `.text`.  
  To get the status code of this HTTP request, use `.status_code`.

### prepare_property
`prepare(dtid)`  

Start a process for updating property. You can use the methods `update_property`, `add_property`, `remove_property` after calling this method.  

* Parameters  
  * `dtid`: `str`  
    Digital twin ID. 

* Return  
  `self`

### prepare_component
`prepare_component(dtid, component_path)`

Start a process for updating component. You can use the methods `update_property`, `add_property`, `remove_property` after calling this method.  

* Parameters  
  * `dtid`: `str`  
    Digital twin ID.  

* Return  
  `self`

### prepare_relationship
`prepare_relationship(source, rid)`

Start a process for updating properties of a relationship. You can use the methods `update_property`, `add_property`, `remove_property` after calling this method.  

* Parameters  
  * `source`: `str`  
    Source digital twin ID.  

  * `rid`: `str`  
    ID of the relationship.  

* Return  
  `self`

### submit
`submit()`  

Submit the process.  

* Return  
  `None`

### update_property
`update_property(key, value)`  

Add an "update" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  

  * `value`: `str`, `int` or `float`  
    Value of property.  

* Return  
  `self`

### add_property
`add_property(key, value)`  

Add an "add" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  

  * `value`: `str`, `int` or `float`  
    Value of property.  

* Return  
  `self`

### remove_property
`remove_property(key)`  

Add an "remove" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  

* Return  
  `self`

---

## adttools.helper.TwinHelper
`class adttools.helper.TwinHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the basic requirements of digital twins.  

### add_twin
`add_twin(dtid, model, init_property={}, init_component={})`  

Add a digital twin with specified model ID, the initial value of properties and component can be set by using dictionary.  

* Parameters  
  * `dtid`: `str`  
    Digital twin ID  

  * `model`: `str`  
    dtmi (digital twins model ID)  

  * `init_property`: `dict`  
    Initial value given to the properties  
    should look like `{"p_1": 123, "p_2":{"sub_p_1": "some value"}}`  

  * `init_component`: `dict`  
    Initial value given to the components  
    should look like `{"c_1": {"c_1_property": "some value"}}`  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

### delete_twin
`delete_twin(dtid)`  

Delete a digital twin with digital twin ID.  

* Parameters  
  * `dtid`: `str`  
    Digital twin ID  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

---

## adttools.helper.QueryHelper
`class adttools.helper.QueryHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the requirements of querying digital twins and relationships.  

### query_twins
`query_twins(dtid=None, condition=None)`

Query twins.

* Parameters  
  * `dtid`: `str` (Default: `None`)  
    Source digital twin ID.  

  * `condition`: `str` (Default: `None`)  
    Other condition can be placed here. 

* Return  
  Type: `list` of `dict`  
  The matched twins.

### query_relationships
`query_relationships(source=None, target=None, rname=None)`

Query relationships.

* Parameters  
  * `source`: `str` (Default: `None`)  
    Source digital twin ID.  
    
  * `target`: `str` (Default: `None`)  
    Target digital twin ID.  

  * `rname`: `str` (Default: `None`)  
    Relationship name. 

* Return  
  Type: `list` of `dict`  
  The matched relationships.

### run_query
`run_query(self, query)`  

Run a query string.

* Parameters  
  * `query`: `str`   
    Query string.  

* Return  
  Type: `list` of `dict`  
  The matched objects.

---

## adttools.helper.DeployHelper
`class adttools.helper.DeployHelper(host_name, token_path=None, token=None)`  

This class can help you deal with the requirements of batch deployment of digital twins.  

### csv_deploy
`csv_deploy(path, atomic=True)`  

Deploy digital twins with a csv file.  

* Columns of this CSV file should be `modelid`, `dtid`, `init_property`, `init_component`, , `rname`, `rtarget`, `init_rproperty`.  
  `init_property`, `init_component` and `init_rproperty` are optional columns.
  * `modelid`: model ID
  * `dtid`: Twin ID
  * `init_property`: (JSON format) Can be empty, the initial value of properties.
  * `init_component`: (JSON format) Can be empty, the initial value of components.
  * `rname`: Relationship name, if `rname` is specified, `rtarget` is required. If multiple relationships are required, just add a new line without `modelid` and using an existing `dtid`.
  * `rtarget`: Target twin ID if a relationship (`rname`) is specified.
  * `init_rproperty`: Initial value of properties of relationship if a relationship (`rname`) is specified.

* Parameters  
  * `path`: `str`  
    CSV file path.  

  * `atomic`: `bool`  
    If set as `True`, any step failed during this deployment will start a deletion process to delete the twins and relationships just created.  
    If set as `False`, any step failed during this deployment will store to a CSV file (file name: `<file name>_failed.csv`) containing the failed twins and relationships. You can fix it and re-deploy it.  

* Return  
  `None`

### clear
`clear()`

Clean all twins and relationships.

* Return  
  `None`
