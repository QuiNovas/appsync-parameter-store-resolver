# appsync-parameter-store-resolver
This is a generic Lambda function that that resolves appsync requests to Parameter Store.

# Environment Variables:
- **SSM_KMS_KEY_ARN** [OPTIONAL] - The arn of the KMS key used for encryption and decryption of SecureString parameters.

# AWS Permissions Required:
- AWS Parameter Store  :GetParameter
- AWS Parameter Store  :GetParameters
- AWS Parameter Store  :GetParameterByPath
- AWS Parameter Store  :PutParameter

# Handler Method
function.handler

# Request syntax
```
{
  "GetParameters": {
    "Names": [] - this will always be an array, for one parameter it will simply be an array of one
  },
  "GetParametersByPath": {
    "Path": "" - required,
    "Recursive": true | false - required
  },
  "PutParameter": {
    "Name": "", - required
    "Description": "", - optional
    "Value": "" | [], - required. If a list, will be converted to a StringList
    "Secure": true | false, - defaults to false. Throws error if true and "Value" is a []
    "KeyId": "",  - optional
    "Overwrite": true|false, - optional, default is false
  }
}
```
# Response syntax

For GetParameter :
```
"Parameters": {
      "name": { - the name of the parameter is the key
          "Type": "String" | "StringList" | "SecureString",
          "Value': 'string' | ['string'], - the [] is if it was a StringList
          "Version": 123,
          "Selector": "string",
          "SourceResult": "string",
          "LastModifiedDate": "datetime",
          "ARN": "string"
      },
}
```

 
# Lambda package location
https://s3.amazonaws.com/lambdalambdalambda-repo/quinovas/appsync-parameter-store-resolver/appsync-parameter-store-resolver-0.0.1.zip


