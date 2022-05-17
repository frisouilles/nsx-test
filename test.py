import json
from lib import auth
from lib import getargs
from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.bindings.converter import TypeConverter
from com.vmware.nsx.model_client import VirtualNetworkInterface, IPSet
from com.vmware.nsx_policy.model_client import (Expression,
                                                Group,
                                                ExternalIDExpression,
                                                IPAddressExpression)

# Create a pretty printer to make the output look nice.
pp = PrettyPrinter()

def find_virtual_network_interface_by_ip(api_client, ip):
    search = api_client.search.Query.list(query=f"resource_type:virtualnetworkinterface AND ip_address_info.ip_addresses:{ip}")
    return [vni.convert_to(VirtualNetworkInterface) for vni in search.results]

def get_sg(api_client, sg_name):
    # Get group
    group = api_client.infra.domains.Groups.get("default", sg_name)

    return group

def create_sg(api_client, sg_name, addresses=[]):
    address_in_sg = []
    if not addresses:
        address_in_sg = [IPAddressExpression(ip_addresses=["255.255.255.255"])]

    # Create group obj
    group_obj = Group(display_name=sg_name)
    # push to nsx
    api_client.infra.domains.Groups.patch("default", sg_name, group_obj)
    # Return new group
    return api_client.infra.domains.Groups.get("default", sg_name)


def update_sg(api_client, sg_name, sg_new_name):
    old_group = api_client.infra.domains.Groups.get("default", sg_name)
    old_group.display_name = sg_new_name
    new_group = api_client.infra.domains.Groups.update("default", old_group.id, old_group)
    return new_group

def main():
    args = getargs.getargs()

    api_client = auth.create_nsx_api_client(
        args.user,
        args.password,
        args.nsx_host,
        args.tcp_port,
        auth_type=auth.SESSION_AUTH
    )

    policy_api_client = auth.create_nsx_policy_api_client(
        args.user,
        args.password,
        args.nsx_host,
        args.tcp_port,
        auth_type=auth.SESSION_AUTH
    )
        
    #pp.pprint(find_virtual_network_interface_by_ip(api_client, '10.200.161.8'))
    #group = get_sg(policy_api_client, "AFRLMKSDMTA.INT.ADEO.COM")
    #print("group")
    #pp.pprint(group)
    #search = policy_api_client.search.Query.list(
    #    query='resource_type:Segment AND subnets.network:"10.205.156.254/26"'
    #)
    #print("result")
    #pp.pprint(search.results)
    #print("Expression")
    #for expr in group.expression:
    #    pp.pprint(expr.to_dict())
    #pp.pprint(update_sg(policy_api_client, "test-sg-mndb", "test-sg-mndb-2"))
    #pp.pprint(create_sg(policy_api_client, "test-sg-mndb"))

    
    api_client.IpSets.create(IPSet(ip_addresses=["10.200.191.129-10.200.191.132"]))
if __name__ == "__main__":
    main()

    