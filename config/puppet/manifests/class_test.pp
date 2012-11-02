class test_class{
	file{"/tmp/test.txt":
		content => "hello world!",
		ensure => present,
		mode => 644,
		owner => root,
		group => root;
	}
}
