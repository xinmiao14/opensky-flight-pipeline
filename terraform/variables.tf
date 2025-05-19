# This file contains the variable definitions for the OpenSky Terraform module.
variable "vpc_id" {
  description = "VPC ID where the resources will be created"
  type = string
}

variable "key_name" {
  description = "key pair name to use for EC2 instance"
  type = string
}

variable "db_name" {
  description = "Database name"
  type = string
}

variable "pg_username" {
  description = "Database admin username"
  type = string
  sensitive = true 
}

variable "cidr_ipv4" { 
  description = "local IP address in CIDR notation"
  type = string
  sensitive = true
}

variable "tfstate_bucket" {
  description = "S3 bucket for Terraform state"
  type = string
  default = "opensky-tfstate"
}

variable "opensky_data_bucket" {
  description = "S3 bucket for OpenSky data"
  type = string
  default = "opensky-dev-data"
}