node default {
	include test2
}

class test{
	file{"/tmp/andrewy.txt":
		content => "hello world!\n",
		ensure => present,
		mode => 644,
		owner => root,
		group => root,
	}
} 

class test1{
	file{
		"/tmp/test.txt":
			ensure => present;
	}
	exec{
		"/bin/echo 'cccccc' >> /tmp/test.txt":
			require => [File["/tmp/test.txt"]];
	}
	exec{
		"/bin/echo 'bbbbbb' >> /tmp/test.txt":
			require => [File["/tmp/test.txt"]];
	}
	exec{
		"/bin/echo 'aaaaaa' >> /tmp/test.txt":
			require => [File["/tmp/test.txt"]];
	}
	
}

class test2{
	file{ "/tmp/test.sh":
		alias => "test.sh",
		source => "puppet://pxeserver/files/test.sh",
		owner => root,
		group => root,
		mode => 755; 
	}
	
	exec{ "/tmp/test.sh":
		subscribe => File["/tmp/test.sh"],
		refreshonly => true;
	}
}
