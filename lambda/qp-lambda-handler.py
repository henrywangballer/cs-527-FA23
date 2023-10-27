import json
def handler(event, context):
    print(event)

    query_parameters = {} if event.get("queryStringParameters") is None else event.get("queryStringParameters")
    message = query_parameters.get('message', 'No message')
    output = f'Message: {message}'

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }
