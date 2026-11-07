# =============================================================
# Lab 8: Infrastructure Provisioning & Deployment using Terraform
# main.tf - Microservice Infrastructure Configuration
# =============================================================

# -----------------------------------------------
# Step 1: Provider Configuration
# -----------------------------------------------
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = "us-east-1"
}

# -----------------------------------------------
# Security Group for Microservice
# -----------------------------------------------
resource "aws_security_group" "microservice_sg" {
  name        = "microservice-sg"
  description = "Security group for microservice container"

  # Allow HTTP traffic
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP"
  }

  # Allow HTTPS traffic
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS"
  }

  # Allow application port (8080)
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow Microservice App Port"
  }

  # Allow SSH for administration
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH"
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  tags = {
    Name        = "microservice-sg"
    Environment = "lab"
    Project     = "SOA-Lab8"
  }
}

# -----------------------------------------------
# EC2 Compute Instance for Microservice
# -----------------------------------------------
resource "aws_instance" "microservice_instance" {
  ami                    = "ami-0c02fb55956c7d316"  # Amazon Linux 2 (us-east-1)
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.microservice_sg.id]

  # User data script to install Docker and run microservice container
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker

    # Pull and run the microservice container
    docker pull nginx:latest
    docker run -d \
      --name microservice \
      -p 8080:80 \
      --restart always \
      nginx:latest

    echo "Microservice deployed successfully!" > /var/log/microservice-deploy.log
  EOF

  tags = {
    Name        = "microservice-instance"
    Environment = "lab"
    Project     = "SOA-Lab8"
    Role        = "microservice"
  }
}

# -----------------------------------------------
# Output Values
# -----------------------------------------------
output "instance_id" {
  description = "ID of the provisioned EC2 instance"
  value       = aws_instance.microservice_instance.id
}

output "public_ip" {
  description = "Public IP address of the microservice"
  value       = aws_instance.microservice_instance.public_ip
}

output "public_dns" {
  description = "Public DNS of the microservice instance"
  value       = aws_instance.microservice_instance.public_dns
}

output "microservice_url" {
  description = "URL to access the deployed microservice"
  value       = "http://${aws_instance.microservice_instance.public_ip}:8080"
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.microservice_sg.id
}
