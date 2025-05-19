resource "aws_instance" "opensky_flight_pipeline" {
  # Create EC2 instance for OpenSky Flight Pipeline
  ami = data.aws_ami.amazon_linux_ami.id
  instance_type = "t2.micro"
  key_name = var.key_name
  # Adding security group to the EC2 instance
  vpc_security_group_ids = [aws_security_group.ec2_access.id, aws_security_group.ec2_to_rds.id]
  # Adding IAM instance profile to the EC2 instance
  iam_instance_profile = aws_iam_instance_profile.opensky_iam_instance_profile.name

  # Increases default EBS volume to the EC2 instance
  root_block_device {
    volume_size = 16 # Size of the root volume in GB
    volume_type = "gp2" # General Purpose SSD
  }

  tags = {
    Name = "OpenSky_Flight_Pipeline"
    Environment = "Dev"
  }
}

resource "aws_db_instance" "postgres_database" {
  # Create PostgreSQL RDS database instance
  allocated_storage = 20
  instance_class = "db.t4g.micro"
  engine = "postgres"
  engine_version = "14.17"
  db_name = var.db_name
  username = var.pg_username
  # Use AWS Secrets Manager to manage the database password
  manage_master_user_password = true
  master_user_secret_kms_key_id = aws_kms_key.pg_password.key_id
  parameter_group_name = "default.postgres14"
  skip_final_snapshot = true
  allow_major_version_upgrade = true
  storage_encrypted = true
  publicly_accessible = false
  # Adding security group to the RDS instance
  vpc_security_group_ids = [aws_security_group.rds_from_ec2.id]
  identifier = "cleaned-opensky-flight-database"

  tags = {
    Name = "Cleaned_OpenSky_Flight_Database"
    Environment = "Dev"
  }
}

resource "aws_kms_key" "pg_password" {
  # Create KMS key for encrypting the database password
  description = "PostgreSQL Database password for RDS"
}

data "aws_ami" "amazon_linux_ami"{
  # Fetch the latest Amazon Linux 2 AMI
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "name"
    values = ["al2023-ami-*-x86_64"]
  }
  filter {
    name = "architecture"
    values = ["x86_64"]
  }
  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
}