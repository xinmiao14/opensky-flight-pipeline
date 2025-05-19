data "aws_iam_policy_document" "s3_access" {
  # IAM policy document for S3 access
  # This policy allows the EC2 instance to access the S3 buckets
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = ["s3:ListBucket"]
    resources = [
      # S3 bucket ARNs
      # Bucket names globally unique
      "arn:aws:s3:::${var.tfstate_bucket}",
      "arn:aws:s3:::${var.opensky_data_bucket}",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${var.tfstate_bucket}/*",
      "arn:aws:s3:::${var.opensky_data_bucket}/*"
    ]
  }
}

data "aws_iam_policy_document" "secrets_access" {
  # IAM policy document for Secrets Manager access
  # This policy allows the EC2 instance to access the database password stored in Secrets Manager
  version = "2012-10-17"
  
  statement {
    effect = "Allow"
    actions = ["secretsmanager:GetSecretValue"]
    resources = ["arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:*"]
  }
}

data "aws_iam_policy_document" "assume_EC2_role" {
  # IAM policy document for EC2 instance role
  # This policy allows the EC2 instance to assume the role
  version = "2012-10-17"

  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "opensky_ec2_role" {
  # IAM role for EC2 instance
  name = "opensky_ec2_role"
  assume_role_policy = data.aws_iam_policy_document.assume_EC2_role.json
}

resource "aws_iam_role_policy" "opensky_s3_access_policy" {
  # IAM policy for S3 access from EC2 instance
  name = "opensky_s3_access_policy"
  role = aws_iam_role.opensky_ec2_role.id
  policy = data.aws_iam_policy_document.s3_access.json
}

resource "aws_iam_role_policy" "opensky_secrets_access_policy" {
  # IAM policy for Secrets Manager access from EC2 instance
  name = "opensky_secrets_access_policy"
  role = aws_iam_role.opensky_ec2_role.id
  policy = data.aws_iam_policy_document.secrets_access.json
}

resource "aws_iam_instance_profile" "opensky_iam_instance_profile" {
  # IAM instance profile for EC2 instance
  name = "opensky_iam_instance_profile"
  role = aws_iam_role.opensky_ec2_role.name
}