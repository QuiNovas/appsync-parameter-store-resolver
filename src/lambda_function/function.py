import boto3
import json
import logging.config

CLIENT = boto3.client('ssm')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.info('Processing event :{}'.format(json.dumps(event)))
	if isinstance(event, dict):
		logger.info('Processing Invoke operation')
		return _operation(event)
	elif isinstance(event, (list, tuple)):
		logger.debug('Processing BatchInvoke operation with a batch of {}'.format(len(event)))
		return list(map(_operation, event))
	else:
		raise ValueError('Event type {} is not supported'.format(type(event)))


def _operation(event):
	if event['operation'] == 'getParameter':
		return _get_parameter(event['arguments']['name'])
	elif event['operation'] == 'getParameters':
		response = CLIENT.get_parameters(
			Names=event['arguments']['names'],
			WithDecryption=True
		)
		return list(map(_transform_parameter, response['Parameters']) if 'Parameters' in response else [])
	elif event['operation'] == 'getParametersByPath':
		return _get_parameters_by_path(event['arguments'])
	elif event['operation'] == 'putParameter':
		if ',' in event['arguments']['value'] and event['arguments'].get('secure', False):
			raise ValueError('Parameter cannot be both a StringList and Secure')
		if event['arguments'].get('secure', False) and 'keyId' in event:
			CLIENT.put_parameter(
				Name=event['arguments']['name'],
				Description=event['arguments'].get('description',''),
				Value=event['arguments']['value'],
				Type='StringList' if ',' in event['arguments']['value'] else 'SecureString' if event['arguments'].get('secure', False) else 'String',
				KeyId=event['keyId'],
				Overwrite=event['arguments'].get('overwrite', True)
			)
		else:
			CLIENT.put_parameter(
				Name=event['arguments']['name'],
				Description=event['arguments'].get('description',''),
				Value=event['arguments']['value'],
				Type='StringList' if ',' in event['arguments']['value'] else 'SecureString' if event['arguments'].get('secure', False) else 'String',
				Overwrite=event['arguments'].get('overwrite', True)
			)
		return _get_parameter(event['arguments']['name'])
	else:
		raise ValueError('operation {} not supported'.format(event['operation']))


def _get_parameter(name):
	response = CLIENT.get_parameter(
		Name=name,
		WithDecryption=True
	)
	return _transform_parameter(response['Parameter']) if 'Parameter' in response else {}		


def _get_parameters_by_path(arguments, next_token=None):
	if not next_token:
		response = CLIENT.get_parameters_by_path(
			Path=arguments['path'],
			Recursive=arguments['recursive'],
			WithDecryption=True
		)
	else:
		response = CLIENT.get_parameters_by_path(
			Path=arguments['path'],
			Recursive=arguments['recursive'],
			WithDecryption=True,
			NextToken=next_token
		)
	parameters = list(map(_transform_parameter, response['Parameters']) if 'Parameters' in response else [])
	return parameters if not 'NextToken' in response else parameters.extend(_get_parameters_by_path(arguments, response['NextToken']))


def _transform_parameter(parameter):
	return {
		'name': parameter['Name'],
		'value': parameter['Value'],
		'lastModifiedDate': parameter['LastModifiedDate'].isoformat(),
		'version': parameter['Version']
	}