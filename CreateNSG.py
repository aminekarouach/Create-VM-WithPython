import GetObjectNetwork
import CreateRG
import Location
from azure.mgmt.network.models import NetworkSecurityGroup
from azure.mgmt.network.models import SecurityRule
import Config

network_client = GetObjectNetwork.NetworkManagementClient(Config.credential, Config.subscription_id)
NSG_NAME = "nsg-exemple"


parameters = NetworkSecurityGroup()
parameters.location = Location.LOCATION
parameters.security_rules = [SecurityRule(
        protocol = 'Tcp',
        access = 'Allow',
        direction = 'Inbound', 
        description='Allow RDP port 3389',
        source_address_prefix = '*',
        destination_address_prefix = '*',
        source_port_range='*', 
        destination_port_range='3389', 
        priority=100, 
        name='RDP1')]   
poller = network_client.network_security_groups.begin_create_or_update(CreateRG.RESOURCE_GROUP_NAME, NSG_NAME, parameters)

nsg_result = poller.result()