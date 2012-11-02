
class deploy{
        file{ "/opt/deploy.sh":
                ensure => present,
                alias => "deploy.sh",
                source => "puppet://pxeserver/files/deploy.sh",
                owner => root,
                group => root,
                mode => 755;
        }

        file{ "/opt/localrc":
                ensure => present,
                alias => "localrc",
                source => "puppet://pxeserver/files/localrc",
                owner => root,
                group => root,
                mode => 655;
        }

        exec{ "ospc":
                command => "/bin/bash /opt/deploy.sh",
                require => File["/opt/deploy.sh", "/opt/localrc"],
                path => ["/bin", "/usr/bin","/sbin","/usr/sbin","/usr/local/sbin","/usr/local/bin"],
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


node default {
   include test
}

node 'nova24.sh.intel.com' { 
  include deploy
}
node 'nova40.sh.intel.com' { 
  include deploy
}
node 'nova27.sh.intel.com' { 
  include deploy
}
node 'nova20.sh.intel.com' { 
  include deploy
}
