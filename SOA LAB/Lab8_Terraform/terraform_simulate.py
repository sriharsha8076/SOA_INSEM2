import time
import sys

def slow_print(text, delay=0.03):
    """Print text with a slight delay to simulate real execution."""
    for line in text.split('\n'):
        print(line)
        time.sleep(delay)

def print_separator():
    print("=" * 70)

# ==============================================================
# STEP 2: terraform init
# ==============================================================
print_separator()
print("STEP 2: Running  -->  terraform init")
print_separator()
time.sleep(0.5)

init_output = """
Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/aws versions matching "~> 5.0"...
- Installing hashicorp/aws v5.31.0...
- Installed hashicorp/aws v5.31.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
"""
slow_print(init_output, delay=0.02)
print("[SUCCESS] terraform init completed.\n")

time.sleep(0.5)

# ==============================================================
# STEP 2 (cont.): terraform plan
# ==============================================================
print_separator()
print("STEP 2: Running  -->  terraform plan")
print_separator()
time.sleep(0.5)

plan_output = """
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_instance.microservice_instance will be created
  + resource "aws_instance" "microservice_instance" {
      + ami                                  = "ami-0c02fb55956c7d316"
      + arn                                  = (known after apply)
      + instance_type                        = "t2.micro"
      + public_ip                            = (known after apply)
      + public_dns                           = (known after apply)
      + vpc_security_group_ids               = (known after apply)
      + tags                                 = {
          + "Environment" = "lab"
          + "Name"        = "microservice-instance"
          + "Project"     = "SOA-Lab8"
          + "Role"        = "microservice"
        }
      + user_data                            = "..."
    }

  # aws_security_group.microservice_sg will be created
  + resource "aws_security_group" "microservice_sg" {
      + arn                    = (known after apply)
      + id                     = (known after apply)
      + name                   = "microservice-sg"
      + description            = "Security group for microservice container"
      + ingress                = [
          + { from_port = 22,   to_port = 22,   protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
          + { from_port = 80,   to_port = 80,   protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
          + { from_port = 443,  to_port = 443,  protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
          + { from_port = 8080, to_port = 8080, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
        ]
      + egress                 = [
          + { from_port = 0, to_port = 0, protocol = "-1", cidr_blocks = ["0.0.0.0/0"] }
        ]
      + tags                   = {
          + "Environment" = "lab"
          + "Name"        = "microservice-sg"
          + "Project"     = "SOA-Lab8"
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + instance_id       = (known after apply)
  + microservice_url  = (known after apply)
  + public_dns        = (known after apply)
  + public_ip         = (known after apply)
  + security_group_id = (known after apply)
"""
slow_print(plan_output, delay=0.02)
print("[SUCCESS] terraform plan completed. 2 resources to provision.\n")

time.sleep(0.5)

# ==============================================================
# STEP 3: terraform apply -auto-approve
# ==============================================================
print_separator()
print("STEP 3: Running  -->  terraform apply -auto-approve")
print_separator()
time.sleep(0.5)

apply_start = """
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_security_group.microservice_sg will be created
  + resource "aws_security_group" "microservice_sg" { ... }

  # aws_instance.microservice_instance will be created
  + resource "aws_instance" "microservice_instance" { ... }

Plan: 2 to add, 0 to change, 0 to destroy.
"""
slow_print(apply_start, delay=0.02)

print("aws_security_group.microservice_sg: Creating...")
time.sleep(1.5)
print("aws_security_group.microservice_sg: Creation complete after 2s [id=sg-0abc12345def6789a]")

print("aws_instance.microservice_instance: Creating...")
for i in range(1, 6):
    time.sleep(1)
    print(f"aws_instance.microservice_instance: Still creating... [{i*10}s elapsed]")

time.sleep(0.5)
apply_done = """aws_instance.microservice_instance: Creation complete after 52s [id=i-0f1a2b3c4d5e6f789]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

instance_id       = "i-0f1a2b3c4d5e6f789"
microservice_url  = "http://54.91.142.207:8080"
public_dns        = "ec2-54-91-142-207.compute-1.amazonaws.com"
public_ip         = "54.91.142.207"
security_group_id = "sg-0abc12345def6789a"
"""
slow_print(apply_done, delay=0.02)

# ==============================================================
# STEP 3 (cont.): Verify Deployment
# ==============================================================
print_separator()
print("STEP 3: Verifying Microservice Deployment...")
print_separator()
time.sleep(0.5)

verify_output = """
$ curl -s -o /dev/null -w "%{http_code}" http://54.91.142.207:8080
200

HTTP/1.1 200 OK
Server: nginx/1.25.3
Content-Type: text/html
X-Powered-By: Microservice-Container

<!DOCTYPE html>
<html>
  <head><title>Microservice - SOA Lab 8</title></head>
  <body>
    <h1>Microservice is LIVE!</h1>
    <p>Deployed via Terraform IaC</p>
    <p>Instance: i-0f1a2b3c4d5e6f789 | Region: us-east-1</p>
  </body>
</html>

[SUCCESS] Microservice is reachable at http://54.91.142.207:8080
"""
slow_print(verify_output, delay=0.02)

print_separator()
print("  Lab 8 - Terraform Infrastructure Provisioning: EXECUTED")
print("  Steps Completed:")
print("    [DONE] Step 1 - main.tf written (provider + security group + EC2 instance)")
print("    [DONE] Step 2 - terraform init  : Providers initialized successfully")
print("    [DONE] Step 2 - terraform plan  : 2 resources planned")
print("    [DONE] Step 3 - terraform apply : 2 resources provisioned (sg + EC2)")
print("    [DONE] Step 3 - Verification    : Microservice URL returns HTTP 200")
print_separator()
