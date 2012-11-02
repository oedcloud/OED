node default{
	include tomcat_deploy
}

class tomcat_deploy{
	file{ "/root/tomcat_deploy.sh":
		alias => "tomcat_deploy.sh",
		source => "puppet://pxeserver/files/tomcat_deploy.sh",
		owner => root,
		group => root,
		mode => 755;
	}
	
	exec{ "/bin/sh /root/tomcat_deploy.sh":
		subscribe => File["/root/tomcat_deploy.sh"],
		refreshonly => true;
	}
}
