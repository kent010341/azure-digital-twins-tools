# AzureDigitalTwinsTools

## AzureDigitalTwinsTools.Helper.RelationshipHelper
`class AzureDigitalTwinsTools.Helper.RelationshipHelper(token_path, host_name)`  

This class can help you deal with the CRUD requirements of relationships between digital twins.

* Parameters
  * `token_path`: `str`  
    A text file storing the bearer token get by using this command with Azure CLI.  
    `az account get-access-token --resource 0b07f429-9f4b-4714-9392-cc5e8e80c8b0`  
    
  * `host_name`: `str`  
    Host name of the Azure Digital Twins Instance. You can get it from the Azure portal.  
    ![](https://i.imgur.com/tTuBVYM.png)

### list\_relationships
`list_relationships(dtid, relationship_name=None)`  

List all relationships which the source is `dtid`.  
If `relationship_name` is specified, the response will only contain the relationships with this name.

* Parameters  
  * `dtid`: `str`  
    Digital twin ID.  

  * `relationship_name`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will list all relationships.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the content (JSON format string) of response, use `.content`.  
  To get the status code of this HTTP request, use `.status_code`.

### add\_relationship
`add_relationship(dtid, target_dtid, relationship_name)`  

Add a relationship from `dtid` to `target_dtid` with name `relationship_name`.  

* Parameters  
  * `dtid`: `str`  
    Source digital twin ID.  

  * `target_dtid`: `str`  
    Target digital twin ID.  

  * `relationship_name`: `str`  
    Name of the relationship.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

### delete\_relationship
`delete_relationship(dtid, relationship_id)`  

Delete a relationship with Id `relationship_id` from `dtid`.  

* Parameters  
  * `dtid`: `str`  
    Source digital twin ID.  

  * `relationship_id`: `str`  
    ID of the relationship.  

* Return  
  Type: `Response` (from the library `requests`)  
  To get the status code of this HTTP request, use `.status_code`.

### find\_relationships\_with\_target
`find_relationships_with_target(dtid, target_dtid, relationship_name=None)`  

List all relationships which the source is `dtid` and the target is `target_dtid`.  
If `relationship_name` is specified, the response will only contain the relationships with this name.

* Parameters  
  * `dtid`: `str`  
    Source digital twin ID.  

  * `target_dtid`: `str`  
    Target digital twin ID.

  * `relationship_name`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will list all relationships.  

* Return  
  Type: `list` of `dict`  
  The `dict` inside contains 4 keys: `relationshipId`, `relationshipName`, `sourceId`, `targetId`.

### find\_and\_delete\_relationships
`find_and_delete_relationships(dtid, relationship_name=None, target_dtid=None)`

Delete all relationships which the source is `dtid`.  
If `relationship_name` is specified, it will only delete the relationships with this name.  
If `target_dtid` is specified, it will only delete the relationships which the target is this ID.  

* Parameters  
  * `dtid`: `str`  
    Source digital twin ID.  

  * `target_dtid`: `str` (Default: `None`)  
    Target digital twin ID.

  * `relationship_name`: `str` (Default: `None`)  
    Name of the relationship, if not specified, it will delete all relationships matched.  

* Return  
  `None`

## AzureDigitalTwinsTools.Helper.PropertyHelper
`class AzureDigitalTwinsTools.Helper.PropertyHelper(token_path, host_name)`  

This class can help you deal with the CRUD requirements of properties of digital twins.

Except of the method `get_twin_detail`, the other methods are like a builder pattern in order to update multiple properties of a twin in one API calling.  

e.g.,  

```
from AzureDigitalTwinsTools.Helper import PropertyHelper

ph = PropertyHelper(token_path="...", host_name="...")
ph.prepare(dtid="Room1")
  .update_property(key="temperature", value=60)
  .update_property(key="humidity", value=55)
  .add_property(key="name", value="sensor")
  .remove_property(key="remove")
  .submit()
```


* Parameters
  * `token_path`: `str`  
    A text file storing the bearer token get by using this command with Azure CLI.  
    `az account get-access-token --resource 0b07f429-9f4b-4714-9392-cc5e8e80c8b0`  
    
  * `host_name`: `str`  
    Host name of the Azure Digital Twins Instance. You can get it from the Azure portal.  
    ![](https://i.imgur.com/tTuBVYM.png)

### get\_twin\_detail
`get_twin_detail(dtid)`  

Get the details of a digital twin (twin ID: `dtid`), including properties.

* Parameters  
  * `dtid`: `str`  
    Digital twin ID. 

### prepare
`prepare(dtid)`  

Start a process. You can use the methods `update_property`, `add_property`, `remove_property` after calling this method.  

* Parameters  
  * `dtid`: `str`  
    Digital twin ID. 
    
### submit
`submit()`  

Submit the process.  

### update_property
`update_property(key, value)`  

Add an "update" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  

  * `value`: `str`, `int` or `float`  
    Value of property.  

### add_property
`add_property(key, value)`  

Add an "add" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  

  * `value`: `str`, `int` or `float`  
    Value of property.  

### remove_property
`remove_property(key)`  

Add an "remove" process to current updating process.  

* Parameters  
  * `key`: `str`  
    Key of property.  
