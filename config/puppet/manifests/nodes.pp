node default {
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

node cc_config {
    include cc_deloy
}

node 'nova40.sh.intel.com' inherits cc_config {
}	
