output "ec2_public_ip" {
  # Output the public IP address of the EC2 instance
  description = "Public IP address assigned to the EC2 instance"
  value = aws_instance.opensky_flight_pipeline.public_ip
}

output "rds_endpoint" {
  # Output the endpoint of the RDS database
  description = "Value of the RDS database endpoint"
  value = aws_db_instance.postgres_database.endpoint
}