node default{
	include glance_cc_deploy
}

class glance_cc_deploy{
	file{ "/root/glance_cc_deploy.sh":
			alias => "glance_cc_deploy.sh",
			source => "puppet://pxeserver/files/glance_cc_deploy.sh",
			owner => root,
			group => root,
			mode => 755;
	}

	exec{ "/bin/sh /root/glance_cc_deploy.sh":
		subscribe => File["/root/glance_cc_deploy.sh"],
		refreshonly => true;
	}
}
