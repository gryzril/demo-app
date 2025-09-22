# main config file

# Create VPC
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}

# Create Subnet
resource "aws_subnet" "subnet" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

# Security Group for ECS
resource "aws_security_group" "ecs_sg" {
  name        = "ecs_sg"
  description = "Allow inbound traffic to ECS services"
  vpc_id      = aws_vpc.main.id
}

# ECS Cluster
resource "aws_ecs_cluster" "myapp_cluster" {
  name = "myapp-cluster"
}

resource "aws_ecr_repository" "backend" {
  name                 = "myapp-backend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# ECS Task Definition (Backend)
resource "aws_ecs_task_definition" "backend" {
  family                   = "myapp-backend-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([{
    name      = "myapp-backend"
    image     = "${aws_ecr_repository.backend.repository_url}:${var.image_tag}"
    cpu       = 256
    memory    = 512
    essential = true
    portMappings = [{
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }]
  }])
}

# ECS Service for Backend
resource "aws_ecs_service" "backend_service" {
  name            = "myapp-backend-service"
  cluster         = aws_ecs_cluster.myapp_cluster.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = [aws_subnet.subnet.id]
    security_groups = [aws_security_group.ecs_sg.id]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.myapp_backend_target_group.arn
    container_name   = "myapp-backend"
    container_port   = 80
  }
}

# Application Load Balancer (ALB)
resource "aws_lb" "myapp_alb" {
  name               = "myapp-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_sg.id]
  subnets            = [aws_subnet.subnet.id]
}

# ALB Target Group
resource "aws_lb_target_group" "myapp_backend_target_group" {
  name     = "myapp-backend-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

# RDS PostgreSQL Instance (Optional)
resource "aws_db_instance" "myapp_db" {
  identifier        = "myapp-db"
  engine            = "postgres"
  engine_version    = "13.3"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  db_name           = var.db_name
  username          = var.db_username
  password          = var.db_password
  port              = 5432
  multi_az          = false
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.ecs_sg.id]
  db_subnet_group_name = aws_db_subnet_group.main.name
}

resource "aws_db_subnet_group" "main" {
  name       = "myapp-db-subnet-group"
  subnet_ids = [aws_subnet.subnet.id]
}

# Route 53 DNS Setup (optional)
resource "aws_route53_record" "myapp_record" {
  zone_id = "Z05973533QD1OSGESGX8D"
  name    = "gryzwa.xyz"
  type    = "A"
  ttl     = 60
  records = [aws_lb.myapp_alb.dns_name]
}
