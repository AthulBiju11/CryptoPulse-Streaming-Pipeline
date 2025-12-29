# Databricks notebook source
import requests
import json

workspace_url = "https://" + spark.conf.get("spark.databricks.workspaceUrl")
token = dbutils.secrets.get(scope="cryptopulse-scope", key="workspace-token")
headers = {"Authorization": f"Bearer {token}"}

# COMMAND ----------

# Use this cell to create DB Secret Scope
secret_scope = "cryptopulse-scope"

scope_data = {
   "scope": secret_scope,
   "initial_manage_principal": "users" 
}


create_response = requests.post(
   f"{workspace_url}/api/2.0/secrets/scopes/create",
   headers=headers,
   json=scope_data
)

if create_response.status_code == 200:
   print("Success: Scope 'cryptopulse-scope' created.")
else:
   print(f"Note: {create_response.text}") 


# COMMAND ----------

# Use this cell to delete DB Secret if any mistakes were made in the initial try
secret_scope = "cryptopulse-scope"
secret_key = "eventhub-conn-string"

secret_data = {
   "scope": "cryptopulse-scope",
   "key": "eventhub-conn-string"
}

put_response = requests.post(
   f"{workspace_url}/api/2.0/secrets/delete",
   headers=headers,
   json=secret_data
)

# COMMAND ----------

# Use this cell to set DB Secret

secret_scope = "cryptopulse-scope"
secret_key = "eventhub-conn-string"
secret_variable = "XXXX"

secret_data = {
   "scope": secret_scope,
   "key": secret_key,
   "string_value": secret_variable
}

put_response = requests.post(
   f"{workspace_url}/api/2.0/secrets/put",
   headers=headers,
   json=secret_data
)

if put_response.status_code == 200:
   print(f"Success: Secret '{secret_data['key']}' is now stored!")
else:
   print(f"Error: {put_response.text}")
