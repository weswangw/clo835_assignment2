variable "region" { default = "us-east-1" }
variable "account_id" { default = "654654181039" }
variable "key_name" { default = null }

# TEMP creds for EC2 to pull from ECR during boot
variable "aws_access_key_id" { default = "PASTE_YOUR_CURRENT_ACCESS_KEY_ID" }
variable "aws_secret_access_key" { default = "PASTE_YOUR_CURRENT_SECRET_ACCESS_KEY" }
variable "aws_session_token" { default = "PASTE_YOUR_CURRENT_SESSION_TOKEN" }
