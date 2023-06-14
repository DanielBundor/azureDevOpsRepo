# Variables for common values

$resourceGroup = 'MyresourceGroup'
$location = 'westus'
$vmName = 'MyVM1'

# Create user object
$cred = Get-Credential -Message "Enter a username and password for the VM."

# Create a resource group
New-AzResourceGroup -ResourceGroupName $resourceGroup -Location $location

# Create a virtual machine
New-AzVM `
  -ResourceGroupName $resourceGroup `
  -Name $vmName
  -Location $location `
  -ImageName "win2016Datacenter" `
  -VirtualNetworkName "myVnet" `
  -SubnetName "mySubnet" `
  -SecurityGroupName "mySecurityGroup" `
  -PublicIpAddressName "myPublicIp" `
  -Credential $cred `
  -OpenPorts 3389

