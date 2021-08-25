from azure.mgmt.resource import ResourceManagementClient
import Config
import Location

#Emplacement
Location

# Step 1 Créer un groupe de ressources
rg_client = ResourceManagementClient(Config.credential, Config.subscription_id)

# Vous pouvez modifier ces valeurs comme vous le souhaitez
RESOURCE_GROUP_NAME = "RG-Python-VM"


result = rg_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, {"location" : Location.LOCATION})
print(f"Groupe de ressources approvisionné {result.name} dans la région {result.location} ")