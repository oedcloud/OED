
node default{
	include nc_deploy	
}

class nc_deploy{
	file{ "/opt/nc.sh":
		alias => "nc.sh",
		source => "puppet://pxeserver/files/nc.sh",
		owner => root,
		group => root,
		mode => 777;
	}
	exec{ "/opt/nc.sh":
		subscribe => File["/opt/nc.sh"],
		refreshonly => true;
	}
}
