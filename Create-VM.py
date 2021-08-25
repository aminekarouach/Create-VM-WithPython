import logging
from azure.mgmt.compute import ComputeManagementClient
import Config
import Location
import CreateRG
import CreateSubnet
import CreateIpAdresse
import CreateNSG
import CreateNiC
import CreateVnet


#Démarrage
print(f"Approvisionnement d'une VM dans Azure")

# Step 1 Créer un groupe de ressources
CreateRG

# Step 2 Mettre en service le réseau virtuel
CreateVnet

# Step 3 - Créer le sous-réseau
CreateSubnet

# Step 4 - Créer l'adresse IP
CreateIpAdresse

# Step 5 -Créer le NSG avec le port RDP
CreateNSG

# Step 6 - Créer le network interface
CreateNiC

# Step 7 - Création de la VM | Configuration de base
Compute_client = ComputeManagementClient(Config.credential, Config.subscription_id)
VM_NAME = "PythonAzureVM"
Username = "UserAdmin"
PASSWORD = "P@ssw0rd2000"

print(f"Prosionnement de la VM {VM_NAME}; cette operation peut prendre quelques minutes !")
# sizing & Version
poller = Compute_client.virtual_machines.begin_create_or_update(CreateRG.RESOURCE_GROUP_NAME, VM_NAME,
{
    "location": Location.LOCATION,
    "storage_profile": {
        "image_reference": {
            "publisher": 'MicrosoftWindowsDesktop',
            "offer": "Windows-10",
            "sku": "20h2-pro",
            "version": "latest"
        }
    },
    "hardware_profile":{
        "vm_size": "Standard_DS1_v2"
    },
    "os_profile":{
        "computer_name": VM_NAME,
        "admin_username": Username,
        "admin_password": PASSWORD
    },
    "network_profile": {
        "network_interfaces": [{
            "id": CreateNiC.nic_result.id,
        }]
    }
})
vm_result = poller.result()

print(f" Machine virtuelle provisionnée {vm_result.name}")

