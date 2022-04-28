import json
from lib import auth
from lib import getargs
from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.bindings.converter import TypeConverter
from com.vmware.nsx.model_client import VirtualNetworkInterface
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
    group = api_client.infra.domains.Groups.get("default", sg_name)
    for expression in group.get_field("expression"):
        expr_typ = expression.to_dict()["resource_type"]
        expr_obj = ""
        if expr_typ == "ExternalIDExpression":
            expr_obj = expression.convert_to(ExternalIDExpression)
        elif expr_typ == "IPAddressExpression":
            expr_obj = expression.convert_to(IPAddressExpression)
        pp.pprint(expr_obj)

    members_types = api_client.infra.domains.groups.MemberTypes.get("default", sg_name)
    for mbr_type in members_types.results:
        if mbr_type == "IPAddress":
            ip_addresses = api_client.infra.domains.groups.members.IpAddresses.list("default", sg_name)
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
    group = get_sg(policy_api_client, "test-sg-mndb")
    #pp.pprint(update_sg(policy_api_client, "test-sg-mndb", "test-sg-mndb-2"))
    #pp.pprint(create_sg(policy_api_client, "test-sg-mndb"))

if __name__ == "__main__":
    main()

    