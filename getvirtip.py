#!/usr/bin/env python3

import libvirt
from argparse import ArgumentParser

filename = "ansible/hosts"

IPTYPE = {
    libvirt.VIR_IP_ADDR_TYPE_IPV4: "ipv4",
    libvirt.VIR_IP_ADDR_TYPE_IPV6: "ipv6",
}


def get_dom_ip(dom: libvirt.virDomain) -> None:
    try:
        ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE)
    except:
        raise SystemExit("Erro ao obter ip")

    if ifaces is None:
        print("Failed to get domain interfaces")
        exit(0)

    for (name, val) in ifaces.items():
        if val['addrs']:
            for addr in val['addrs']:
                return addr['addr']
        else:
            return Null


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("domain")
    args = parser.parse_args()

    try:
        conn = libvirt.open("qemu:///system")
    except:
        raise SystemExit("Unable to open connection to libvirt")

    try:
        dom = conn.lookupByName(args.domain)
    except:
        print("Domain %s not found" % args.domain)
        exit(0)

    ip=get_dom_ip(dom)

    if ip:
        f = open(filename , "w")
        f.write(f'[all]\n{ip}\n')
        f.close()
        print(ip)

    conn.close()

