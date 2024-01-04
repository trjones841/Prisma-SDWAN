'''
Prisma SD-WAN - Python script using SDK

This script was written to collect the configuration from a Prisma SD-WAN tenant deployed on Strata Cloud Manager.

'''
__date__ = '4JAN2023'
__author__ = 'Terry Jones'
__version__ = '0.1'
__license__ = 'MIT'
__email__ = 'tejones@paloaltonetworks.com'
__status__ = 'Development'


import datetime
from cgxauth import auth_session
import json

sdk = auth_session()

PRINT = False
WRITE_TO_FILE = True
filename = 'prisma_sdwan_eval_' + str(datetime.date.today()) +'.txt'


# **********************************************************************************************************************
# Methods used for iterating dictionaries

def match_items_by_key(data, key, target_tags):
    matching_items = []
    if 'items' in data and isinstance(data['items'], list):
        for item in data['items']:
            if item[key] != target_tags:
                matching_items.append(item)
    return matching_items

# ********************************************** Executes if this file is run ******************************************
if __name__ == '__main__':

    # Returns the site data for a Prisma SD-WAN tenant
    try:
        site_list = sdk.get.sites()
        site_dict = [
            {'name': item.get("name", None), 'site_id': item["id"]} for item
            in site_list.json().get("items", [])]

        if PRINT == True:
            n = 0
            for i in site_dict:
                print('Site Name: ', site_dict[n]['name'], ' Site ID: ', site_dict[n]['site_id'])
                n += 1

            print('****** ' + str(datetime.date.today()) + ' ******')
            print(json.dumps(site_list.json(), indent=4))

        if WRITE_TO_FILE == True:
            with open(filename, 'w') as f:
                f.write('***** Filename: ' + filename + ' ~~~~~ Date & Time: ' + datetime.date.today().strftime('%B %d, %Y  %H:%M:%S') + ' ******************************\n\n')
                f.write('***** site_list **********\n')
                f.write(json.dumps(site_list.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
                f.write('\n')
    except:
        print('Error occurred in the site data section')


    # Returns the ION data for all sites
    try:
        elements = sdk.get.elements()
        element_dict = [
            {'name': item.get("name", None), 'site_id': item["site_id"], 'serial_number': item.get("hw_id", None), 'element_id': item.get("id")} for item
            in elements.json().get("items", [])]
        # print('Elements: \n',json.dumps(element_dict, indent=4),'\n')  # pretty print

        if PRINT == True:
            print(json.dumps(elements.json(), indent=4))
        if WRITE_TO_FILE == True:
            with open(filename, 'a') as f:
                f.write('***** elements **********\n')
                f.write(json.dumps(elements.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
                f.write('\n')
    except:
        print('Error occurred in the elements data section')


    # Gather interface info for each ion at each site
    try:
        for item in element_dict:
            site_interfaces = sdk.get.interfaces(site_id=item['site_id'], element_id=item['element_id'])
            if PRINT == True:
                print(item['name'])
                print(json.dumps(site_interfaces.json(), indent=4))

            if WRITE_TO_FILE == False:
                with open(filename, 'a') as f:
                    f.write('***** Interface Information **********\n')
                    f.write(item['name'])
                    f.write(json.dumps(site_interfaces.json(), indent=4))
                    f.write(
                        '\n***********************************************************************************************************************\n\n')
                    f.write('\n')
    except:
        print('Error occurred in the interface section')


    # Returns the Service & DC Groups info along with the custom endpoint info
    # Capture only the endpoints that are customer (ie - not auto-generated for Prisma Access)
    try:
        servicebindingmaps_dict = sdk.get.servicebindingmaps()  # servicebindingmaps returns the Service & DC Groups information
        serviceendpoints_dict = sdk.get.serviceendpoints()  # serviceendpoints returns the available endpoints in Service & DC Gruops
        servicelabels_dict = sdk.get.serviceendpoints()

        key_to_match = 'tags'
        target_tags_to_match = ['AUTO-PRISMA_MANAGED']
        custom_serviceendpoints = match_items_by_key(serviceendpoints_dict.json(), key_to_match, target_tags_to_match)
        custom_servicelabels = match_items_by_key(servicelabels_dict.json(), key_to_match, target_tags_to_match) #Filter out auto-generated labels

        if PRINT == True:
            print('servicebindingmaps: ', json.dumps(servicebindingmaps_dict.json(), indent=4), '\n\n')
            print('serviceendpoints: ', json.dumps(custom_serviceendpoints, indent=4), '\n\n')
            print('custom_servicelabels: ', json.dumps(custom_servicelabels, indent=4), '\n\n')

        if WRITE_TO_FILE == True:
            with open(filename, 'a') as f:
                f.write('***** servicebindingmaps **********\n')
                f.write(json.dumps(servicebindingmaps_dict.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
                f.write('\n')
                f.write('***** serviceendpoints **********\n')
                f.write(json.dumps(serviceendpoints_dict.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
                f.write('\n')
                f.write('***** servicebindingmaps **********\n')
                f.write(json.dumps(custom_servicelabels, indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
                f.write('\n')
    except:
        print('Error occurred in the service bindings section')


    # Get the security zones
    try:
        security_zones_dict = sdk.get.securityzones()
        if PRINT == True:
            print(json.dumps(security_zones_dict.json(), indent=4))

        if WRITE_TO_FILE == True:
            with open(filename, 'a') as f:
                f.write('***** security zones **********\n')
                f.write(json.dumps(security_zones_dict.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
    except:
        print('Error occurred in the security zones section')


    # Get the IPSec profile settings
    try:
        ipsec_profiles_dict = sdk.get.ipsecprofiles()
        if PRINT == True:
            print(json.dumps(ipsec_profiles_dict.json(), indent=4))

        if WRITE_TO_FILE == True:
            with open(filename, 'a') as f:
                f.write('***** ipsec profiles **********\n')
                f.write(json.dumps(ipsec_profiles_dict.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
    except:
        print("Error occurred in the ipsec profile section")


    # Get the vrf settings
    try:
        vrfs_context_dict = sdk.get.vrfcontexts()
        vrf_profiles_dict = sdk.get.vrfcontextprofiles()

        if PRINT == True:
            print('vrf_context: ', json.dumps(vrfs_context_dict.json(),indent=4))
            print('vrf_profiles: ', json.dumps(vrf_profiles_dict.json(),indent=4))

        if WRITE_TO_FILE == True:
            with open(filename, 'a') as f:
                f.write('***** vrf contexts **********\n')
                f.write(json.dumps(vrfs_context_dict.json(), indent=4))
                f.write('***** vrf profiles **********\n')
                f.write(json.dumps(vrf_profiles_dict.json(), indent=4))
                f.write('\n***********************************************************************************************************************\n\n')
    except:
        print('Error occurred in the vrf section')

    # Routing - provides the configured items within the routing of an ION
    try:
        for item in element_dict:
            routing_routemaps = sdk.get.routing_routemaps(site_id=item['site_id'], element_id=item['element_id'])
            bgp_configs = sdk.get.bgpconfigs(site_id=item['site_id'], element_id=item['element_id'])
            if PRINT == True:
                print('***** routing routemaps **********\n')
                print(json.dumps(routing_routemaps.json(), indent=4))
                print('***** bgp configs **********\n')
                print(json.dumps(bgp_configs.json(), indent=4))

            if WRITE_TO_FILE == True:
                with open(filename, 'a') as f:
                    f.write('***** routing routemaps **********\n')
                    f.write(json.dumps(routing_routemaps.json(), indent=4))
                    f.write('***** bgp configs **********\n')
                    f.write(json.dumps(bgp_configs.json(), indent=4))
                    f.write('\n***********************************************************************************************************************\n\n')

    except:
        print('Error occurred in the routing section: \n', bgp_configs.json(), '\n', routing_routemaps.json())

