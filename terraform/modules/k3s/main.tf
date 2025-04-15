resource "null_resource" "k3s_install" {
  triggers = {
    instance_id = var.instance_id
  }

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(var.private_key_path)
    host        = var.instance_public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo curl -sfL https://get.k3s.io | sh -",
      "sudo chmod 644 /etc/rancher/k3s/k3s.yaml",
      "sleep 30",  # Wait for k3s to start
      "mkdir -p ~/.kube",
      "sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config",
      "sudo chown ec2-user:ec2-user ~/.kube/config",
      "export KUBECONFIG=~/.kube/config",
      "echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc"
    ]
  }
}

# Output the kubeconfig file
resource "null_resource" "get_kubeconfig" {
  depends_on = [null_resource.k3s_install]

  provisioner "local-exec" {
    command = "mkdir -p ~/.kube && scp -o StrictHostKeyChecking=no -i ${var.private_key_path} ec2-user@${var.instance_public_ip}:.kube/config ~/.kube/config-k3s"
  }
}
