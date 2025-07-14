class log4j_remediation {
  # Stop affected services
  service { $log4j_services:
    ensure => stopped,
    before => File['replace_log4j_jars'],
  }

  # Replace vulnerable JARs
  file { 'replace_log4j_jars':
    ensure => present,
    source => 'puppet:///modules/log4j_remediation/log4j-core-2.17.1.jar',
    path   => $log4j_jar_locations,
    backup => true,
    notify => Service[$log4j_services],
  }

  # Restart services
  service { $log4j_services:
    ensure => running,
    subscribe => File['replace_log4j_jars'],
  }
}
