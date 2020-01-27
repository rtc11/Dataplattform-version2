import boto3


def add_parameter(value, type):

	name = input("Name:")
	description = input("Description:")
	stage = input("Stage(dev, test, prod):")
	service = input("Service:")
	overwrite = bool(input("Overwrite existing value, true/false?:"))

	tags = []
	while True:
		if input("Add new tag? y/n:") is "y":
			key = input("Key:")
			value = input("Value:")
			tags.append({"Key": key, "Value": value})
		else: 
			break

	session = boto3.Session(profile_name="new")
	
	client = session.client('ssm')

	finalName = "/" + stage + "/" + service + "/" + name

	response = client.put_parameter(
		Name=finalName,
		Description=description,
		Value=value,
		Type=type,
		Overwrite=overwrite,
		Tier='Standard'
	)

	tags.append({
					'Key': 'Project',
					'Value': 'Dataplattform'
				})

	response = client.add_tags_to_resource(
		ResourceType='Parameter',
		ResourceId=finalName,
		Tags=tags
	)

	return finalName




def main():
	type = int(input("Type of parameter(1, 2, or 3)? 1=String, 2=StringList, 3=SecureString:"))
	value = input("Value:")

	types = ["String", "StringList", "SecureString"]

	response = add_parameter(value, types[type-1])

	print("Final name: " + response)

if __name__== "__main__" :
	main()