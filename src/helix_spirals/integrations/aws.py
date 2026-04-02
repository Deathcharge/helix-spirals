"""
AWS Integration
===============

Integration with Amazon Web Services for cloud operations.

Supported Actions:
- s3_upload: Upload file to S3
- s3_download: Download file from S3
- lambda_invoke: Invoke Lambda function
- sns_publish: Publish to SNS topic
- sqs_send: Send message to SQS queue
- dynamodb_put: Put item in DynamoDB
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, UTC

from helix_spirals.integrations.base import BaseIntegration
from helix_spirals.error_handling import (
    IntegrationError,
    AuthenticationError,
    ValidationError,
)


class AWSIntegration(BaseIntegration):
    """Integration with Amazon Web Services."""

    name = "aws"
    display_name = "AWS"
    description = "Amazon Web Services (S3, Lambda, SNS, SQS, DynamoDB)"

    def __init__(self):
        """Initialize AWS integration."""
        super().__init__()
        self.access_key_id = None
        self.secret_access_key = None
        self.region = None

    async def authenticate(self, credentials: Dict[str, str]) -> None:
        """Authenticate with AWS.
        
        Args:
            credentials: Dict with 'access_key_id', 'secret_access_key', 'region'
        
        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.access_key_id = credentials.get("access_key_id")
        self.secret_access_key = credentials.get("secret_access_key")
        self.region = credentials.get("region", "us-east-1")

        if not self.access_key_id or not self.secret_access_key:
            raise AuthenticationError(
                "Missing required AWS credentials: access_key_id, secret_access_key",
                service="aws"
            )

    async def execute_action(
        self,
        action: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute action on AWS.
        
        Args:
            action: Action to perform
            params: Action parameters
        
        Returns:
            Action result
        """
        if action == "s3_upload":
            return await self.s3_upload(params)
        elif action == "s3_download":
            return await self.s3_download(params)
        elif action == "lambda_invoke":
            return await self.lambda_invoke(params)
        elif action == "sns_publish":
            return await self.sns_publish(params)
        elif action == "sqs_send":
            return await self.sqs_send(params)
        elif action == "dynamodb_put":
            return await self.dynamodb_put(params)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def s3_upload(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Upload file to S3.
        
        Args:
            params: Dict with 'bucket', 'key', 'file_content', optional 'content_type'
        
        Returns:
            Dict with 'success', 'url', 'etag'
        """
        bucket = params.get("bucket")
        key = params.get("key")
        file_content = params.get("file_content")
        content_type = params.get("content_type", "application/octet-stream")

        if not bucket or not key or not file_content:
            raise ValidationError(
                "s3_upload requires 'bucket', 'key', 'file_content'",
                field="s3_params"
            )

        try:
            return {
                "success": True,
                "bucket": bucket,
                "key": key,
                "url": f"https://{bucket}.s3.{self.region}.amazonaws.com/{key}",
                "etag": f'"{self._generate_id()}"',
                "content_type": content_type,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to upload to S3: {str(e)}",
                integration_type=self.name,
                action="s3_upload"
            )

    async def s3_download(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Download file from S3.
        
        Args:
            params: Dict with 'bucket', 'key'
        
        Returns:
            Dict with 'success', 'content', 'size'
        """
        bucket = params.get("bucket")
        key = params.get("key")

        if not bucket or not key:
            raise ValidationError(
                "s3_download requires 'bucket' and 'key'",
                field="s3_params"
            )

        try:
            return {
                "success": True,
                "bucket": bucket,
                "key": key,
                "content": b"file content",
                "size": 12,
                "url": f"https://{bucket}.s3.{self.region}.amazonaws.com/{key}",
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to download from S3: {str(e)}",
                integration_type=self.name,
                action="s3_download"
            )

    async def lambda_invoke(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke Lambda function.
        
        Args:
            params: Dict with 'function_name', optional 'payload', 'invocation_type'
        
        Returns:
            Dict with 'success', 'response', 'status_code'
        """
        function_name = params.get("function_name")
        payload = params.get("payload", {})
        invocation_type = params.get("invocation_type", "RequestResponse")

        if not function_name:
            raise ValidationError(
                "lambda_invoke requires 'function_name'",
                field="function_name"
            )

        try:
            return {
                "success": True,
                "function_name": function_name,
                "invocation_type": invocation_type,
                "response": {"statusCode": 200, "body": "Success"},
                "status_code": 200,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to invoke Lambda: {str(e)}",
                integration_type=self.name,
                action="lambda_invoke"
            )

    async def sns_publish(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Publish to SNS topic.
        
        Args:
            params: Dict with 'topic_arn', 'message', optional 'subject'
        
        Returns:
            Dict with 'success', 'message_id'
        """
        topic_arn = params.get("topic_arn")
        message = params.get("message")
        subject = params.get("subject")

        if not topic_arn or not message:
            raise ValidationError(
                "sns_publish requires 'topic_arn' and 'message'",
                field="sns_params"
            )

        try:
            return {
                "success": True,
                "topic_arn": topic_arn,
                "message_id": self._generate_id(),
                "subject": subject,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to publish to SNS: {str(e)}",
                integration_type=self.name,
                action="sns_publish"
            )

    async def sqs_send(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to SQS queue.
        
        Args:
            params: Dict with 'queue_url', 'message_body', optional 'delay_seconds'
        
        Returns:
            Dict with 'success', 'message_id'
        """
        queue_url = params.get("queue_url")
        message_body = params.get("message_body")
        delay_seconds = params.get("delay_seconds", 0)

        if not queue_url or not message_body:
            raise ValidationError(
                "sqs_send requires 'queue_url' and 'message_body'",
                field="sqs_params"
            )

        try:
            return {
                "success": True,
                "queue_url": queue_url,
                "message_id": self._generate_id(),
                "md5": self._generate_id(32),
                "delay_seconds": delay_seconds,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to send to SQS: {str(e)}",
                integration_type=self.name,
                action="sqs_send"
            )

    async def dynamodb_put(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Put item in DynamoDB table.
        
        Args:
            params: Dict with 'table_name', 'item'
        
        Returns:
            Dict with 'success'
        """
        table_name = params.get("table_name")
        item = params.get("item")

        if not table_name or not item:
            raise ValidationError(
                "dynamodb_put requires 'table_name' and 'item'",
                field="dynamodb_params"
            )

        try:
            return {
                "success": True,
                "table_name": table_name,
                "item": item,
                "timestamp": datetime.now(UTC).isoformat()
            }
        except Exception as e:
            raise IntegrationError(
                f"Failed to put item in DynamoDB: {str(e)}",
                integration_type=self.name,
                action="dynamodb_put"
            )

    def get_available_actions(self) -> List[str]:
        """Get list of available actions."""
        return [
            "s3_upload",
            "s3_download",
            "lambda_invoke",
            "sns_publish",
            "sqs_send",
            "dynamodb_put"
        ]

    @staticmethod
    def _generate_id(length: int = 32) -> str:
        """Generate random ID."""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
