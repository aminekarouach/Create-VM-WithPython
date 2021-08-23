import logging
from azure.identity import AzureCliCredential
from azure.identity._credentials.user_password import UsernamePasswordCredential
from azure.mgmt import network
from azure.mgmt import compute
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import os

print(f"Approvisionnement d'une VM dans Azure")

#credential

credential = AzureCliCredential()

#Récupération de l'ID d'abonnement à partir de la variable.

sub_id = os.environ["Azure_Sub_Id"] = "729c7ae2-5a3d-4f30-9935-8d87f3158969"

# Step 1 Créer un groupe de ressources

rg_client = ResourceManagementClient(credential, sub_id)

# Vous pouvez modifier ces valeurs comme vous le souhaitez
RESOURCE_GROUP_NAME = "RG-Python-VM"

#Emplacement

LOCATION = "northeurope"

result = rg_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, {"location" : LOCATION})

print(f"Groupe de ressources approvisionné {result.name} dans la région {result.location} ")

# Step 2 Mettre en service le réseau virtuel

# Définir le noms de réseau et l'adresse IP

VNET_NAME = "vnet-exemple" 
SUBNET_NAME = "subnet-exemple"
IP_NAME = "ip-exemple"
IP_CONFIG_NAME = "ip-config-exemple"
NIC_NAME = "nic-exemple"

# Obtenir l'objet de gestion pour le réseau

network_client = NetworkManagementClient(credential, sub_id)

poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space" : {
            "address_prefixes": ["192.0.0.0/16"]
        }
    }
)

vnet_result = poller.result()

# Step 3 - Créer le sous-réseau
poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME, SUBNET_NAME, {"address_prefix": "192.0.0.0/24" }
)
subnet_result = poller.result()

# Step 4 - Créer l'adresse IP
poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME, IP_NAME,{
    "location" : LOCATION,
    "sku": { "name": "Standard"},
    "public_ip_allocation_method": "Static",
    "public_ip_address_version": "IPV4"

})

ip_address_result = poller.result()

# Step 5 - Créer le network interface
poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME, NIC_NAME, {
    "location" : LOCATION,
    "ip_configurations": [{
        "name" : IP_CONFIG_NAME,
        "subnet" : { "id": subnet_result.id},
        "public_ip_address": {"id": ip_address_result.id}

    }]
})

nic_result = poller.result()

# Step 6 - Création de la VM | Configuration de base

Compute_client = ComputeManagementClient(credential, sub_id)

VM_NAME = "PythonAzureVM"
Username = "UserAdmin"
PASSWORD = "P@ssw0rd2000"

print(f"Prosionnement de la VM {VM_NAME}; cette operation peut prendre quelques minutes !")

# sizing & Version
poller = Compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
{
    "location": LOCATION,
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
            "id": nic_result.id,
        }]
    }
})
vm_result = poller.result()

print(f" Machine virtuelle provisionnée {vm_result.name}")

