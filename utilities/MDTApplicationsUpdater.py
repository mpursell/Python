#check the applications xml and return a dict of {name: guid} for each
#stick the guids in ordered lists
#check the application groups.xml and do any replacements - need to check and replace ONLY guids in bundles
#check the task sequence xmls and do any replacements
# TODO - talk to SQL and see if we can do bundle replacements there.


import subprocess
import os
import itertools
from xml.etree import ElementTree


global target_folder
global target_file
target_folder = # requires Control folder as string
target_file = # requires path to Applications.XML as string


global old_flash_name
global old_shockwave_name
global old_reader_name
global old_anyconnect_name
global old_nac_name
global old_java8_name
global old_java7_name
global old_java8_64_name
global old_java7_64_name
global new_flash_name
global new_shockwave_name
global new_reader_name
global new_anyconnect_name
global new_nac_name
global new_java8_name
global new_java8_64_name
global new_java7_name
global new_java7_64_name

## OLD APP NAMES ##
old_flash_name = ''
old_shockwave_name = ''
old_reader_name = ''
old_anyconnect_name = ''
old_nac_name = ''
old_java8_name = ''
old_java8_64_name = ''
old_java7_name = ''
old_java7_64_name = ''

## NEW APP NAMES ##
new_flash_name = ''
new_shockwave_name = ''
new_reader_name = ''
new_anyconnect_name = ''
new_nac_name = ''
new_java8_name = ''
new_java8_64_name = ''
new_java7_name = ''
new_java7_64_name = ''

#####################

#function to copy the current folder to a backup
def backup():

    subprocess.call('xcopy /E {} ControlBAK\\'.format(target_folder))


#######################


def appGuids():

    app_dict = {}

    app_guid = ''

    app_xml = ElementTree.parse('{}\\Applications.xml'.format(target_folder))
    app_xml_tree = app_xml.getroot()

    for child in app_xml_tree: # for each child (app tag)

        for child in app_xml_tree.iter():  # iterate over the children of the child (application)
            #print(child.tag)
            if child.tag == 'application':  # grab the application tags - returns (True, {guid})
                for value in child.attrib.values():
                    if value != 'True':  # we're only interested in the guid value so exclude the 'Trues'
                        app_guid = value
                        # print(value)
            if child.tag == 'Name': # grab the application name tags
                app_name = child.text  # get the text inside the Name tag

                app_dict[app_name] = app_guid  # put the names and guids into a dictionary

    #print(app_dict)
    return app_dict


def appReplace(application_dict):  # needs a file as an argument for the amendments!!

    #print(app)

    old_guids_list = []
    new_guids_list = []


    #check our dictionary for the old image names and store the guids in the old_guids_list
    #for every additional application a FOR block will need to be created for old and new guids
    for app_name, app_guid in application_dict.items():
        if app_name == old_flash_name:
            old_guids_list.insert(0,app_guid)  # insert the values at a specific index so we're not confusing GUIDs

    for app_name, app_guid in application_dict.items():
        if app_name == old_shockwave_name:
            old_guids_list.insert(1,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == old_reader_name:
            old_guids_list.insert(2,app_guid)
    
    for app_name, app_guid in application_dict.items():
        if app_name == old_anyconnect_name:
            old_guids_list.insert(3,app_guid)
    
    for app_name, app_guid in application_dict.items():
        if app_name == old_nac_name:
            old_guids_list.insert(4,app_guid)
            
    for app_name, app_guid in application_dict.items():
        if app_name == old_java8_name:
            old_guids_list.insert(5,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == old_java8_64_name:
            old_guids_list.insert(6,app_guid)
            
    for app_name, app_guid in application_dict.items():
        if app_name == old_java7_name:
            old_guids_list.insert(7,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == old_java7_64_name:
            old_guids_list.insert(8,app_guid)

    #test output
    #print (old_guids_list)

    #check our dictionary for the new image names and store the guids in the new_guids_list
    for app_name, app_guid in application_dict.items():
        if app_name == new_flash_name:
            new_guids_list.insert(0,app_guid)  # insert the values at a specific index so we're not confusing GUIDs

    for app_name, app_guid in application_dict.items():
        if app_name == new_shockwave_name:
            new_guids_list.insert(1,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == new_reader_name:
            new_guids_list.insert(2,app_guid)
    
    for app_name, app_guid in application_dict.items():
        if app_name == new_anyconnect_name:
            new_guids_list.insert(3,app_guid)
    
    for app_name, app_guid in application_dict.items():
        if app_name == new_nac_name:
            new_guids_list.insert(4,app_guid)
            
    for app_name, app_guid in application_dict.items():
        if app_name == new_java8_name:
            new_guids_list.insert(5,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == new_java8_64_name:
            new_guids_list.insert(6,app_guid)
            
    for app_name, app_guid in application_dict.items():
        if app_name == new_java7_name:
            new_guids_list.insert(7,app_guid)

    for app_name, app_guid in application_dict.items():
        if app_name == new_java7_64_name:
            new_guids_list.insert(8,app_guid)

    # test output
    # print (new_guids_list)
   # print('{}\nwill be replaced with\n{}'.format(old_guids_list, new_guids_list))


    with open(target_file, 'r') as application_xml:
        application_xml = application_xml.read()

        index_counter = 0  # since we explictly set the indices for the lists, we can use slice
        for item in old_guids_list:
            application_xml = application_xml.replace(  # we only want to replace dependencies, NOT every app guid
                '<Dependency>{}</Dependency>'.format(old_guids_list[index_counter]),
                '<Dependency>{}</Dependency>'.format(new_guids_list[index_counter]))
            index_counter += 1

    with open(target_file, 'w') as output_xml:  # write the file back out with amendments
        output_xml.write(application_xml)




########################





def main():

    if backup() is None:  # make sure the backup is place before we do anything!

        appReplace(appGuids())

        print('\n **** Finished ***')

    else:  # if backup is not successful for some non-fatal reason, quit before we overwrite anything.
        print('Backup Failed...quitting')
        exit()

if __name__ == '__main__':
    main()
