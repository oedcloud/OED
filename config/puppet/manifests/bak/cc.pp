node default{
	include cc_deploy
}

class cc_deploy{
	file{ "/root/cc_deploy.sh":
		alias => "cc_deploy.sh",
		source => "puppet://pxeserver/files/cc_deploy.sh",
		owner => root,
		group => root,
		mode => 755;
	}
	
	exec{ "/bin/sh /root/cc_deploy.sh":
		subscribe => File["/root/cc_deploy.sh"],
		refreshonly => true;
	}
}
