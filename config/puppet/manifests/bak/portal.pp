node default{
	include portal_deploy
}

class portal_deploy{
	file{ "/root/portal_deploy.sh":
		alias => "portal_deploy.sh",
		source => "puppet://pxeserver/files/portal_deploy.sh",
		owner => root,
		group => root,
		mode => 755;
	}
	
	exec{ "/bin/sh /root/portal_deploy.sh":
		subscribe => File["/root/portal_deploy.sh"],
		refreshonly => true;
	}
}
