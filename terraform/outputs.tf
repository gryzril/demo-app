# Outputs, like ALB DNS name, RDS endpoint

output "alb_dns_name" {
  value = aws_lb.myapp_alb.dns_name
}

output "rds_endpoint" {
  value = aws_db_instance.myapp_db.endpoint
}
