# Variables for configuration

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for Subnet"
  default     = "10.0.1.0/24"
}

variable "db_username" {
  description = "Database username"
  default     = "app"
}

variable "db_password" {
  description = "Database password"
  default     = "db"
}

variable "db_name" {
  description = "Database name"
  default     = "app"
}

variable "ecs_instance_type" {
  description = "ECS instance type for Fargate"
  default     = "t3.micro"
}

variable "image_tag" { default = "latest" }