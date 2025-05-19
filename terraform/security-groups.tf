# This file contains the security group configurations for the OpenSky project.
resource "aws_security_group" "ec2_access" {
  # Create security group for inbound access to EC2 instance
  name = "ec2_access"
  description = "Allow EC2 inbound access"
  vpc_id = var.vpc_id

  tags = {
    Name = "ec2_access"
    Environment = "Dev"
  }
}

resource "aws_security_group" "ec2_to_rds" {
  # Create security group for outbound access from EC2 instance to RDS database
  name = "ec2_to_rds"
  description = "Allows EC2 access to RDS database on port 5432"
  vpc_id = var.vpc_id

  tags = {
    Name = "EC2 to RDS"
    Environment = "Dev"
  }
}

resource "aws_security_group" "rds_from_ec2" {
  # Create security group to allow inbound access to RDS database from EC2 instance
  name = "rds_from_ec2"
  description = "Allows EC2 access to RDS database on port 5432"
  vpc_id = var.vpc_id

  tags = {
    Name = "RDS from EC2"
    Environment = "Dev"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_rds_from_ec2_ingress" {
  # Add ingress rule to allow EC2 instance to connect to RDS database
  security_group_id = aws_security_group.rds_from_ec2.id
  referenced_security_group_id = aws_security_group.ec2_to_rds.id
  from_port = 5432
  to_port = 5432
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_ec2_to_rds_egress" {
  # Add egress rule to allow EC2 instance to connect to RDS database
  security_group_id = aws_security_group.ec2_to_rds.id
  referenced_security_group_id = aws_security_group.rds_from_ec2.id
  from_port = 5432
  to_port = 5432
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ingress" {
  # Add ingress rule to allow SSH access to EC2 instance
  security_group_id = aws_security_group.ec2_access.id
  cidr_ipv4 = var.cidr_ipv4
  from_port = 22
  to_port = 22
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "allow_fastapi_ingress" {
  # Add ingress rule to allow FastAPI access to EC2 instance
  security_group_id = aws_security_group.ec2_access.id
  cidr_ipv4 = "0.0.0.0/0"
  from_port = 8000
  to_port = 8000
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_outbound_egress" {
  # Add egress rule to allow outbound access from EC2 instance
  security_group_id = aws_security_group.ec2_access.id
  cidr_ipv4 = "0.0.0.0/0"
  ip_protocol = "-1" # all protocols
} 