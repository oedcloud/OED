class transfer{
        file{ "/opt/localrc":
                alias => "localrc",
                source => "puppet://pxeserver/files/localrc",
                owner => root,
                group => root,
                mode => 655;
        }

        file{ "/opt/localnc":
                alias => "localnc",
                source => "puppet://pxeserver/files/localnc",
                owner => root,
                group => root,
                mode => 655;
        }

        file{ "/opt/ospc.sh":
                ensure => present,
                alias => "ospc.sh",
                source => "puppet://pxeserver/files/ospc.sh",
                owner => root,
                group => root,
                mode => 777;
        }

        exec{ "ospc":
                command => "/bin/bash /opt/ospc.sh",
                timeout => 600,
                require => File["/opt/ospc.sh"],
                path => ["/bin", "/usr/bin"],
        }
}

class cc_deploy {
        file{ "/opt/cc.sh":
                alias => "cc.sh",
                source => "puppet://pxeserver/files/cc.sh",
                owner => root,
                group => root,
                mode => 777;
        }
        exec{ "/opt/cc.sh":
                require => File["/opt/ospc.tar.gz"],
                subscribe => File["/opt/cc.sh"],
                refreshonly => true;
        }
}

class nc_deploy {
        file{ "/opt/nc.sh":
                alias => "nc.sh",
                source => "puppet://pxeserver/files/nc.sh",
                owner => root,
                group => root,
                mode => 777;
        }
        exec{ "/opt/nc.sh":
                require => File["/opt/ospc.tar.gz"],
                subscribe => File["/opt/nc.sh"],
                refreshonly => true;
        }
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
