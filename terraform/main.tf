terraform {
  backend "s3" {
    bucket = "sovereign-ai-system-bucket-aanidhay"
    key    = "sovereignai/terraform.tfstate"
    region = "ap-south-1"
  }
}

provider "aws" { region = "ap-south-1" }

resource "aws_security_group" "sovereign_sg" {
  name        = "sovereign-tunnel-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "sovereign_server" {
  ami           = "ami-01b40e1bcccae197a" 
  instance_type = "t3.large" 
  key_name      = "nexus-ai-key" 
  vpc_security_group_ids = [aws_security_group.sovereign_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y docker.io docker-compose
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker ubuntu
              EOF
  
  iam_instance_profile = aws_iam_instance_profile.nexusai_instance_profile.name
  tags = { Name = "SovereignAI-Server" }
}

resource "null_resource" "save_ip" {
  depends_on = [aws_instance.sovereign_server]
  provisioner "local-exec" {
    command = "echo ${aws_instance.sovereign_server.public_ip} > ip_address.txt"
  }
}