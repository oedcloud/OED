OED
===

openstack easy deployment


Automatic Installation Steps for OSPC
Definition and Preparation
* PXE Server: An installation machine for PXE, containing PXE installation packages, OSPC installation scripts and corresponding packages.
* Client Server: Client machines. By default these clients have double network cards. One connects to company network and gets IP address through DHCP. The other obtains static IP address from PXE Server.
* Switch: PXE Server and Client Server mutually connect via switch.
* Lots of network cables
* USB startup disk: Making USB flash disk from image or ospcdeploy source code (https://sh-svn.sh.intel.com/itflex_repos/svn_ospc/ospc/pxeinstall).
Steps
1.  Booting PXE Server from USB flash disk.
2.  Running startup.sh script by typing below commands:
cd /pxeinstall
./startup.sh
3.  Before starting up the client, testing whether PXE Server can distribute static IP to client. At the same time, setting PXE as enable and choosing to boot from network in BIOS. Waiting for OS installation completion later.
4.  When have been installed OS successfully, you can check installed machines information by access http://pxeserver/ospcdeploy/ospcdeploy (see diagram 1-1).
 
Diagram 1-1
    Submit button used to submit the machine role to database. 
    Configure button used to configure the machine’s installation parameters.
    Refresh button used to refresh the page.
    
Every machine information displays in a line, and also has three buttons in Action and a text icon (in the red circle), its function is as follows:
* Config: Configuring the machine’s installation parameters.
* Deploy: Configuring and installing packages of the corresponding role.
* Delete: Deleting the machine information and validation information in server.
* Log icon: Checking installation log.
5.  Steps for configuration Client Server:
a)  Connecting Client Server and PXE Server, and booting from network to install OS. 
b)  Assigning the corresponding role to Client Server: selecting Client Server in the Hostname drop-down menu, and selecting role in the role drop-down menu, and click the submit to confirm. After submitting, the form will display the newest role of the machine.
c)  Clicking Config button, and page will display configuration information.
d)  Clicking Deploy button, and Client Server begins to configure and install. Its status changes from ready to installing. When has been installed, its status changes from installing to Finished. During installation process, end user can check installation information through clicking text icon.
Q&A
1.  When network error occurs after installation client, this may be plug wrong of internal static IP network interface and external. You can try to change the two interfaces and try again.
2.  When clicking Deploy button, Deployment Failure has come out. Please check whether puppet client process works smoothly. If the process hasn’t existed, please restart the process.
3.  When clicking submit button, and promoting unable to open file error. The reason may be authority issue. Please enter the directory pxeinstall/httpd, type the command chmod 777 –R ospcdeploy and refresh the page.
4.  When to click log text icon, the page displays loading status. The reason may be log file is large and needs the more time.
5.  Client Server’s log information:
/opt/ospc/post.log is post installed script result log.
/opt/inst-deploy.log is ospc installed log.
