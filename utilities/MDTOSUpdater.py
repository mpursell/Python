# Script to update all the ts.xml files within
# #%DeploymentShare%\Control\<Name>\ with the later versions of the OS captures
# Mike Pursell 2014

## Script flow ##
# -> Copies the current Control directory to Desktop\ControlBAK
# --> If that's successful, use the Control\OperatingSystems.xml to create a dictionary of image names and GUIDs
# ----> Use the dictionary to look up the GUIDs for the given image names and
# #     slot them into specific indices into 2 lists, old and new OSs
# -----> Find and replace all instances of old list items with the corresponding new list items
#        - eg oldlist[0] -> oldlist[0]


import subprocess
import os
import itertools
from xml.etree import ElementTree

#  globals just so they're accessible at the top of the script.

#  location of the deploymentshare$\control folder
global target_folder
target_folder = # requires the path to the Control folder as a string

global old_xp_image_name
global old_7_32_image_name
global old_7_64_image_name
global new_xp_image_name
global new_7_32_image_name
global new_7_64_image_name


# Enter our image names for the old and new images
old_xp_image_name = ''
old_7_32_image_name = ''
old_7_64_image_name = ''

new_xp_image_name = ''
new_7_32_image_name = ''
new_7_64_image_name = ''





#function to copy the current folder to a backup
def backup():

    subprocess.call('xcopy /E {} ControlBAK\\'.format(target_folder))
 
			

#function to get the task sequence directories in the target folder
def listTsDirs():

    #get the list of files in the path, pull out only those that are directories
    dir_list = [dir for dir in os.listdir('{}'.format(target_folder)) if os.path.isdir(os.path.join('{}'.format(target_folder), dir))]

    #test print list of dirs
    #print (dir_list)

    return dir_list



#function to get the OS names and matching GUIDs from the OperatingSystems.xml.
def osGuids():

    os_dict = {}


    os_xml = ElementTree.parse('{}\\OperatingSystems.xml'.format(target_folder))
    os_xml_tree = os_xml.getroot()

    for child in os_xml_tree: # for each child (os tag)

        for child in os_xml_tree.iter():  # iterate over the children of the child (os)
            #print(child.tag)
            if child.tag == 'os':  # grab the os tags - returns (True, {guid})
                for value in child.attrib.values():
                    if value != 'True':  # we're only interested in the guid value so exclude the Trues
                        os_guid = value
                        # print(value)
            if child.tag == 'Name':  # grab the OS name tags
                os_name = child.text  # get the text inside the Name tag

                os_dict[os_name] = os_guid  # put the names and guids into a dictionary

    return os_dict




#  function to replace the OS GUIDs with the new ones in each of the task sequences,
#  takes the os_dict returned by osGuids() and the task sequence directory list from listTsDirs arguments
def osReplace(operating_system_dict, ts_dir_list):

    #print(os)

    old_guids_list = []
    new_guids_list = []


    #check our dictionary for the old image names and store the guids in the old_guids_list
    for os_name, os_guid in operating_system_dict.items():
       if os_name == old_xp_image_name:
           old_guids_list.insert(0,os_guid)  # insert the values at a specific index so we're not confusing GUIDs

    for os_name, os_guid in operating_system_dict.items():
       if os_name == old_7_32_image_name:
           old_guids_list.insert(1,os_guid)

    for os_name, os_guid in operating_system_dict.items():
       if os_name == old_7_64_image_name:
           old_guids_list.insert(2,os_guid)

    #test output
    #print (old_guids_list)

    #check our dictionary for the new image names and store the guids in the new_guids_list
    for os_name, os_guid in operating_system_dict.items():
       if os_name == new_xp_image_name:
           new_guids_list.insert(0, os_guid)  # insert the values at a specific index so we're not confusing GUIDs

    for os_name, os_guid in operating_system_dict.items():
       if os_name == new_7_32_image_name:
           new_guids_list.insert(1, os_guid)

    for os_name, os_guid in operating_system_dict.items():
       if os_name == new_7_64_image_name:
           new_guids_list.insert(2, os_guid)

    # test output
    # print (new_guids_list)
    # print('{}\nwill be replaced with\n{}'.format(old_guids_list, new_guids_list))

    for ts_directory in ts_dir_list:

        folder = os.path.join(target_folder, ts_directory, 'ts.xml')
        with open(folder, 'r') as task_sequence:  # open and read in the xml file as a string so we can call .replace()
            task_sequence = task_sequence.read()

            index_counter = 0  # since we explicitly set the indices for the lists, we can use slice

            for item in old_guids_list:
                # do a like for like - old_guids[0] for new_guids1[0] etc...
                task_sequence = task_sequence.replace(old_guids_list[index_counter], new_guids_list[index_counter])
                index_counter = index_counter+1

        with open(folder, 'w') as output_xml:  # write the file back out with amendments
            output_xml.write(task_sequence)

    #test print the xml
    #print(task_sequence)




def main():

    if backup() == None:  # make sure the backup is place before we do anything!

        #listTsDirs()
        #osGuids()

        osReplace(osGuids(), listTsDirs())
		

        print('\n **** Finished ***')

    else:  # if backup is not successful for some non-fatal reason, quit before we overwrite anything.
        print('Backup Failed...quitting')
        exit()

if __name__ == '__main__':
    main()
