
node default{
	include cc_deploy	
}

class cc_deploy{
	file{ "/opt/cc.sh":
		alias => "cc.sh",
		source => "puppet://pxeserver/files/cc.sh",
		owner => root,
		group => root,
		mode => 777;
	}
	exec{ "/opt/cc.sh":
		subscribe => File["/opt/cc.sh"],
		refreshonly => true;
	}
}
