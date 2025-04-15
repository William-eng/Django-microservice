variable "instance_id" {
  description = "ID of the EC2 instance"
  type        = string
}

variable "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  type        = string
}

variable "private_key_path" {
  description = "Path to the private key file for SSH access"
  type        = string
}
