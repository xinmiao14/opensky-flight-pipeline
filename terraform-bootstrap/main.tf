# This Terraform configuration file sets up the necessary resources for the OpenSky project.
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS provider 
provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "opensky_tfstate" {
  # Create S3 bucket for Terraform state
  bucket = "opensky-tfstate"
  force_destroy = true

  tags = {
    Name = "opensky-tfstate"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "opensky_tfstate_versioning" {
  # Enable versioning for the OpenSky Terraform state bucket
  bucket = aws_s3_bucket.opensky_tfstate.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "opensky_dev_data" {
  # Create S3 bucket for OpenSky data
  bucket = "opensky-dev-data"
  force_destroy = true

  tags = {
    Name = "opensky-dev-data"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "opensky_dev_data_versioning" {
  # Enable versioning for the OpenSky dev data bucket
  bucket = aws_s3_bucket.opensky_dev_data.id

  versioning_configuration {
    status = "Enabled"
  }
}