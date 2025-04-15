output "instance_id" {
  value = aws_instance.k3s_node.id
}

output "instance_public_ip" {
  value = aws_instance.k3s_node.public_ip
}
