provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "tasks" {
  name         = "tasks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_instance" "app" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name      = "task-tracker-key"
  tags = { Name = "task-tracker" }
}

output "instance_public_ip" {
  value = aws_instance.app.public_ip
}
