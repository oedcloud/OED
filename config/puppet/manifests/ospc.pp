
node default{
        include ospc_deploy
}

class ospc_deploy{
        file{ "/tmp/ospc.sh":
                alias => "ospc.sh",
                source => "puppet://pxeserver/files/ospc.sh",
                owner => root,
                group => root,
                mode => 777;
        }
        
        exec{ "/tmp/ospc.sh":
                subscribe => File["/tmp/ospc.sh"],
                refreshonly => true;
        }
}
