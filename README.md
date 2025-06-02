# Defining hypervisors and VMs

## Adding a new hyperisor

1. Add it to the inventory `hosts` file
2. Add the VM names and dependencies to `host_vars/<inventory_hostname>.yml`
3. Run the playbook to generate the unit files

## Host variable structure

```
$ cat host_vars/hypervisor.example.com.yml
---
vms:
  - name: firewall
    depends_on: []
    waitfor_port: 22
    waitfor_addr: firewall.example.com
  - name: adserver
    depends_on:
      - firewall
    waitfor_port: 3389
    waitfor_addr: adserver.example.com
  - name: nas
    depends_on:
      - adserver
      - firewall
    waitfor_port: 22
    waitfor_addr: nas.example.com
  - name: dockervm
    depends_on:
      - nas
      - firewall
    waitfor_port: 22
    waitfor_addr: dockervm.example.com
  - name: awx
    depends_on:
      - firewall
    waitfor_port: 22
    waitfor_addr: awx.example.com
```

# Starting VMs based on dependency order

```
ansible-playbook -i hosts startvms-no-systemd.yml
```

# Stopping VMs based on dependency order

```
ansible-playbook -i hosts stopvms-no-systemd.yml
```

# Generating systemd units (experimental)

## Generating the unit files with Ansible
```
ansible-playbook -i hosts -c local generate-systemd-units.yml
```

Use `--limit` or separate inventories as appropriate.

## Starting or stopping all VM's manually

```
sudo systemctl stop vm-group.target
sudo systemctl start vm-group.target
```

## Useful commands after editing unit files
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
```
