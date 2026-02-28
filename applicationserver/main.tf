# ---------- Security Group ----------
resource "aws_security_group" "app_sg" {
  name        = "docker4-app-sg"
  description = "Allow SSH, HTTP, and App Port"


  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App Port"
    from_port   = 5000
    to_port     = 5000
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


# ---------- EC2 Instance ----------
resource "aws_instance" "docker_ec2" {
  ami                    = "ami-0737d2d50c7fece1b" # Amazon Linux 2 (us-east-1)
  instance_type          = "t3.micro"
  key_name               = "ansible"  # 🔴 CHANGE THIS to your key pair name
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              sudo yum install docker -y
              service docker start
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user

    EOF

  tags = {
    Name = "Docker-App-EC2"
  }
}

# ---------- Output ----------
output "ec2_public_ip" {
  value = aws_instance.docker_ec2.public_ip
}