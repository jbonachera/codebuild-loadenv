Basic script to load environment variables from a CodeBuild buildspec file.

Requires pyyaml and boto3.
```
# Check fetched values
curl -s https://raw.githubusercontent.com/jbonachera/codebuild-loadenv/main/load.py| python

# Load values into shell environment
$(curl -s https://raw.githubusercontent.com/jbonachera/codebuild-loadenv/main/load.py| python)
```
