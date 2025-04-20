resource "null_resource" "k3s_install" {
  triggers = {
    instance_id = var.instance_id
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file(var.private_key_path)
    host        = var.instance_public_ip
  }

  provisioner "remote-exec" {
    inline = [
      # Install Docker
      "curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh ./get-docker.sh",

      # Add user to docker group
      "sudo groupadd docker || true",
      "sudo usermod -aG docker ubuntu"

      # Install rootless Docker
      #"curl -fsSL https://get.docker.com/rootless | sh",

      # Setup environment for rootless Docker
      #"echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc",
      #"echo 'export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock' >> ~/.bashrc",
      #"source ~/.bashrc",

      # Start rootless Docker
      #"~/.docker/bin/dockerd-rootless-setuptool.sh install",

      # Verify
      #"docker context use rootless",
      #"docker info | grep -i rootless"

      # Kind installation
      # "curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64",
      # "chmod +x ./kind",
      # "sudo mv ./kind /usr/local/bin/kind",

      # # Install kubectl
      # "curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\"",
      # "chmod +x kubectl",
      # "sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl",

            # Create Kind cluster
      #"kind create cluster --name mycluster --wait 5m",

      # Configure kubectl
      #"mkdir -p ~/.kube",
      #"kind get kubeconfig --name mycluster > ~/.kube/config",
      #"chmod 600 ~/.kube/config",
      #"echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc"
    ]
  }
}

