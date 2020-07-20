#################################################################################################################
#	 									Login Gcloud 															#
#################################################################################################################
gcloud auth login
gcloud config set project electric-glyph-273720

#################################################################################################################
#                                              Setup                                                            #
#################################################################################################################
gcloud compute networks create bds-vpc \
    --bgp-routing-mode=regional \
    --description=private-network \
    --subnet-mode=custom

gcloud compute networks subnets create bds-private \
    --region=europe-west1 \
    --network=bds-vpc \
    --range=10.198.1.0/24 \
    --region=europe-west1 \
    --role=ACTIVE \
    --purpose=PRIVATE

gcloud compute routers create nat-router \
    --network=bds-vpc \
    --region=europe-west1

gcloud compute firewall-rules create bds-internal \
    --network=bds-vpc \
    --priority=1000 \
    --direction=INGRESS \
    --source-ranges=10.198.1.0/24 \
    --allow all

gcloud compute firewall-rules create bds-ssh \
    --direction=INGRESS \
    --priority=1000 \
    --network=bds-vpc \
    --target-tags=bastion \
    --source-ranges=0.0.0.0/0 \
    --allow tcp:22

gcloud compute instances create bastion-1 \
    --zone=europe-west1-b \
    --machine-type=n1-standard-1 \
    --tags=bds,bastion \
    --network-interface=network=bds-vpc,subnet=bds-private,private-network-ip=10.198.1.2 \
    --image-project=ubuntu-os-cloud --image-family=ubuntu-1604-lts

gcloud compute instances create nat-test \
    --zone=europe-west1-b \
    --machine-type=n1-standard-1 \
    --tags=bds \
    --network-interface=network=bds-vpc,subnet=bds-private,no-address,private-network-ip=10.198.1.3 \
    --image-project=ubuntu-os-cloud --image-family=ubuntu-1604-lts

gcloud compute instances create s01 \
    --zone=europe-west1-b \
    --machine-type=n1-standard-2 \
    --tags=bds,hadoop \
    --network-interface=network=bds-vpc,subnet=bds-private,no-address,private-network-ip=10.198.1.10 \
    --create-disk=size=100GB \
    --image-project=ubuntu-os-cloud --image-family=ubuntu-1604-lts

gcloud compute instances create s02 \
    --zone=europe-west1-b \
    --machine-type=n1-standard-2 \
    --tags=bds,hadoop \
    --network-interface=network=bds-vpc,subnet=bds-private,no-address,private-network-ip=10.198.1.11 \
    --create-disk=size=100GB \
    --image-project=ubuntu-os-cloud --image-family=ubuntu-1604-lts

gcloud compute instances create s03 \
    --zone=europe-west1-b \
    --machine-type=n1-standard-2 \
    --tags=bds,hadoop \
    --network-interface=network=bds-vpc,subnet=bds-private,no-address,private-network-ip=10.198.1.12 \
    --create-disk=size=100GB \
    --image-project=ubuntu-os-cloud --image-family=ubuntu-1604-lts

ssh-keygen -b 2048 -t rsa -f /tmp/sshkey -q -N ""
cat /dev/zero | ssh-keygen -b 4098 -C e_proimakis -q -N ""

ssh-copy-id -i ~/.ssh/id_rsa root@10.198.1.10,11,12
ssh -i gcloud_rsa_external e_proimakis@34.77.186.112

#################################################################################################################
#                                              Tear Down                                                        #
#################################################################################################################
gcloud compute instances delete bastion-1 --quiet --zone=europe-west1-b

gcloud compute instances delete nat-test --quiet --zone=europe-west1-b

gcloud compute instances delete s01 s02 s03 --quiet --zone=europe-west1-b

gcloud compute networks subnets delete bds-private --quiet --region=europe-west1

gcloud compute firewall-rules delete bds-internal bds-ssh --quiet

gcloud compute routers delete nat-router --region=europe-west1 --quiet

gcloud compute networks delete bds-vpc --quiet

#################################################################################################################
#                                              Start Stop                                                       #
#################################################################################################################

gcloud compute instances stop --zone=europe-west1-b bastion-1 nat-test s01 s02 s03

gcloud compute instances start --zone=europe-west1-b bastion-1 nat-test s01 s02 s03