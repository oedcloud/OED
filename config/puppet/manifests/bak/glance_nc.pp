node default{
	include glance_nc_deploy
}

class glance_nc_deploy{
	file{ "/root/glance_nc_deploy.sh":
		alias => "glance_nc_deploy.sh",
		source => "puppet://pxeserver/files/glance_nc_deploy.sh",
		owner => root,
		group => root,
		mode => 755;
	}
	
	exec{ "/bin/sh /root/glance_nc_deploy.sh":
		subscribe => File["/root/glance_nc_deploy.sh"],
		refreshonly => true;
	}
}
