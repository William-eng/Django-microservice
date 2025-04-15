provider "aws" {
  region = var.aws_region
}

# Use existing or create a new VPC
module "vpc" {
  source = "./modules/vpc"
  
  vpc_name      = var.vpc_name
  vpc_cidr      = var.vpc_cidr
  azs           = var.availability_zones
  public_subnets = var.public_subnets
}

# Create EC2 instance for k3s
module "ec2" {
  source = "./modules/ec2"
  
  instance_name = var.instance_name
  ami_id        = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_id        = module.vpc.vpc_id
  subnet_id     = module.vpc.public_subnet_ids[0]
  security_group_id = module.vpc.security_group_id
  private_key_path  = var.private_key_path
}

# Setup k3s on EC2
module "k3s" {
  source = "./modules/k3s"
  
  instance_id   = module.ec2.instance_id
  instance_public_ip = module.ec2.instance_public_ip
  private_key_path = var.private_key_path
}


output "instance_public_ip" {
  value = module.ec2.instance_public_ip
  description = "The public IP address of the EC2 instance"
}

