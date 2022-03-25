#!/usr/bin/env python
# Basic script to load environment variables from a CodeBuild spec.
# Be aware that any you should check or trust the output of this script before loading it in your shell environment.

import yaml
import boto3
import os
import sys

ssm = boto3.client('ssm')


def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        yield every_chunk

spec = ""
with open("buildspec.yml", "r") as stream:
    try:
        spec = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print('Loading hardcoded environment variables', file=sys.stderr)
env_spec = spec['env']
for key in env_spec['variables']:
    value = env_spec['variables'][key]
    print(f'export {key}={value}')

print('Loading parameter-store environment variables', file=sys.stderr)
#param_store_spec = {env_spec['parameter-store'][key]: key for key in env_spec['parameter-store']}
names = [env_spec['parameter-store'][key] for key in env_spec['parameter-store']]
cached_values = {};
for chunk in list_split(names, 10):
    response = ssm.get_parameters(Names=chunk, WithDecryption=True).get('Parameters')
    for param in response:
        cached_values[param['Name']] = param['Value']

for key in env_spec['parameter-store']:
    value=cached_values[env_spec['parameter-store'][key]]
    print(f'export {key}={value}')
