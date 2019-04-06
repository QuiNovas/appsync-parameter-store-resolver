appsync-parameter-store-resolver
================================

.. _APL2: http://www.apache.org/licenses/LICENSE-2.0.txt

This is an AWS Lambda designed to resolve appsync requests to Parameter Store.

AWS Permissions Required
------------------------
- ssm:GetParameter
- ssm:GetParameters
- ssm:GetParametersByPath
- ssm:PutParameter

Handler Method
--------------
.. code::

  function.handler

Request Syntax
--------------
The event is passed in as a JSON object. Examples:

.. code::

  {
    "operation": "getParameter",
    "attributes": {
      "name": "name"
    }
  }

  {
    "operation": "getParameters",
    "attributes": {
      "names": ["name1", "name2]
    }
  }

  {
    "operation": "getParametersByPath",
    "attributes": {
      "path": "path",
      "recursive": true | false
    }
  }

  {
    "operation": "putParameter",
    "attributes": {
      "name": "",
      "description": "",
      "value": "string",
      "secure": true | false,
      "overwrite": true|false
    },
    "keyId": ""
  }

**operation** - REQUIRED
  Can be one of ``getParameter``, ``getParameters``, ``getParametersByPath``,
  or ``putParameter``.

**getParameter**
  :name: the name of the parameter to get - REQUIRED

**getParameters**
  :names: the names of the parameters to get - REQUIRED

**getParametersByPath**
  :path: the path to get parameters under - REQUIRED
  :recursive: ``true`` or ``false`` - REQUIRED

**putParameter**
  :name: the name of the paramter to put - REQUIRED
  :description: the description of the parameter - OPTIONAL
  :value: the value of the parameter. If this contains a ``,`` then a ``StringList`` will be used - REQUIRED
  :secure: ``true`` or ``false`` - OPTIONAL, defaults to ``false``
  :overwrite: ``true`` or ``false`` - OPTIONAL, defaults to ``true``
  :keyId: the KMS Key ARN or ID to encrypt the parameter - OPTIONAL, defaults to the account key

Each of these requests can be batched via the `BatchInvoke` protocol
from Appsync.

Response syntax
---------------
For ``getParameter`` and ``putParameter``:

.. code::

  {
    "name": "string",
    "value": "string",
    "lastModifiedDate": "iso8601 datetime",
    "version": int
  }

For ``getParameters`` and ``getParametersByPath``:

.. code::

  [
    {
      "name": "string",
      "value": "string",
      "lastModifiedDate": "iso8601 datetime",
      "version": int
    }
  ]

Example AWS Appsync schema:

.. code::

  type Mutation {
    putParameter(
      name: String!,
      value: String!,
      description: String,
      secure: Boolean,
      overwrite: Boolean
    ): Parameter
  }

  type Parameter {
    name: String!
    value: String!
    lastModifiedDate: AWSDateTime!
    version: Int!
  }

  type Query {
    getParameter(name: String!): Parameter
    getParameters(names: [String]!): [Parameter]
    getParametersByPath(path: String!, recursive: Boolean!): [Parameter]
  }

  schema {
    query: Query
    mutation: Mutation
  }

Lambda Package Location
-----------------------
https://s3.amazonaws.com/lambdalambdalambda-repo/quinovas/appsync-parameter-store-resolver/appsync-parameter-store-resolver-0.0.1.zip

License: `APL2`_
