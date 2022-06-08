import json

from com.vmware.nsx_policy.infra_client import Segments
from lib import auth
from lib import getargs
from vmware.vapi.bindings.struct import PrettyPrinter
from vmware.vapi.bindings.converter import TypeConverter
from com.vmware.nsx.model_client import VirtualNetworkInterface, IPSet
from com.vmware.nsx_policy.model_client import (Group,
                                                Rule,
                                                Service,
                                                Segment,
                                                Tag,
                                                L4PortSetServiceEntry,
                                                ExternalIDExpression,
                                                IPAddressExpression)

# Create a pretty printer to make the output look nice.
pp = PrettyPrinter()

if __name__ == "__main__":
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

    group_name = "PGOIPAENISA.INT.ADEO.COM"
    policy_api_client.infra.domains.Groups.patch("default", f"{group_name}", Group(display_name=f"{group_name}", expression=[], tags=[{"tag": "MYNETWORKDB"}]))
    group = policy_api_client.infra.domains.Groups.get("default", f"{group_name}")

    pp.pprint(group)

    