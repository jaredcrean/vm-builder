#!/sbin/env python2.7

import yaml, argparse

parser = argparse.ArgumentParser(description="A easy way to deploy a VM with virsh")
parser.add_argument('-t', '--template', action="store", dest="Os_Config_File", \
                    help="location of the yaml file")
args = parser.parse_args()
os_file = args.Os_Config_File


def yml_import(filepath):
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
            os_settings = config['config']
        return os_settings


settings = yml_import(os_file)





def VMCreate(SettingsDic):
    """
    Requires module  os, sys, subprocess
    """
    import os, sys, subprocess

    Virt_Install = ("/usr/bin/virt-install --name {} --ram {} --disk path={}\
                    --vcpus {} --os-type linux --os-variant rhel7 --network\
                    bridge=br0 --graphics none --virt-type kvm\
                    --console pty,target_type=serial \
                    --import").format(SettingsDic['HOST_NAME'], SettingsDic['RAM'],\
                    SettingsDic['OUTPUT_DISK'], SettingsDic['NUM_CPU'] )


    virt_opt = ("/usr/bin/virt-builder {} --hostname {} --root-password {} \
 --size {} --install {} --format {} --timezone {} -o {} \
 --update --selinux-relabel").format(SettingsDic['OS_FLAV'], SettingsDic['HOST_NAME'], \
 SettingsDic['PASSWORD'], SettingsDic['DISK_SIZE'], SettingsDic['PACKAGES_INSTALL'], \
 SettingsDic['FORMAT'], SettingsDic['TIME_ZONE'], SettingsDic['OUTPUT_DISK'])



    print "Creating Disk {}".format(SettingsDic['OUTPUT_DISK'])
    Build_VM = subprocess.Popen(virt_opt ,shell=True, stdout=subprocess.PIPE)
    print ""
    print virt_opt
    for line in iter(Build_VM.stdout.readline, b''):
        print ">> " + str(line.rstrip())
    INSTALL_OUTPUT = subprocess.Popen(Virt_Install, shell=True, stdout=subprocess.PIPE)
    print ""
    print INSTALL_OUTPUT
    output = INSTALL_OUTPUT.stdout
    for line in iter(output.readline, b''):
        print ">> " + str(line.rstrip())


VMCreate(settings)

