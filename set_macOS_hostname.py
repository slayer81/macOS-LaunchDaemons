'''
1. Open a terminal.
2. Type the following command to change the primary hostname of your Mac: This is your fully qualified hostname, for example myMac.domain.com
sudo scutil --set HostName <new host name>
So for example:
sudo scutil --set HostName flame01.domain.com

3. Type the following command to change the Bonjour hostname of your Mac: This is the name usable on the local network, for example myMac.local.
sudo scutil --set LocalHostName <new host name>
So for example:
sudo scutil --set LocalHostName flame01

4. Type the following command to change the computer name: This is the user-friendly computer name you see in Finder, for example myMac.
sudo scutil --set ComputerName <new name>
So for example:
sudo scutil --set ComputerName flame01

5. Flush the DNS cache by typing: dscacheutil -flushcache   
6. Restart Mac.
'''
import os, sys, time

yes = ["y", "Y"]
cmdPrefix = 'sudo scutil'
setFlag = '--set'
getFlag = '--get'
flushCache = 'dscacheutil -flushcache '



fqdn = sys.argv[1]
host, domain = fqdn.split('.', 1)

dict = {
	'primary': {'label': 'Primary Hostname', 'command': 'HostName', 'string': fqdn},
	'bonjour': {'label': 'Bonjour Hostname', 'command': 'LocalHostName', 'string': host},
	'computer': {'label': 'Computer Name', 'command': 'ComputerName', 'string': host}
}




print("You are about to change your hostname to: " + fqdn)
print("This will require a system restart to fully take effect.")
print("Proceed? y / n")
confirmation = input()

if confirmation not in yes:
	print("Exiting......")
	sys.exit()
else:
	print("Commencing system configuration; your password may be required.")

	for key in dict.keys():
		# Set
		print("Changing \'{}\' to \'{}\'".format(dict[key]['label'], dict[key]['string']))
		setCommand = os.system("{} {} {} {}".format(cmdPrefix, setFlag, dict[key]['command'], dict[key]['string']))

		# Verify
		if setCommand == 0:
			print("Your {} is now \'{}\'\n".format(dict[key]['label'], dict[key]['string']))
		else:
			print("Failed to change {}. Exiting.".format(dict[key]['label']))
			sys.exit()

	# Flush DNS cache
	flushCommand = os.system("{}".format(flushCache))

print("Successfully set machine hostname. Do you want to restart now?     y / n")
reboot = input()
if reboot not in yes:
	print("Changes will take effect upon next system restart.")
	sys.exit()
else:
	print("Performing system restart in 5 seconds.")
	print("Press CTRL + c to terminate system restart")
	time.sleep(5)
	restart = os.system("sudo shutdown -r now")



