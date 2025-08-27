systemctl stop systemd-tmpfiles-clean.timer
systemctl stop logrotate.timer
systemctl stop unbound-anchor.timer
systemctl mask systemd-tmpfiles-clean.timer
systemctl mask logrotate.timer 
systemctl mask unbound-anchor.timer 


