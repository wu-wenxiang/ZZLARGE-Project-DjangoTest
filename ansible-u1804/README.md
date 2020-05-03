# Deploy

## Deploy to Ubuntu 18.04
```shell
cp inventory/inventory.ini.example inventory/inventory.ini
### Modify inventory/inventory.ini ###
ansible-playbook -i inventory/inventory.ini playbook/deploy.yml
```