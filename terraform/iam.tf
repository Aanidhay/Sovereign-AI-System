resource "aws_iam_role" "sovereignai_cloudwatch_role" {
  name = "SovereignAI-CloudWatch-Role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cloudwatch_agent_policy" {
  role       = aws_iam_role.sovereignai_cloudwatch_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "nexusai_instance_profile" {
  name = "SovereignAI-Instance-Profile"
  role = aws_iam_role.sovereignai_cloudwatch_role.name
}